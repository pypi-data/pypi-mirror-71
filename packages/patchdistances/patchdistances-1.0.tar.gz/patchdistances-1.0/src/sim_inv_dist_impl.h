/*! \file sim_inv_dist_impl.h
	\brief Similarity invariant distance for patches (implementation)
	\sa sim_inv_dist.h
*/

#pragma once

#include "../include/device_matrix.h"
#include "../include/device_patches.h"
#include "../include/enums.h"
#include "../include/local_nearest_neighbor.h"
#include "../include/log_polar_transform.h"
#include "../include/math.h"
#include "../include/nearest_neighbor.h"
#include "../include/partition_NA.h"
#include "../include/rec_image.h"
#include "../include/sim_inv_dist.h"
#include "../include/type_traits.h"
#include "../include/unique_cufft_plan.h"
#include "../include/utils.h"
#include "../include/vec3.h"
#include "../include/warp_perspective.h"

#include "../extern/gsl/gsl_util"

#include <cuda_runtime.h>
#include <cufft.h>
#include <thrust/device_vector.h>
#include <thrust/execution_policy.h>
#include <thrust/extrema.h>
#include <thrust/for_each.h>
#include <thrust/functional.h>
#include <thrust/transform.h>

#include <algorithm>
#include <utility>
#include <vector>

// Requires compute capability of 2.0 or higher.
constexpr auto MAX_THREADS_X = 1024; /**< Max threads per block (x) */
constexpr auto MAX_BLOCKS_X = 2147483647; /**< Max blocks per grid (x); 2^31 - 1 */
constexpr auto SMEM_SIZE = 16 * 1024; /**< Shared memory size in bytes per block */
constexpr auto TwoPi = 6.283185307179586476925286766559005768394338798750211641949f; /**< Pi */

/*
 **
 ***
 **** Class
 ***
 **
 */

// Instantiate destructor.
#include "pimpl_impl.h"
template class pimpl<sim_inv_dist::impl>;

//! Implementation of sim_inv_dist class.
class sim_inv_dist::impl
{
  public:
	//! See class sim_inv_dist for a description.
	template<typename FloatVec>
	device_matrix<double> distance_matrix(const device_patches<FloatVec>& i_patches0,
										  const device_patches<FloatVec>& i_patches1,
										  const sid_params& i_params);

	//! See class sim_inv_dist for a description.
	template<typename FloatVec>
	std::pair<device_patches<FloatVec>, std::vector<size_t>>
		greedy_k_center(const device_patches<FloatVec>& i_patches, size_t i_clusters,
						size_t i_first, const sid_params& i_params);

	//! See class sim_inv_dist for a description.
	template<typename FloatVec>
	std::pair<device_matrix<FloatVec>, device_matrix<size_t>>
		reconstruct(const device_patches<FloatVec>& i_data_patches,
					const device_patches<FloatVec>& i_labels, const Size& i_img_size, rec_t i_type,
					const sid_params& i_params, interpolation_t i_interpolation);

	//! See class sim_inv_dist for a description.
	template<typename FloatVec>
	std::pair<device_matrix<FloatVec>, device_matrix<size_t>>
		reconstruct_w_translation(const device_patches<FloatVec>& i_data_patches,
								  const device_patches<FloatVec>& i_labels, const Size& i_img_size,
								  rec_t i_type, const sid_params& i_params,
								  interpolation_t i_interpolation);

	//! See class sim_inv_dist for a description.
	template<typename FloatVec>
	device_patches<float>
		perspective_transformations(const device_patches<FloatVec>& i_data_patches,
									const device_patches<FloatVec>& i_labels,
									const sid_params& i_params);

	//! See class sim_inv_dist for a description.
	device_patches<cuComplex> afmt(const device_patches<float>& i_patches, float i_sigma);

	//! See class sim_inv_dist for a description.
	device_patches<cuDoubleComplex> afmt(const device_patches<double>& i_patches, float i_sigma);

