/*! \file affine_inv_dist_impl.h
	\brief Affine invariant distance for patches (implementation)
	\sa affine_inv_dist.h
*/

#pragma once

#include "../include/affine_inv_dist.h"
#include "../include/device_matrix.h"
#include "../include/device_patches.h"
#include "../include/enums.h"
#include "../include/identity_solver.h"
#include "../include/imed.h"
#include "../include/least_squares_solver.h"
#include "../include/local_nearest_neighbor.h"
#include "../include/math.h"
#include "../include/metric.h"
#include "../include/nearest_neighbor.h"
#include "../include/partition_NA.h"
#include "../include/procrustes_solver.h"
#include "../include/rec_image.h"
#include "../include/type_traits.h"
#include "../include/unique_cublas_handle.h"
#include "../include/utils.h"
#include "../include/vec3.h"
#include "../include/warp_perspective.h"

#include "../extern/gsl/gsl_util"

#include <cuda_runtime.h>
#include <thrust/device_vector.h>

#include <numeric>
#include <utility>
#include <vector>

using uint = unsigned int; /**< unsigned int */
constexpr auto TColsFirst = uint{3}; /**< Columns of image moments T for first-order moments. */
constexpr auto TColsHigh = uint{7}; /**< Columns of image moments T for high-order moments. */

/*
 **
 ***
 **** Class
 ***
 **
 */

// Instantiate destructor.
#include "pimpl_impl.h"
template class pimpl<affine_inv_dist::impl>;

//! Implementation of affine_inv_dist class.
class affine_inv_dist::impl final
{
  public:
	//! See class affine_inv_dist for a description.
	template<typename FloatVec>
	device_matrix<double> distance_matrix(const device_patches<FloatVec>& i_patches0,
										  const device_patches<FloatVec>& i_patches1,
										  const aid_params& i_params);

	//! See class affine_inv_dist for a description.
	template<typename FloatVec>
	std::pair<device_patches<FloatVec>, std::vector<size_t>>
		greedy_k_center(const device_patches<FloatVec>& i_patches, size_t i_clusters,
						std::size_t i_first, const aid_params& i_params);

	//! See class affine_inv_dist for a description.
	template<typename FloatVec>
	std::pair<device_matrix<FloatVec>, device_matrix<size_t>>
		reconstruct(const device_patches<FloatVec>& i_data_patches,
					const device_patches<FloatVec>& i_patches1, const Size& i_img_size,
					rec_t i_type, const aid_params& i_params);

	//! See class affine_inv_dist for a description.
	template<typename FloatVec>
	std::pair<device_matrix<FloatVec>, device_matrix<size_t>>
		reconstruct_w_translation(const device_patches<FloatVec>& i_data_patches,
								  const device_patches<FloatVec>& i_labels, const Size& i_img_size,
								  rec_t i_type, const aid_params& i_params);

  private:
	//! A member computing the affine transformations from two sets of moments T.
	/*!
	 * \param i_lhs Moments T of a set of image patches.
	 * \param i_rhs Moments T of a set of image patches.
	 * \param i_patch_size Size of the image patches.
	 * \param i_solver The method for solving the overdetermined linear systems.
	 * \return Perspective transformations.
	 */
	template<typename FloatVec>
	device_patches<float> solve(const device_patches<FloatVec>& i_lhs,
								const device_patches<FloatVec>& i_rhs, const Size& i_patch_size,
								solver_t i_solver);

	//! A member computing the affine-invariant distance matrix between patches.
	/*!
	 * The input data has to lie in [0,1].
	 * \param i_patches0 Set of patches.
	 * \param i_T0 Matrix T for i_patches0.
	 * \param i_patches1 Set of patches.
	 * \param i_T1 Matrix T for i_patches1.
	 * \param i_solver The method for solving the overdetermined linear systems.
	 * \param i_type Interpolation method for perspective warping.
	 * results in clustering.
	 * \return Distance matrix.
	 */
	template<typename FloatVec, typename Float>
	device_matrix<double> distance_matrix(const device_patches<FloatVec>& i_patches0,
										  const device_patches<Float>& i_T0,
										  const device_patches<FloatVec>& i_patches1,
										  const device_patches<Float>& i_T1, solver_t i_solver,
										  interpolation_t i_type);

	unique_cublas_handle m_cublas{};
};