	//! See class sim_inv_dist for a description.
	device_patches<vec3<cuComplex>> afmt(const device_patches<vec3<float>>& i_patches,
										 float i_sigma);

	//! See class sim_inv_dist for a description.
	device_patches<vec3<cuDoubleComplex>> afmt(const device_patches<vec3<double>>& i_patches,
											   float i_sigma);

  private:
	//! A member function that conditionally (if needed) initializes the class.
	/*!
	 * \param i_M Size of the log polar interpolated patches. This has to be even and should
	 * be a power of 2.
	 * \param i_patch_count The number of patches to process simultaneously.
	 * \param private_cookie Prevents calling the method publicly.
	 * \param i_single If true use single precision, otherwise double precision.
	 * \param i_stride Stride in elements (not bytes) between consecutive elements.
	 * Usually 1, for vec3 3.
	 * \return Size of descriptor array.
	 */
	Size init(size_t i_M, size_t i_patch_count, bool i_single, size_t i_stride = 1);

	//! A member that computes the similarity-invariant patch descriptors using the
	//! Fourier-Mellin-Transformation.
	/*!
	 * \param i_patches Patches.
	 * \param i_params Parameters of the similarity invariant distance.
	 * \return A matrix with the afmt coefficients for each patch. It only contains one
	 * half of the actual matrix due to symmetry. The second part contains the center frequencies
	 * (0,0) and (-1,0) (in this order) for every patch.
	 */
	template<typename FloatVec>
	std::pair<device_patches<to_thrust_type_t<FloatVec>>,
			  device_patches<remove_vec3_t<to_thrust_type_t<FloatVec>>>>
		descriptors_cf(const device_patches<FloatVec>& i_patches, const sid_params& i_params);

	unique_cufft_plan m_plan{};

	size_t m_M{}; // log polar size
	size_t m_patch_count{};
	bool m_single{}; // single or double precision fft
};

/*
 **
 ***
 **** Free functions, such as CUDA kernels.
 ***
 **
 */

//! A CUDA kernel computing the distance between two similarity invariant descriptors.
/*!
 * It is expected that the grid dimension is equal to the number of descriptors in the first set.
 * It is expected that the block dimension is equal to the number of descriptors in the second
 set.
 * Each thread computes the distance between two descriptors and each block computes the distance
 * of one descriptor in i_a to every descriptor in i_b.
 * Each block loads one descriptor from i_a in shared memory. Thus shared memory should be of the
 * same size as the descriptors (i_a_col).
 * Memory is not allowed to overlap.
 * \param i_a_ptr Pointer to the first element of the first descriptor set.
 * \param i_b_ptr Pointer to the first element of the second descriptor set.
 * \param i_c_ptr Pointer to the first element of the allocated output. The distances are stored as
 * [a0b0 a1b0 ... a1b0 a1b1 ...].
 * \param i_size Length of each descriptor of i_a_ptr and i_b_ptr.
 */
template<typename ComplexVec>
__global__ void distance_kernel_shared(const ComplexVec* __restrict__ i_a_ptr,
									   const ComplexVec* __restrict__ i_b_ptr,
									   double* __restrict__ i_c_ptr, unsigned int i_size)
{
	const auto a_offset = blockIdx.x * i_size;
	const auto b_offset = threadIdx.x * i_size;

	// Strided shared memory loading. (template compatible declaration)
	extern __shared__ __align__(alignof(ComplexVec)) unsigned char smem[];
	ComplexVec* a_shared = reinterpret_cast<ComplexVec*>(smem);

	for(unsigned int i = threadIdx.x; i < i_size; i = i + blockDim.x)
	{
		a_shared[i] = i_a_ptr[i + a_offset];
	}
	__syncthreads();

	auto dist = float{};
	for(unsigned int i = 0; i < i_size; i++)
	{
		// Use a strided index for efficient shared memory loads.
		const auto index = (i + threadIdx.x) % i_size;
		dist += abs_square(a_shared[index] - i_b_ptr[b_offset + index]);
	}

	i_c_ptr[blockIdx.x + threadIdx.x * gridDim.x] = sqrt(dist);
}

//! A CUDA kernel computing the distance between two similarity invariant descriptors.
/*!
 * It is expected that the grid dimension is equal to the number of descriptors in the first set.
 * It is expected that the block dimension is equal to the number of descriptors in the second
 set.
 * Each thread computes the distance between two descriptors and each block computes the distance
 * of one descriptor in i_a to every descriptor in i_b.
  * Memory is not allowed to overlap.
 * \param i_a_ptr Pointer to the first element of the first descriptor set.
 * \param i_b_ptr Pointer to the first element of the second descriptor set.
 * \param i_c_ptr Pointer to the first element of the allocated output. The distances are stored as
 * [a0b0 a1b0 ... a1b0 a1b1 ...].
 * \param i_size Length of each descriptor of i_a_ptr and i_b_ptr.
 */
template<typename ComplexVec>
__global__ void distance_kernel(const ComplexVec* __restrict__ i_a_ptr,
								const ComplexVec* __restrict__ i_b_ptr,
								double* __restrict__ i_c_ptr, unsigned int i_size)
{
	const auto a_offset = blockIdx.x * i_size;
	const auto b_offset = threadIdx.x * i_size;

	auto dist = to_real_type_t<remove_vec3_t<ComplexVec>>{}; // float or double
	for(unsigned int i = 0; i < i_size; i++)
	{
		const auto val_a = i_a_ptr[i + a_offset];
		const auto val_b = i_b_ptr[i + b_offset];
		dist += abs_square(val_a - val_b);
	}

	i_c_ptr[blockIdx.x + threadIdx.x * gridDim.x] = sqrt(dist);
}

//! A  function that computes the distance between each element of two sets of descriptors.
/*!
 * \param i_descr_a The first set of descriptors. This should be the larger set. Maximal 2^31
 * descriptors are allowed.
 * \param i_descr_b The second set of descriptors. This should be the smaller set.
 * \return The distance matrix where each row contains the distance of one element in i_descr_a to
 * all elements in i_descr_b.
 */
template<typename ComplexVec>
device_matrix<double> distance_matrix_descriptors(const device_patches<ComplexVec>& i_descr_a,
												  const device_patches<ComplexVec>& i_descr_b)
{
	Expects(i_descr_a.total_per_patch() == i_descr_b.total_per_patch());
	Expects(i_descr_a.total_per_patch() == i_descr_b.total_per_patch());
	Expects(i_descr_a.patch_count() <= MAX_BLOCKS_X);
	Expects(i_descr_b.patch_count() <= MAX_THREADS_X);

	const auto size = gsl::narrow<unsigned int>(i_descr_a.total_per_patch());
	const auto patch_count_a = gsl::narrow<unsigned int>(i_descr_a.patch_count());
	const auto patch_count_b = gsl::narrow<unsigned int>(i_descr_b.patch_count());

	auto out = device_matrix<double>{Rows{patch_count_a}, Cols{patch_count_b}};

	const auto block = dim3{patch_count_b};
	const auto grid = dim3{patch_count_a};

	const auto smem_size = size * sizeof(ComplexVec);
	if(smem_size <= SMEM_SIZE)
	{
		distance_kernel_shared<<<grid, block, smem_size>>>(
			i_descr_a.data().get(), i_descr_b.data().get(), out.data().get(), size);
	}
	else
	{
		distance_kernel<<<grid, block>>>(i_descr_a.data().get(), i_descr_b.data().get(),
										 out.data().get(), size);
	}

	check(cudaDeviceSynchronize(), cudaSuccess);

	return out;
}