/*
 **
 ***
 **** Free functions, such as CUDA kernels.
 ***
 **
 */

//! Atomic add limited to thread blocks for compute capability 2.x and higher.
/*!
 * \param address Address of the value old. Computes (old + val) and stores the result back to
 * address.
 * \param val Floating point value.
 * \result old.
 */
inline __device__ float atomic_add_block(float* address, float val)
{
#if __CUDA_ARCH__ < 600 // Not actually limited to blocks.
	return atomicAdd(address, val);
#else
	return atomicAdd_block(address, val);
#endif
}

/*!
 * \overload
 */
inline __device__ double atomic_add_block(double* address, double val)
{
#if __CUDA_ARCH__ < 600 // Not actually limited to blocks.
	using I = unsigned long long int;
	I* address_as_ull = reinterpret_cast<I*>(address);
	I old = *address_as_ull, assumed;

	do
	{
		assumed = old;
		old = atomicCAS(address_as_ull, assumed,
						__double_as_longlong(val + __longlong_as_double(assumed)));
		// Note: uses integer comparison to avoid hang in case of NaN (since NaN != NaN)
	} while(assumed != old);

	return __longlong_as_double(old);
#else
	return atomicAdd_block(address, val);
#endif
}

//! Templated CUDA kernel to compute the matrix T from Hagege 2016.
/*!
 * blockDim: min(i_levels, patch_size) gridDim: patches
 * All data is expected to be and stored in column-major format.
 * \param i_patches Pointer to a set of patches. Is not allowed to overlap with o_T.
 * \param i_rows Number of rows of one patch of i_patches.
 * \param i_cols Number of columns of one patch of i_patches.
 * \param o_T Output matrix T. Is not allowed to overlap with i_patches.
 * \param i_levels The size of the function family.
 * \param i_high_order If true high-order moments are used, otherwise first-order moments.
 * If true the number o_T columns is 7, otherwise 3.
 * \tparam FuncFamily Non-linear functions. __device__ static Float compute(const Float& x, unsigned
 * int i, unsigned int max)
 * \tparam Float Data type of input/ output.
 */
template<typename FuncFamily, typename Float,
		 typename = std::enable_if<std::is_floating_point<Float>::value>>
__global__ void image_moments_kernel(const Float* __restrict__ i_patches, uint i_rows, uint i_cols,
									 Float* __restrict__ o_T, uint i_levels, bool i_high_order)
{
	const auto patch = blockIdx.x;
	const auto patch_size = i_rows * i_cols;
	const auto off_in = patch * patch_size;
	const auto off_out = [i_high_order, patch, i_levels] {
		if(i_high_order)
		{
			return patch * i_levels * TColsHigh;
		}
		else
		{
			return patch * i_levels * TColsFirst;
		}
	}();

	const auto cols_1 = Float{2.0} / static_cast<Float>(i_cols - 1);
	const auto rows_1 = Float{2.0} / static_cast<Float>(i_rows - 1);

	// Loop over all elements in a patch.
	for(uint i = threadIdx.x; i < patch_size; i += blockDim.x)
	{
		const auto val = i_patches[off_in + i];

		// coordinates scaled to [-1,1]
		const auto x = static_cast<Float>(i / i_rows) * cols_1 - Float{1.0};
		const auto y = static_cast<Float>(i % i_rows) * rows_1 - Float{1.0};

		// Loop over rows in the output.
		for(uint j = 0; j < i_levels; j++)
		{
			// Stride reduces the possibility, that two threads write to the same position
			// simultaneously. This greatly reduces the impact of atomic operations.
			const auto stride = (j + threadIdx.x) % i_levels;
			const auto odx = off_out + stride;
			const auto wi = FuncFamily::compute(val, stride, i_levels);
			const auto xwi = x * wi;
			const auto ywi = y * wi;

			atomic_add_block(o_T + odx, wi);
			atomic_add_block(o_T + (odx + i_levels), xwi);
			atomic_add_block(o_T + (odx + 2 * i_levels), ywi);

			if(i_high_order)
			{
				const auto xxwi = x * xwi;
				const auto xywi = x * ywi;
				const auto yywi = y * ywi;

				atomic_add_block(o_T + (odx + 3 * i_levels), xxwi);
				atomic_add_block(o_T + (odx + 4 * i_levels), xywi);
				atomic_add_block(o_T + (odx + 5 * i_levels), xywi);
				atomic_add_block(o_T + (odx + 6 * i_levels), yywi);
			}
		}
	}
}

//! Overload for vec3. Identical, except for 3 times more output rows.
//! Changes are commented.
/*!
 * \overload
 */
template<typename FuncFamily, typename Float>
__global__ void image_moments_kernel(const vec3<Float>* __restrict__ i_patches, uint i_rows,
									 uint i_cols, Float* __restrict__ o_T, uint i_levels,
									 bool i_high_order)
{
	const auto patch = blockIdx.x;
	const auto patch_size = i_rows * i_cols;
	const auto off_in = patch * patch_size;
	const auto rows_out = 3 * i_levels; // Changed in this overload!
	const auto off_out = [i_high_order, patch, rows_out] {
		if(i_high_order)
		{
			return patch * rows_out * TColsHigh;
		}
		else
		{
			return patch * rows_out * TColsFirst;
		}
	}();

	const auto cols_1 = Float{2.0} / static_cast<Float>(i_cols - 1);
	const auto rows_1 = Float{2.0} / static_cast<Float>(i_rows - 1);

	// Loop over all elements in a patch.
	for(uint i = threadIdx.x; i < patch_size; i += blockDim.x)
	{
		const auto val = i_patches[off_in + i];

		// coordinates scaled to [-1,1]
		const auto x = static_cast<Float>(i / i_rows) * cols_1 - Float{1.0};
		const auto y = static_cast<Float>(i % i_rows) * rows_1 - Float{1.0};

		// Loop over rows in the output.
		for(uint j = 0; j < i_levels; j++)
		{
			// Stride ensures that no two threads write to the same position simultaneously.
			const auto level = (j + threadIdx.x) % i_levels;
			const auto stride = 3 * (j + threadIdx.x) % rows_out;
			const auto odx = off_out + stride;
			const auto wi = FuncFamily::compute(val, level, i_levels);
			const auto xwi = x * wi;
			const auto ywi = y * wi;

			// Changed in this overload!
			atomic_add_block(o_T + odx, wi._1);
			atomic_add_block(o_T + (odx + 1), wi._2);
			atomic_add_block(o_T + (odx + 2), wi._3);
			atomic_add_block(o_T + (odx + rows_out), xwi._1);
			atomic_add_block(o_T + (odx + rows_out + 1), xwi._2);
			atomic_add_block(o_T + (odx + rows_out + 2), xwi._3);
			atomic_add_block(o_T + (odx + 2 * rows_out), ywi._1);
			atomic_add_block(o_T + (odx + 2 * rows_out + 1), ywi._2);
			atomic_add_block(o_T + (odx + 2 * rows_out + 2), ywi._3);

			if(i_high_order)
			{
				const auto xxwi = x * xwi;
				const auto xywi = x * ywi;
				const auto yywi = y * ywi;

				// Changed in this overload!
				atomic_add_block(o_T + (odx + 3 * rows_out), xxwi._1);
				atomic_add_block(o_T + (odx + 3 * rows_out + 1), xxwi._2);
				atomic_add_block(o_T + (odx + 3 * rows_out + 2), xxwi._3);

				atomic_add_block(o_T + (odx + 4 * rows_out), xywi._1);
				atomic_add_block(o_T + (odx + 4 * rows_out + 1), xywi._2);
				atomic_add_block(o_T + (odx + 4 * rows_out + 2), xywi._3);

				atomic_add_block(o_T + (odx + 5 * rows_out), xywi._1);
				atomic_add_block(o_T + (odx + 5 * rows_out + 1), xywi._2);
				atomic_add_block(o_T + (odx + 5 * rows_out + 2), xywi._3);

				atomic_add_block(o_T + (odx + 6 * rows_out), yywi._1);
				atomic_add_block(o_T + (odx + 6 * rows_out + 1), yywi._2);
				atomic_add_block(o_T + (odx + 6 * rows_out + 2), yywi._3);
			}
		}
	}
}

//! A function that computes the column space T of the UME (image moments).
/*!
 * \param i_patches Set of patches. For each the column space is computed.
 * \param i_ff The type of linearly independent functions.
 * \param i_levels The number of rows of the output.
 * \param i_high_order True if high order moments should be used otherwise false.
 * \return The column space T for each patch.
 */