//! A CUDA kernel that computes a subset of the descriptors from one half of the
//! Fourier-Mellin-Coefficients.
/*!
 * blockDim: output rows (k+1); gridDim: patch count
 * The functions exploits the DFT symmetry: g(u,v) = g(-u,-v).
 * Thus each thread computes the descriptors of half a column.
 * \param i_f Fourier-Mellin-Coefficients computed with cufft.
 * \param i_c Center frequencies used for scaling. Two for each patch.
 * \param o_f Normalized coefficients of size (k+1)*(2v).
 * \param i_rows The number of rows of each patch.
 * \param i_cols The number of cols of each patch.
 * \param i_v The number of output columns.
 * \param i_sigma Fourier-Mellin coefficient.
 * \tparam ComplexVec Either cuComplex or cuDoubleComplex or vec3<>.
 */
template<typename ComplexVec>
__global__ void
	scale_afmt_kernel(const ComplexVec* __restrict__ i_f,
					  const remove_vec3_t<to_thrust_type_t<ComplexVec>>* __restrict__ i_c,
					  to_thrust_type_t<ComplexVec>* __restrict__ o_f, int i_rows, int i_cols,
					  int i_v, float i_sigma)
{
	// Each thread updates a row of a patch.
	const auto k1 = static_cast<int>(blockDim.x); // k+1!
	const auto tid = static_cast<int>(threadIdx.x); // row index starting at the center
	const auto pid = static_cast<int>(blockIdx.x); // patch index
	const auto off_i_patch = pid * i_rows * i_cols;
	const auto off_o_patch = pid * k1 * (2 * i_v);

	// Center coordinates, given that we work on half of the full dft.
	// For afmt_10 one, we exploit hermitian symmetry, since we have to use the coordinates
	// (-1,0) instead of (1,0).
	const auto afmt_00 = i_c[pid * 2];
	const auto arg_afmt_10 = arg(i_c[pid * 2 + 1]);
	const auto exp_10 = exp(make_complex(0.0f, (-tid) * arg_afmt_10));

	const auto v_begin = i_cols / 2 - i_v;
	const auto v_end = i_cols / 2 + i_v;
	for(int i = v_begin; i < v_end; i++)
	{
		const auto o_idx = off_o_patch + (k1 - 1 - tid) + ((i - v_begin) * k1);
		const auto in = i_f[off_i_patch + (i_rows - 1 - tid) + (i * i_rows)];
		const auto pow_00 = make_complex(-1.0f, (i - i_cols / 2) / i_sigma);
		const auto scale = pow(afmt_00, pow_00) * exp_10;

		// If the central coefficients are small, numerical errors will be very high.
		constexpr auto eps = 1.0f;
		if(abs(afmt_00) > eps)
		{
			o_f[o_idx] = to_thrust_type_t<ComplexVec>{scale} * make_thrust_type(in);
		}
		else
		{
			// 0.0 should be the best compromise between not making the distance to small, which
			// leads to problems when assigning patches and making the distance too high, which
			// leads to broken clustering.
			o_f[o_idx] = to_thrust_type_t<ComplexVec>{0.0f};
		}
	}
}

//! A function that computes a subset of the descriptors from one half of the
//! Fourier-Mellin-Coefficients.
/*!
 * \param i_frq Fourier-Mellin-Coefficients computed with cufft.
 * \param i_center_frq Center frequencies used for scaling. Two for each patch.
 * \param i_k The output rows are k + 1. Only unique descriptors are returned because of hermitian
 * symmetry.
 * \param i_v The output columns are 2 * v.
 * \param i_sigma Fourier-Mellin-Coefficient.
 * \return Normalized coefficients of size (k+1)*(2v).
 */