template<typename FloatVec>
device_patches<remove_vec3_t<FloatVec>> image_moments(const device_patches<FloatVec>& i_patches,
													  func_family_t i_ff, uint i_levels,
													  bool i_high_order)
{
	// Casts are safe (same signedness, small values).
	const auto patches = gsl::narrow_cast<uint>(i_patches.patch_count());
	const auto cols = gsl::narrow_cast<uint>(i_patches.cols_patches());
	const auto rows = gsl::narrow_cast<uint>(i_patches.rows_patches());
	const auto patch_size = gsl::narrow_cast<uint>(i_patches.total_per_patch());
	const auto colsT = i_high_order ? TColsHigh : TColsFirst;
	const auto blockDim = dim3{std::min(i_levels, patch_size)};
	const auto gridDim = dim3{patches};
	auto T_matrix = [&] {
		if(std::is_same<FloatVec, float>::value || std::is_same<FloatVec, double>::value)
		{
			return device_patches<remove_vec3_t<FloatVec>>{patch_index{patches}, Rows{i_levels},
														   Cols{colsT}};
		}
		else // vec3<float>, vec3<double>
		{
			return device_patches<remove_vec3_t<FloatVec>>{patch_index{patches}, Rows{3 * i_levels},
														   Cols{colsT}};
		}
	}();

	if(i_ff == func_family_t::superlevelsets)
	{
		image_moments_kernel<superlevelsets><<<gridDim, blockDim>>>(
			i_patches.data().get(), rows, cols, T_matrix.data().get(), i_levels, i_high_order);
	}
	else if(i_ff == func_family_t::clip)
	{
		image_moments_kernel<clip><<<gridDim, blockDim>>>(
			i_patches.data().get(), rows, cols, T_matrix.data().get(), i_levels, i_high_order);
	}
	else
	{
		throw std::runtime_error{"Error in moments: function family type not supported."};
	};

	check(cudaDeviceSynchronize(), cudaSuccess);

	return T_matrix;
}

//! Templated CUDA kernel that computes one column of a distance matrix.
/*!
 * blockDim = 1, gridDim = f patches
 * The supplied memory is not allowed to overlap.
 * \param i_f Set of patches, which correspond to the rows of the distance matrix.
 * \param i_g_trans Set of patches, which is compared to i_f.
 * \param i_g Set of patches, which corresponds to a column of the distance matrix.
 * \param i_f_trans Set of patches, which is compared to i_g.
 * \param o_dist f*g distance matrix in column-major format.
 * \param i_patch_size Size of one patch.
 */
template<typename Metric, typename FloatVec>
__global__ void distance_matrix_impl_kernel(const FloatVec* __restrict__ i_f,
											const FloatVec* __restrict__ i_g_trans,
											const FloatVec* __restrict__ i_g,
											const FloatVec* __restrict__ i_f_trans,
											double* __restrict__ o_dist, uint i_patch_size)
{
	const auto off = blockIdx.x * i_patch_size;
	const auto val_f = Metric::compute(i_f + off, i_g_trans + off, i_patch_size);
	const auto val_g = Metric::compute(i_g, i_f_trans + off, i_patch_size);

	// A row contains the symmetrized distances from one element in f to all elements in g_trans.
	o_dist[blockIdx.x] = 0.5 * (val_f + val_g);
}

//! A function computing the symmetric distance between transformed patches.
/*!
 * \param i_f Set of patches, which correspond to the rows of the distance matrix.
 * \param i_g_trans Set of patches, which is compared to i_f.
 * \param i_g Set of patches, which corresponds to a column of the distance matrix.
 * \param i_f_trans Set of patches, which is compared to i_g.
 * \param o_dist_mat Initialized distance matrix which will contain the result.
 * \param i_col Column of the distance matrix to write to.
 */
template<typename Metric, typename FloatVec>
void distance_matrix_impl(const device_patches<FloatVec>& i_f,
						  const device_patches<FloatVec>& i_g_trans,
						  const device_patches<FloatVec>& i_g,
						  const device_patches<FloatVec>& i_f_trans,
						  device_matrix<double>& o_dist_mat, size_t i_col)
{
	Expects(i_f.size_patches() == i_g_trans.size_patches());
	Expects(i_g.size_patches() == i_f_trans.size_patches());
	Expects(i_f.size_patches() == i_g.size_patches());
	Expects(i_f.patch_count() == i_g_trans.patch_count());
	Expects(i_g_trans.patch_count() == i_f_trans.patch_count());
	Expects(o_dist_mat.rows() == i_f.patch_count());
	Expects(o_dist_mat.cols() == i_g.patch_count());

	const auto f_patches = gsl::narrow<uint>(i_f.patch_count());
	const auto patch_size = gsl::narrow<uint>(i_f.total_per_patch());
	const auto f_ptr = i_f.data().get();
	const auto g_trans_ptr = i_g_trans.data().get();
	const auto g_ptr = i_g.data().get() + i_col * patch_size;
	const auto f_trans_ptr = i_f_trans.data().get();
	auto out_ptr = o_dist_mat.data().get() + i_col * f_patches;

	distance_matrix_impl_kernel<Metric, FloatVec>
		<<<dim3{f_patches}, dim3{1}>>>(f_ptr, g_trans_ptr, g_ptr, f_trans_ptr, out_ptr, patch_size);
}

//! Templated CUDA kernel to tile a vector, i.e.,
//! [A,B,C] -> [A,B,C,A,B,C]
/*!
 * blockDim: input size gridDim: number of tiles shared mem: input size in bytes
 * Input/ ouput vectors are not allowed to overlap.
 * \param in Input vector of size size.
 * \param out Output vector of size size*tiles.
 * \param size Size of in.
 * \param tiles Number of output tiles.
 * \tparam Data type of input/ output.
 */
template<typename Float>
__global__ void tile_kernel(const Float* __restrict__ in, Float* __restrict__ out, size_t size,
							size_t tiles)
{
	extern __shared__ __align__(alignof(Float)) unsigned char smem[];
	Float* s = reinterpret_cast<Float*>(smem);

	if(threadIdx.x < size)
	{
		s[threadIdx.x] = in[threadIdx.x];
	}
	__syncthreads();

	size_t idx = threadIdx.x + blockDim.x * blockIdx.x;
	if(idx < size * tiles)
	{
		out[idx] = s[idx % size];
	}
}

//! Templated CUDA function to tile a vector, i.e.,
//! [A,B,C] -> [A,B,C,A,B,C]
/*!
 * \param first1 Beginning of the input vector.
 * \param last1 End of the input vector.
 * \param output Beginning of the allocated output of size tiles * size(input vector).
 * \param tiles Number of output tiles.
 */
template<typename InputIterator, typename OutputIterator>
void tile(InputIterator first1, InputIterator last1, OutputIterator output, size_t tiles)
{
	const auto input_size = static_cast<uint>(thrust::distance(first1, last1));
	const auto blockDim = dim3{1024};
	const auto gridDim = dim3{static_cast<uint>(tiles * input_size / 1024 + 1)};
	const auto smem = input_size * sizeof(typename std::iterator_traits<InputIterator>::value_type);

	tile_kernel<<<gridDim, blockDim, smem>>>(thrust::raw_pointer_cast(&first1[0]),
											 thrust::raw_pointer_cast(&output[0]), input_size,
											 tiles);

	check(cudaDeviceSynchronize(), cudaSuccess);
}

/*
 **
 ***
 **** Private members
 ***
 **
 */

//! See class sim_inv_dist for a description.
template<typename Float>
device_patches<float> affine_inv_dist::impl::solve(const device_patches<Float>& i_lhs,
												   const device_patches<Float>& i_rhs,
												   const Size& i_patch_size, solver_t i_solver)
{
	if(i_solver == solver_t::least_squares)
	{
		return least_squares_solver(i_lhs, i_rhs, i_patch_size, m_cublas.get());
	}
	else if(i_solver == solver_t::procrustes)
	{
		return procrustes_solver(i_lhs, i_rhs, i_patch_size, m_cublas.get());
	}
	else
	{
		return identity_solver(i_lhs.patch_count());
	}
}