template<typename ComplexVec>
device_patches<to_thrust_type_t<ComplexVec>>
	scale_afmt(const device_patches<ComplexVec>& i_frq,
			   const device_patches<remove_vec3_t<to_thrust_type_t<ComplexVec>>> i_center_frq,
			   Rows i_k, Cols i_v, float i_sigma)
{
	Expects(i_k.value() + 1 <= i_frq.rows_patches());
	Expects(2 * i_v.value() <= i_frq.cols_patches());
	Expects(i_frq.patch_count() == i_center_frq.patch_count());
	Expects(i_center_frq.rows_patches() == 2);
	Expects(i_center_frq.cols_patches() == 1);

	auto out = device_patches<to_thrust_type_t<ComplexVec>>{
		patch_index{i_frq.patch_count()}, Rows{i_k.value() + 1}, Cols{2 * i_v.value()}};

	// Casts are safe, since the dimensions are small.
	const auto rows = gsl::narrow_cast<int>(i_frq.rows_patches());
	const auto cols = gsl::narrow_cast<int>(i_frq.cols_patches());
	const auto v = gsl::narrow_cast<int>(i_v.value());
	const auto blockDim = dim3{gsl::narrow_cast<unsigned int>(i_k.value() + 1)};
	const auto gridDim = dim3{gsl::narrow_cast<unsigned int>(i_frq.patch_count())};

	scale_afmt_kernel<<<gridDim, blockDim>>>(i_frq.data().get(), i_center_frq.data().get(),
											 out.data().get(), rows, cols, v, i_sigma);

	check(cudaDeviceSynchronize(), cudaSuccess);

	return out;
}

//! A function that copies the mean center frequencies (0,0) and (-1,0) from an AFMT.
/*
 * \param i_afmt AFMT as computed by sim_inv_dist::impl:afmt().
 * \return Center frequencies (0,0) and (1,0) (in this order) for each patch. For vec3 the mean
 * frequencies are returned.
 */
template<typename ComplexVec>
device_patches<remove_vec3_t<to_thrust_type_t<ComplexVec>>>
	get_center_frequencies(const device_patches<ComplexVec>& i_afmt)
{
	Expects(i_afmt.col_maj_patches());

	auto out = device_patches<remove_vec3_t<to_thrust_type_t<ComplexVec>>>{
		patch_index{i_afmt.patch_count()}, 2_rows, 1_cols};
	auto out_ptr = out.data().get();
	const auto afmt_ptr = i_afmt.data().get();

	const auto stride = i_afmt.ld();
	const auto rows = i_afmt.rows_patches();
	const auto cols = i_afmt.cols_patches();
	const auto idx_00 = (rows - 1) + (cols / 2 * rows);
	const auto idx_10 = idx_00 - 1;

	const auto begin = thrust::make_counting_iterator<size_t>(0);
	const auto end = begin + i_afmt.patch_count();

	thrust::for_each(begin, end, [=] __device__(size_t patch_idx) {
		out_ptr[patch_idx * 2] = mean(make_thrust_type(afmt_ptr[patch_idx * stride + idx_00]));
		out_ptr[patch_idx * 2 + 1] = mean(make_thrust_type(afmt_ptr[patch_idx * stride + idx_10]));
	});

	return out;
}

//! A functions computes the transformations between two sets of patches, but only for the specified
//! indices.
/*!
 * \param i_patches_cf0 Center frequencies (0,0) and (-1,0) of patches.
 * \param i_patches_cf1 Center frequencies (0,0) and (-1,0) of patches.
 * \param i_indices0 Indices for i_patches_cf0.
 * \param i_indices1 Indices for i_patches_cf1.
 * \param i_patches_size Size of the data patches and labels.
 * \param i_sigma Fourier-Mellin-Coefficient.
 * \return Transformations for i_patches_cf0[i] -> i_patches_cf1[i] (Cave: order).
 */
template<typename Complex>
device_patches<float> compute_transforms(const device_patches<Complex>& i_patches_cf0,
										 const device_patches<Complex>& i_patches_cf1,
										 const thrust::device_vector<size_t>& i_indices0,
										 const thrust::device_vector<size_t>& i_indices1,
										 const Size& i_patches_size, float i_sigma)
{
	const auto max0 = *thrust::max_element(i_indices0.cbegin(), i_indices0.cend());
	const auto max1 = *thrust::max_element(i_indices1.cbegin(), i_indices1.cend());

	Expects(i_patches_cf1.cols_patches() == 1);
	Expects(i_patches_cf1.rows_patches() == 2);
	Expects(i_patches_cf0.cols_patches() == 1);
	Expects(i_patches_cf0.rows_patches() == 2);
	Expects(i_indices0.size() == i_indices1.size());
	Expects(i_patches_cf0.patch_count() >= (max0 + 1));
	Expects(i_patches_cf1.patch_count() >= (max1 + 1));

	const auto row_maj = false;
	auto out =
		device_patches<float>{patch_index{i_patches_cf1.patch_count()}, 3_rows, 3_cols, row_maj};
	auto out_ptr = out.data().get();
	const auto ptr1 = i_patches_cf1.data().get();
	const auto ptr0 = i_patches_cf0.data().get();
	const auto ind_ptr0 = i_indices0.data().get();
	const auto ind_ptr1 = i_indices1.data().get();

	const auto begin = thrust::make_counting_iterator<size_t>(0);
	const auto end = begin + i_patches_cf1.patch_count();

	thrust::for_each(begin, end, [=] __device__(size_t idx) {
		const auto idx0 = ind_ptr0[idx];
		const auto idx1 = ind_ptr1[idx];
		const auto c00_l = ptr0[2 * idx0];
		const auto c10_l = ptr0[2 * idx0 + 1];
		const auto c00_d = ptr1[2 * idx1];
		const auto c10_d = ptr1[2 * idx1 + 1];

		const auto off_o = idx * 9;

		// Central frequencies should be >> 1. Otherwise they are probably 0s with rounding errors.
		// If not corrected, this leads to high errors in the following divisions.
		using Real = to_real_type_t<Complex>; // necessary for msvc
		const auto eps = 0.01f;
		const auto alpha = abs(c00_l) > eps && abs(c00_d) > eps
							   ? pow((c00_l / c00_d).real(), Real{-1.0f} / i_sigma)
							   : 1.0f;
		const auto beta = abs(c10_l) > eps && abs(c10_d) > eps ? log(c10_l / c10_d).imag() : 0.0f;

		const auto a_11 = static_cast<float>(alpha * cos(beta));
		const auto a_12 = static_cast<float>(alpha * -sin(beta));
		const auto a_21 = static_cast<float>(-a_12);
		const auto a_22 = static_cast<float>(a_11);
		const auto b_1 = 0.0f;
		const auto b_2 = 0.0f;

		perspective_matrix(a_11, a_12, b_1, a_21, a_22, b_2, i_patches_size, out_ptr + off_o);
	});

	return out;
}

//! A functions computes the transformations between two sets of patches, but only for the specified
//! indices. The indices for the first set are set to 0, 1, 2, ...
/*!
 * \param i_labels_cf Center frequencies (0,0) and (-1,0) for each label.
 * \param i_data_patches_cf Center frequencies (0,0) and (-1,0) for each data patch.
 * \param i_labels_indices Indices of labels matched to data patches.
 * \param i_patches_size Size of the data patches and labels.
 * \param i_sigma Fourier-Mellin-Coefficient.
 * \return Transformations labels -> data patches corresponding to the nearest neighbor
 * labeling.
 */
template<typename Complex>
device_patches<float> compute_transforms(const device_patches<Complex>& i_labels_cf,
										 const device_patches<Complex>& i_data_patches_cf,
										 const device_matrix<size_t>& i_labels_indices,
										 const Size& i_patches_size, float i_sigma)
{
	const auto data_indices = d_seq(i_labels_indices.total());

	return compute_transforms(i_labels_cf, i_data_patches_cf, i_labels_indices.container(),
							  data_indices, i_patches_size, i_sigma);
}

/*
 **
 ***
 **** Private members
 ***
 **
 */