template<typename FloatVec, typename Float>
device_matrix<double> affine_inv_dist::impl::distance_matrix(
	const device_patches<FloatVec>& i_patches0, const device_patches<Float>& i_T0,
	const device_patches<FloatVec>& i_patches1, const device_patches<Float>& i_T1,
	solver_t i_solver, interpolation_t i_type)
{
	// Solve Tf * X = det(A) * Tg and det(A) * Tg * X = Tf (least squares). A = affine transform.
	Expects(i_patches0.size_patches() == i_patches1.size_patches());
	Expects(i_T0.cols_patches() == i_T1.cols_patches());
	Expects(i_T0.rows_patches() == i_T1.rows_patches());
	Expects(i_T0.col_maj_patches());
	Expects(i_T1.col_maj_patches());

	const auto tiles = i_patches0.patch_count();
	const auto iterations = i_patches1.patch_count();
	const auto patch_size = i_patches0.size_patches();
	auto T1_tiled = device_patches<Float>(patch_index{tiles}, i_T1.size_patches());
	auto dist_mat = device_matrix<double>{Rows{tiles}, Cols{iterations}};

	// Each iteration solves all Tf for a fixed Tg. Hence, computes the distances for one column
	// in the matrix.
	for(size_t i = 0; i < iterations; i++)
	{
		// Make a copy of a fixed Tg for each Tf.
		tile(i_T1.cbegin(patch_index{i}), i_T1.cend(patch_index{i}), T1_tiled.begin(), tiles);
		const auto transforms = solve(i_T0, T1_tiled, patch_size, i_solver);
		const auto transforms_reverse = solve(T1_tiled, i_T0, patch_size, i_solver);

		const auto trans = warp_perspective(copy(i_patches1, i), transforms, i_type);
		const auto trans_reverse = warp_perspective(i_patches0, transforms_reverse, i_type);

		distance_matrix_impl<euclidean_metric>(i_patches0, trans, i_patches1, trans_reverse,
											   dist_mat, i);
	}

	check(cudaDeviceSynchronize(), cudaSuccess);

	return dist_mat;
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
	affine_inv_dist::impl::distance_matrix(const device_patches<FloatVec>& i_patches0,
										   const device_patches<FloatVec>& i_patches1,
										   const aid_params& i_params)
{
	const auto solver = i_params.solver;
	const auto ff = i_params.func_family;
	const auto levels = gsl::narrow<uint>(i_params.levels);
	const auto moments = i_params.higher_order_moments;
	const auto imed = i_params.imed;
	const auto interpolation = i_params.interpolation;

	const auto T0 = image_moments(i_patches0, ff, levels, moments);
	const auto T1 = image_moments(i_patches1, ff, levels, moments);

	return imed ? distance_matrix(imed_cft(i_patches0), T0, imed_cft(i_patches1), T1, solver,
								  interpolation)
				: distance_matrix(i_patches0, T0, i_patches1, T1, solver, interpolation);
}

template<typename FloatVec>
std::pair<device_patches<FloatVec>, std::vector<size_t>>
	affine_inv_dist::impl::greedy_k_center(const device_patches<FloatVec>& i_patches,
										   size_t i_clusters, std::size_t i_first,
										   const aid_params& i_params)
{
	Expects(i_clusters > 1);
	Expects(i_first < i_patches.patch_count());

	const auto solver = i_params.solver;
	const auto ff = i_params.func_family;
	const auto levels = gsl::narrow<uint>(i_params.levels);
	const auto moments = i_params.higher_order_moments;
	const auto imed = i_params.imed;
	const auto interpolation = i_params.interpolation;

	const auto T_patches = image_moments(i_patches, ff, levels, moments);
	const auto imed_patches = imed ? imed_cft(i_patches) : device_patches<FloatVec>{};
	auto dist =
		thrust::device_vector<double>(i_patches.patch_count(), std::numeric_limits<double>::max());

	auto ind = std::vector<size_t>(i_clusters);
	ind.at(0) = i_first;

	for(size_t i = 1; i < i_clusters; i++)
	{
		const auto idx = std::vector<size_t>{ind.at(i - 1)};
		const auto patch = copy(i_patches, idx);
		const auto T_patch = copy(T_patches, idx);
		const auto dist_mat =
			imed ? distance_matrix(imed_patches, T_patches, copy(imed_patches, idx), T_patch,
								   solver, interpolation)
				 : distance_matrix(i_patches, T_patches, patch, T_patch, solver, interpolation);

		thrust::transform(dist_mat.cbegin(), dist_mat.cend(), dist.cbegin(), dist.begin(),
						  thrust::minimum<double>{});
		const auto max = thrust::max_element(dist.cbegin(), dist.cend());
		ind.at(i) = thrust::distance(dist.cbegin(), max);
	}

	return std::make_pair(copy(i_patches, ind), std::move(ind));
}

template<typename FloatVec>
std::pair<device_matrix<FloatVec>, device_matrix<size_t>> affine_inv_dist::impl::reconstruct(
	const device_patches<FloatVec>& i_data_patches, const device_patches<FloatVec>& i_labels,
	const Size& i_img_size, rec_t i_type, const aid_params& i_params)
{
	Expects(i_data_patches.size_patches() == i_labels.size_patches());

	// Transformations for reconstruction and nearest neighbor labeling.
	// Use scoping to reduce memory footprint.
	auto patches_nn = [&] {
		const auto solver = i_params.solver;
		const auto ff = i_params.func_family;
		const auto levels = gsl::narrow<uint>(i_params.levels);
		const auto moments = i_params.higher_order_moments;
		const auto imed = i_params.imed;
		const auto interpolation = i_params.interpolation;

		const auto T_data = image_moments(i_data_patches, ff, levels, moments);
		const auto T_labels = image_moments(i_labels, ff, levels, moments);
		const auto dist_mat =
			imed ? distance_matrix(imed_cft(i_data_patches), T_data, imed_cft(i_labels), T_labels,
								   solver, interpolation)
				 : distance_matrix(i_data_patches, T_data, i_labels, T_labels, solver,
								   interpolation);

		// Since only patches with full support are used, the nearest neighbor labeling is smaller
		// than the image.
		const auto min = true;
		const auto nn_size = patch_count_size(i_img_size, i_labels.size_patches());
		const auto nn = nearest_neighbor(dist_mat, nn_size, min);
		const auto nn_vec = get_host_vector(nn);

		// Get the transformations for the nearest neighbor labels.
		const auto nn_T_labels = copy(T_labels, nn_vec); // Best label for each patch.
		const auto nn_transforms = solve(nn_T_labels, T_data, i_labels.size_patches(), solver);
		const auto nn_labels = copy(i_labels, nn_vec);

		return std::make_pair(warp_perspective(nn_labels, nn_transforms, interpolation), nn);
	}();

	return std::make_pair(rec_image(std::get<0>(patches_nn), i_img_size, i_type),
						  std::move(std::get<1>(patches_nn)));
}

template<typename FloatVec>
std::pair<device_matrix<FloatVec>, device_matrix<size_t>>
	affine_inv_dist::impl::reconstruct_w_translation(const device_patches<FloatVec>& i_data_patches,
													 const device_patches<FloatVec>& i_labels,
													 const Size& i_img_size, rec_t i_type,
													 const aid_params& i_params)
{
	Expects(i_data_patches.size_patches() == i_labels.size_patches());

	// Transformations for reconstruction and nearest neighbor labeling.
	// Use scoping to reduce memory footprint.
	auto patches_nn = [&] {
		const auto solver = i_params.solver;
		const auto ff = i_params.func_family;
		const auto levels = gsl::narrow<uint>(i_params.levels);
		const auto moments = i_params.higher_order_moments;
		const auto imed = i_params.imed;
		const auto interpolation = i_params.interpolation;

		const auto T_data = image_moments(i_data_patches, ff, levels, moments);
		const auto T_labels = image_moments(i_labels, ff, levels, moments);
		const auto dist_mat =
			imed ? distance_matrix(imed_cft(i_data_patches), T_data, imed_cft(i_labels), T_labels,
								   solver, interpolation)
				 : distance_matrix(i_data_patches, T_data, i_labels, T_labels, solver,
								   interpolation);

		// Since only patches with full support are used, the nearest neighbor labeling is smaller
		// than the image.
		const auto patch_size = i_labels.size_patches();
		const auto nn_size = patch_count_size(i_img_size, patch_size);
		const auto labeled = local_nearest_neighbor(dist_mat, nn_size, patch_size);

		// Get the transformations for the labeling.
		const auto nn_T_labels = copy(T_labels, get_host_vector(labeled.labels));
		const auto nn_T_patches = copy(T_data, get_host_vector(labeled.patches));
		const auto nn_transforms = solve(nn_T_labels, nn_T_patches, patch_size, solver);
		const auto nn_labels = copy(i_labels, get_host_vector(labeled.labels));

		// Warp and translate the patches.
		const auto warped = warp_perspective(nn_labels, nn_transforms, interpolation);
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