template<typename FloatVec>
std::pair<device_patches<to_thrust_type_t<FloatVec>>,
		  device_patches<remove_vec3_t<to_thrust_type_t<FloatVec>>>>
	sim_inv_dist::impl::descriptors_cf(const device_patches<FloatVec>& i_patches,
									   const sid_params& i_params)
{
	const auto M = i_params.log_polar_size;
	const auto K = i_params.descriptors_rows;
	const auto V = i_params.descriptors_cols;
	const auto sigma = i_params.sigma;

	const auto embed = false; // Interpolate the largest disk contained in the patches.
	const auto transpose = true; // Patches need to be transposed before fft.
	auto lp_patches = log_polar_transform(i_patches, Rows{M}, Cols{M}, embed, transpose);
	// Rows == Cols: Necessary for fft, since the patches need to be transposed.

	const auto fmt = afmt(lp_patches, sigma);
	auto cf = get_center_frequencies(fmt);
	auto descr = scale_afmt(fmt, cf, K, V, sigma);

	return std::make_pair(std::move(descr), std::move(cf));
}

/*
 **
 ***
 **** Public members
 ***
 **
 */

template<typename FloatVec>
device_matrix<double>
	sim_inv_dist::impl::distance_matrix(const device_patches<FloatVec>& i_patches0,
										const device_patches<FloatVec>& i_patches1,
										const sid_params& i_params)
{
	return distance_matrix_descriptors(std::get<0>(descriptors_cf(i_patches0, i_params)),
									   std::get<0>(descriptors_cf(i_patches1, i_params)));
}

//! See class sim_inv_dist for a description.
template<typename FloatVec>
std::pair<device_patches<FloatVec>, std::vector<size_t>>
	sim_inv_dist::impl::greedy_k_center(const device_patches<FloatVec>& i_patches,
										size_t i_clusters, std::size_t i_first,
										const sid_params& i_params)
{
	Expects(i_clusters > 1);
	Expects(i_first < i_patches.patch_count());

	auto ind = std::vector<size_t>(i_clusters);
	ind.at(0) = i_first;
	const auto descr = std::get<0>(descriptors_cf(i_patches, i_params));
	auto dist =
		thrust::device_vector<double>(i_patches.patch_count(), std::numeric_limits<double>::max());

	for(size_t i = 1; i < i_clusters; i++)
	{
		const auto patch = copy(descr, std::vector<size_t>{ind.at(i - 1)});
		const auto dist_mat = distance_matrix_descriptors(descr, patch);
		thrust::transform(dist_mat.cbegin(), dist_mat.cend(), dist.cbegin(), dist.begin(),
						  thrust::minimum<double>{});
		const auto max = thrust::max_element(dist.cbegin(), dist.cend());
		ind.at(i) = thrust::distance(dist.cbegin(), max);
	}

	return std::make_pair(copy(i_patches, ind), std::move(ind));
}

template<typename FloatVec>
std::pair<device_matrix<FloatVec>, device_matrix<size_t>>
	sim_inv_dist::impl::reconstruct(const device_patches<FloatVec>& i_data_patches,
									const device_patches<FloatVec>& i_labels,
									const Size& i_img_size, rec_t i_type,
									const sid_params& i_params, interpolation_t i_interpolation)
{
	Expects(i_data_patches.size_patches() == i_labels.size_patches());

	const auto sigma = i_params.sigma;

	// Transformations for reconstruction and nearest neighbor labeling.
	// Use scoping to reduce memory footprint.
	auto patches_nn = [&] {
		const auto descr_cf_d = descriptors_cf(i_data_patches, i_params);
		const auto descr_cf_l = descriptors_cf(i_labels, i_params);
		const auto dist_mat =
			distance_matrix_descriptors(std::get<0>(descr_cf_d), std::get<0>(descr_cf_l));

		// Since only patches with full support are used, the nearest neighbor labeling is
		// smaller than the image.
		const auto select_min = true;
		const auto nn_size = patch_count_size(i_img_size, i_labels.size_patches());
		const auto nn = nearest_neighbor(dist_mat, nn_size, select_min);

		const auto nn_trans = compute_transforms(std::get<1>(descr_cf_l), std::get<1>(descr_cf_d),
												 nn, i_labels.size_patches(), sigma);
		const auto nn_labels = copy(i_labels, get_host_vector(nn));

		return std::make_pair(warp_perspective(nn_labels, nn_trans, i_interpolation), nn);
	}();

	return std::make_pair(rec_image(std::get<0>(patches_nn), i_img_size, i_type),
						  std::move(std::get<1>(patches_nn)));
}

template<typename FloatVec>
std::pair<device_matrix<FloatVec>, device_matrix<size_t>>
	sim_inv_dist::impl::reconstruct_w_translation(const device_patches<FloatVec>& i_data_patches,
												  const device_patches<FloatVec>& i_labels,
												  const Size& i_img_size, rec_t i_type,
												  const sid_params& i_params,
												  interpolation_t i_interpolation)
{
	Expects(i_data_patches.size_patches() == i_labels.size_patches());

	const auto sigma = i_params.sigma;

	// Transformations for reconstruction and nearest neighbor labeling.
	// Use scoping to reduce memory footprint.
	auto patches_nn = [&] {
		const auto descr_cf_d = descriptors_cf(i_data_patches, i_params);
		const auto descr_cf_l = descriptors_cf(i_labels, i_params);
		const auto dist_mat =
			distance_matrix_descriptors(std::get<0>(descr_cf_d), std::get<0>(descr_cf_l));

		// Since only patches with full support are used, the nearest neighbor labeling is
		// smaller than the image.
		const auto patch_size = i_labels.size_patches();
		const auto nn_size = patch_count_size(i_img_size, patch_size);
		const auto labeled = local_nearest_neighbor(dist_mat, nn_size, patch_size);

		// Get the transformations for the labeling.
		const auto nn_trans = compute_transforms(std::get<1>(descr_cf_l), std::get<1>(descr_cf_d),
												 labeled.labels.container(),
												 labeled.patches.container(), patch_size, sigma);

		// Warp and translate the patches.
		const auto nn_labels = copy(i_labels, get_host_vector(labeled.labels));
		const auto warped = warp_perspective(nn_labels, nn_trans, i_interpolation);
		const auto emb_size =
			Size{Rows{2 * patch_size.rows() - 1}, Cols{2 * patch_size.cols() - 1}};

		return std::make_pair(embed(warped, labeled.offsets, emb_size, FloatVec{details::NA}),
							  labeled.labels);
	}();

	// Due to embedding the patches (necessary for translation), the reconstructed image is
	// enlarged and needs to be cropped.
	const auto emb_labels_size = std::get<0>(patches_nn).size_patches();
	const auto rows = i_img_size.rows() + emb_labels_size.rows() - i_labels.rows_patches();
	const auto cols = i_img_size.cols() + emb_labels_size.cols() - i_labels.cols_patches();
	const auto emb_img_size = Size{Rows{rows}, Cols{cols}};
	const auto rec = rec_image(std::get<0>(patches_nn), emb_img_size, i_type);

	return std::make_pair(crop(rec, i_img_size), std::move(std::get<1>(patches_nn)));
}

template<typename FloatVec>
device_patches<float>
	sim_inv_dist::impl::perspective_transformations(const device_patches<FloatVec>& i_data_patches,
													const device_patches<FloatVec>& i_labels,
													const sid_params& i_params)
{
	Expects(i_data_patches.size_patches() == i_labels.size_patches());

	const auto patch_count = i_data_patches.patch_count();
	const auto sigma = i_params.sigma;

	const auto central_frq_d = std::get<1>(descriptors_cf(i_data_patches, i_params));
	const auto central_frq_l = std::get<1>(descriptors_cf(i_labels, i_params));

	// The nearest neighbor matrix is just the integer sequence 0, 1, 2, ...
	const auto nn = device_matrix<size_t>{d_seq(patch_count), Rows{patch_count}, Cols{1}};

	return compute_transforms(central_frq_l, central_frq_d, nn, i_labels.size_patches(), sigma);
}