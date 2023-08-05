#include "../include/sim_inv_dist.h"
#include "../src/sim_inv_dist_impl.h"

#include <array>
#include <utility>

device_matrix<double> sim_inv_dist::distance_matrix(const device_patches<float>& i_patches0,
													const device_patches<float>& i_patches1,
													const sid_params& i_params)
{
	return pimpl->distance_matrix(i_patches0, i_patches1, i_params);
}

device_matrix<double> sim_inv_dist::distance_matrix(const device_patches<double>& i_patches0,
													const device_patches<double>& i_patches1,
													const sid_params& i_params)
{
	return pimpl->distance_matrix(i_patches0, i_patches1, i_params);
}

device_matrix<double> sim_inv_dist::distance_matrix(const device_patches<vec3<float>>& i_patches0,
													const device_patches<vec3<float>>& i_patches1,
													const sid_params& i_params)
{
	return pimpl->distance_matrix(i_patches0, i_patches1, i_params);
}

device_matrix<double> sim_inv_dist::distance_matrix(const device_patches<vec3<double>>& i_patches0,
													const device_patches<vec3<double>>& i_patches1,
													const sid_params& i_params)
{
	return pimpl->distance_matrix(i_patches0, i_patches1, i_params);
}

std::pair<device_patches<float>, std::vector<size_t>>
	sim_inv_dist::greedy_k_center(const device_patches<float>& i_patches, size_t i_clusters,
								  size_t i_first, const sid_params& i_params)
{
	return pimpl->greedy_k_center(i_patches, i_clusters, i_first, i_params);
}

std::pair<device_patches<double>, std::vector<size_t>>
	sim_inv_dist::greedy_k_center(const device_patches<double>& i_patches, size_t i_clusters,
								  size_t i_first, const sid_params& i_params)
{
	return pimpl->greedy_k_center(i_patches, i_clusters, i_first, i_params);
}

std::pair<device_patches<vec3<float>>, std::vector<size_t>>
	sim_inv_dist::greedy_k_center(const device_patches<vec3<float>>& i_patches, size_t i_clusters,
								  size_t i_first, const sid_params& i_params)
{
	return pimpl->greedy_k_center(i_patches, i_clusters, i_first, i_params);
}

std::pair<device_patches<vec3<double>>, std::vector<size_t>>
	sim_inv_dist::greedy_k_center(const device_patches<vec3<double>>& i_patches, size_t i_clusters,
								  size_t i_first, const sid_params& i_params)
{
	return pimpl->greedy_k_center(i_patches, i_clusters, i_first, i_params);
}

std::pair<device_matrix<float>, device_matrix<size_t>>
	sim_inv_dist::reconstruct(const device_patches<float>& i_data_patches,
							  const device_patches<float>& i_labels, const Size& i_img_size,
							  rec_t i_type, const sid_params& i_params,
							  interpolation_t i_interpolation)
{
	return pimpl->reconstruct(i_data_patches, i_labels, i_img_size, i_type, i_params,
							  i_interpolation);
}

std::pair<device_matrix<double>, device_matrix<size_t>>
	sim_inv_dist::reconstruct(const device_patches<double>& i_data_patches,
							  const device_patches<double>& i_labels, const Size& i_img_size,
							  rec_t i_type, const sid_params& i_params,
							  interpolation_t i_interpolation)
{
	return pimpl->reconstruct(i_data_patches, i_labels, i_img_size, i_type, i_params,
							  i_interpolation);
}

std::pair<device_matrix<vec3<float>>, device_matrix<size_t>>
	sim_inv_dist::reconstruct(const device_patches<vec3<float>>& i_data_patches,
							  const device_patches<vec3<float>>& i_labels, const Size& i_img_size,
							  rec_t i_type, const sid_params& i_params,
							  interpolation_t i_interpolation)
{
	return pimpl->reconstruct(i_data_patches, i_labels, i_img_size, i_type, i_params,
							  i_interpolation);
}

std::pair<device_matrix<vec3<double>>, device_matrix<size_t>>
	sim_inv_dist::reconstruct(const device_patches<vec3<double>>& i_data_patches,
							  const device_patches<vec3<double>>& i_labels, const Size& i_img_size,
							  rec_t i_type, const sid_params& i_params,
							  interpolation_t i_interpolation)
{
	return pimpl->reconstruct(i_data_patches, i_labels, i_img_size, i_type, i_params,
							  i_interpolation);
}

std::pair<device_matrix<float>, device_matrix<size_t>> sim_inv_dist::reconstruct_w_translation(
	const device_patches<float>& i_data_patches, const device_patches<float>& i_labels,
	const Size& i_img_size, rec_t i_type, const sid_params& i_params,
	interpolation_t i_interpolation)
{
	return pimpl->reconstruct_w_translation(i_data_patches, i_labels, i_img_size, i_type, i_params,
											i_interpolation);
}

std::pair<device_matrix<double>, device_matrix<size_t>> sim_inv_dist::reconstruct_w_translation(
	const device_patches<double>& i_data_patches, const device_patches<double>& i_labels,
	const Size& i_img_size, rec_t i_type, const sid_params& i_params,
	interpolation_t i_interpolation)
{
	return pimpl->reconstruct_w_translation(i_data_patches, i_labels, i_img_size, i_type, i_params,
											i_interpolation);
}

std::pair<device_matrix<vec3<float>>, device_matrix<size_t>>
	sim_inv_dist::reconstruct_w_translation(const device_patches<vec3<float>>& i_data_patches,
											const device_patches<vec3<float>>& i_labels,
											const Size& i_img_size, rec_t i_type,
											const sid_params& i_params,
											interpolation_t i_interpolation)
{
	return pimpl->reconstruct_w_translation(i_data_patches, i_labels, i_img_size, i_type, i_params,
											i_interpolation);
}

std::pair<device_matrix<vec3<double>>, device_matrix<size_t>>
	sim_inv_dist::reconstruct_w_translation(const device_patches<vec3<double>>& i_data_patches,
											const device_patches<vec3<double>>& i_labels,
											const Size& i_img_size, rec_t i_type,
											const sid_params& i_params,
											interpolation_t i_interpolation)
{
	return pimpl->reconstruct_w_translation(i_data_patches, i_labels, i_img_size, i_type, i_params,
											i_interpolation);
}

device_patches<float>
	sim_inv_dist::perspective_transformations(const device_patches<float>& i_data_patches,
											  const device_patches<float>& i_labels,
											  const sid_params& i_params)
{
	return pimpl->perspective_transformations(i_data_patches, i_labels, i_params);
}

device_patches<float>
	sim_inv_dist::perspective_transformations(const device_patches<double>& i_data_patches,
											  const device_patches<double>& i_labels,
											  const sid_params& i_params)
{
	return pimpl->perspective_transformations(i_data_patches, i_labels, i_params);
}

device_patches<float>
	sim_inv_dist::perspective_transformations(const device_patches<vec3<float>>& i_data_patches,
											  const device_patches<vec3<float>>& i_labels,
											  const sid_params& i_params)
{
	return pimpl->perspective_transformations(i_data_patches, i_labels, i_params);
}

device_patches<float>
	sim_inv_dist::perspective_transformations(const device_patches<vec3<double>>& i_data_patches,
											  const device_patches<vec3<double>>& i_labels,
											  const sid_params& i_params)
{
	return pimpl->perspective_transformations(i_data_patches, i_labels, i_params);
}

device_patches<cuComplex> sim_inv_dist::afmt(const device_patches<float>& i_patches, float i_sigma)
{
	return pimpl->afmt(i_patches, i_sigma);
}

device_patches<cuDoubleComplex> sim_inv_dist::afmt(const device_patches<double>& i_patches,
												   float i_sigma)
{
	return pimpl->afmt(i_patches, i_sigma);
}

device_patches<vec3<cuComplex>> sim_inv_dist::afmt(const device_patches<vec3<float>>& i_patches,
												   float i_sigma)
{
	return pimpl->afmt(i_patches, i_sigma);
}

device_patches<vec3<cuDoubleComplex>>
	sim_inv_dist::afmt(const device_patches<vec3<double>>& i_patches, float i_sigma)
{
	return pimpl->afmt(i_patches, i_sigma);
}

/*
**
*** sim_inv_dist::impl
**
*/

//! Initializes cuff plan and returns fft output size.
/*!
 * cuFTT data layout
 * input[b * idist + (x * inembed[1] + y) * istride]
 * output[b * odist + (x * onembed[1] + y) * ostride]
 * \param i_M Input dimension of fft. (Square input expected.)
 * \param i_patch_count Batch number of the fft.
 * \param i_single If true single precision, otherwise double precision.
 * \o_stride Stride of the out memory elements. (For the input 1 is expected.)
 */
Size sim_inv_dist::impl::init(size_t i_M, size_t i_patch_count, bool i_single, size_t o_stride)
{
	Expects(i_M > 0);
	Expects(i_patch_count > 0);

	// Cufft stores n/2 + 1 elements in the columns.
	const auto int_M = gsl::narrow<int>(i_M);
	const auto int_N = gsl::narrow<int>(i_M);
	const auto ostride = gsl::narrow<int>(o_stride);
	const auto int_pc = gsl::narrow<int>(i_patch_count);

	if(i_M != m_M || i_patch_count != m_patch_count || i_single != m_single)
	{
		// TODO: Is it necessary to get a new plan?
		m_plan.reset();

		// fft dimension
		// cave: contiguous dimension last
		auto N = std::array<int, 2>{int_M, int_N};
		const auto batch = int_pc;

		// storage dimension input
		auto inembed = std::array<int, 2>{int_N, int_M};
		const auto istride = 1;
		const auto idist = int_M * int_N;

		// storage dimension output
		// Cufft computes only the unique coefficients.
		auto onembed = std::array<int, 2>{int_M, int_N / 2 + 1};
		const auto odist = ostride * (int_N / 2 + 1) * (int_M);

		const auto type = i_single ? CUFFT_R2C : CUFFT_D2Z;

		constexpr auto Rank = 2;
		auto worksize = size_t{}; // unused
		check(cufftMakePlanMany(m_plan.get(), Rank, N.data(), inembed.data(), istride, idist,
								onembed.data(), ostride, odist, type, batch, &worksize),
			  CUFFT_SUCCESS);

		m_M = i_M;
		m_patch_count = i_patch_count;
		m_single = i_single;
	}

	// Cufft computes only the unique coefficients.
	return Size{Rows{int_N / 2 + 1}, Cols{int_M}};
}

// Synchronization is done with scaleafmt().
inline void cufftExec(cufftHandle plan, cufftReal* idata, cuComplex* odata)
{
	check_cufft(cufftExecR2C(plan, idata, odata));
}

// Synchronization is done with scaleafmt().
inline void cufftExec(cufftHandle plan, cufftDoubleReal* idata, cuDoubleComplex* odata)
{
	check_cufft(cufftExecD2Z(plan, idata, odata));
}

// The struct is needed since __device__ lambdas are not supported in private members.
template<typename Float>
struct afmt_func_struct_1D final
{
  public:
	//! Constructor.
	/*!
	 * \param i_ptr Log-polar transformed patches (transposed! and continuous).
	 * \param o_ptr Output patches of the same size, read for the fft (continuous).
	 * \param i_rows Rows per patch.
	 * \param i_cols Columns per patches.
	 * \param i_sigma Sigma parameter from afmt.
	 */
	afmt_func_struct_1D(const Float* i_ptr, Float* o_ptr, size_t i_rows, size_t i_cols,
						float i_sigma) noexcept
		: in_ptr{i_ptr}, out_ptr{o_ptr}, sigma{i_sigma}, patches_size{i_rows * i_cols},
		  rows{i_rows}, rowsT{static_cast<float>(i_rows)}, colsT{static_cast<float>(i_cols)}
	{
	}

	//! Use the fft symmetry to put the origin in the frequency space in the center of the fft
	//! output  and multiply afmt related constants.
	/*!
	 * \param el Index of the input element from 0 to size of patches * number of patches.
	 */
	__device__ void operator()(std::size_t el) const noexcept
	{
		// Cave: The log polar image is expected to be transposed!
		const auto el_patch = el % patches_size;
		const auto m = static_cast<float>(el_patch % rows);
		const auto n = static_cast<float>(el_patch / rows);

		out_ptr[el] =
			TwoPi / rowsT * exp(TwoPi * sigma * n / colsT) * pow(-1.0f, n + m) * in_ptr[el];
	}

  private:
	const Float* in_ptr;
	Float* out_ptr;
	float sigma;
	size_t patches_size;
	size_t rows;
	float rowsT;
	float colsT;
};

// The struct is needed since __device__ lambdas are not supported in private members.
template<typename Float>
struct afmt_func_struct_3D final
{
  public:
	//! Constructor.
	/*!
	 * \param i_ptr Log-polar transformed patches (transposed! and continuous).
	 * \param o_ptr0 Output patches of the first channel of the same size, read for the fft
	 * (continuous).
	 * \param o_ptr1 Output patches of the second channel of the same size, read for the fft
	 * (continuous).
	 * \param o_ptr2 Output patches of the third channel of the same size, read for the fft
	 * (continuous).
	 * \param i_rows Rows per patch.
	 * \param i_cols Columns per patches.
	 * \param i_sigma Sigma parameter from afmt.
	 */
	afmt_func_struct_3D(const vec3<Float>* i_ptr, Float* o_ptr0, Float* o_ptr1, Float* o_ptr2,
						size_t i_rows, size_t i_cols, float i_sigma) noexcept
		: in_ptr{i_ptr}, out_ptr0{o_ptr0}, out_ptr1{o_ptr1}, out_ptr2{o_ptr2}, sigma{i_sigma},
		  patches_size{i_rows * i_cols}, rows{i_rows}, rowsT{static_cast<float>(i_rows)},
		  colsT{static_cast<float>(i_cols)}
	{
	}

	//! Use the fft symmetry to put the origin in the frequency space in the center of the fft
	//! output  and multiply afmt related constants.
	/*!
	 * \param el Index of the input element from 0 to size of patches * number of patches.
	 */
	__device__ void operator()(std::size_t el) const noexcept
	{
		// Cave: The log polar image is expected to be transposed!
		const auto el_patch = el % patches_size;
		const auto m = static_cast<float>(el_patch % rows);
		const auto n = static_cast<float>(el_patch / rows);

		const auto res =
			TwoPi / rowsT * exp(TwoPi * sigma * n / colsT) * pow(-1.0f, n + m) * in_ptr[el];
		out_ptr0[el] = res._1;
		out_ptr1[el] = res._2;
		out_ptr2[el] = res._3;
	}

  private:
	const vec3<Float>* in_ptr;
	Float* out_ptr0;
	Float* out_ptr1;
	Float* out_ptr2;
	float sigma;
	size_t patches_size;
	size_t rows;
	float rowsT;
	float colsT;
};

//! A function that pre-processes image patches to reduce the analytic Fourier-Mellin
//! transformation to a fast Fourier transform (FFT).
/*!
 * \param i_patches Image patches.
 * \param i_sigma Fourier-Mellin-Coefficient.
 * \return Pre-processed images.
 */
template<typename Float>
device_patches<Float> pre_fft(const device_patches<Float>& i_patches, float i_sigma)
{
	Expects(i_patches.col_maj_patches());
	Expects(i_patches.rows_patches() % 2 == 0); // Necessary for shift to center frequency.
	Expects(i_patches.rows_patches() == i_patches.cols_patches());
	// Rows == Cols: Necessary for fft, since the patches need to be transposed.

	// Shift the zero frequency to the center and multiply afmt related constants.
	const auto in_ptr = i_patches.data().get();
	const auto K = i_patches.rows_patches();
	const auto V = i_patches.cols_patches();
	const auto patches_size = i_patches.total_per_patch();
	const auto patches_rows = i_patches.rows_patches();
	const auto patches_first = thrust::counting_iterator<std::size_t>{0};
	const auto patches_last = thrust::counting_iterator<std::size_t>{i_patches.total()};

	const auto pc = patch_index{i_patches.patch_count()};
	const auto size = i_patches.size_patches();
	auto out = device_patches<Float>{pc, size};
	auto out_ptr = out.data().get();

	thrust::for_each(patches_first, patches_last,
					 afmt_func_struct_1D<Float>{in_ptr, out_ptr, K, V, i_sigma});

	return out;
}

/*!
 * \overlaod
 */
template<typename Float>
std::array<device_patches<Float>, 3> pre_fft(const device_patches<vec3<Float>>& i_patches,
											 float i_sigma)
{
	Expects(i_patches.col_maj_patches());
	Expects(i_patches.rows_patches() % 2 == 0); // Necessary for shift to center frequency.
	Expects(i_patches.rows_patches() == i_patches.cols_patches());
	// Rows == Cols: Necessary for fft, since the patches need to be transposed.

	// Shift the zero frequency to the center and multiply afmt related constants.
	const auto in_ptr = i_patches.data().get();
	const auto K = i_patches.rows_patches();
	const auto V = i_patches.cols_patches();
	const auto patches_size = i_patches.total_per_patch();
	const auto patches_rows = i_patches.rows_patches();
	const auto patches_first = thrust::counting_iterator<std::size_t>{0};
	const auto patches_last = thrust::counting_iterator<std::size_t>{i_patches.total()};

	using T = device_patches<Float>;
	const auto pc = patch_index{i_patches.patch_count()};
	const auto size = i_patches.size_patches();
	auto out = std::array<T, 3>{T{pc, size}, T{pc, size}, T{pc, size}};
	auto out0 = out[0].data().get();
	auto out1 = out[1].data().get();
	auto out2 = out[2].data().get();

	thrust::for_each(patches_first, patches_last,
					 afmt_func_struct_3D<Float>{in_ptr, out0, out1, out2, K, V, i_sigma});

	return out;
}

device_patches<cuComplex> sim_inv_dist::impl::afmt(const device_patches<float>& i_patches,
												   float i_sigma)
{
	auto pre_patches = pre_fft(i_patches, i_sigma);

	const auto single_prec = true;
	const auto pc = pre_patches.patch_count();
	const auto o_stride = 1;
	auto afmts_size = init(pre_patches.rows_patches(), pc, single_prec, o_stride);
	auto afmts = device_patches<cuComplex>{patch_index{pc}, afmts_size};

	cufftExec(m_plan.get(), pre_patches.data().get(), afmts.data().get());
	check(cudaDeviceSynchronize(), cudaSuccess);

	return afmts;
}

device_patches<cuDoubleComplex> sim_inv_dist::impl::afmt(const device_patches<double>& i_patches,
														 float i_sigma)
{
	auto pre_patches = pre_fft(i_patches, i_sigma);

	const auto double_prec = false;
	const auto pc = pre_patches.patch_count();
	const auto o_stride = 1;
	auto afmts_size = init(pre_patches.rows_patches(), pc, double_prec, o_stride);
	auto afmts = device_patches<cuDoubleComplex>{patch_index{pc}, afmts_size};

	cufftExec(m_plan.get(), pre_patches.data().get(), afmts.data().get());
	check(cudaDeviceSynchronize(), cudaSuccess);

	return afmts;
}

device_patches<vec3<cuComplex>>
	sim_inv_dist::impl::afmt(const device_patches<vec3<float>>& i_patches, float i_sigma)
{
	// Due to alignment(?), the input data has to be copied first; the output need not be copied.
	auto pre_patches = pre_fft(i_patches, i_sigma);
	const auto single_prec = true;
	const auto pc = i_patches.patch_count();
	const auto o_stride = 3;
	const auto afmts_size = init(i_patches.rows_patches(), pc, single_prec, o_stride);

	auto out = device_patches<vec3<cuComplex>>{patch_index{pc}, afmts_size};
	auto out_ptr = reinterpret_cast<cuComplex*>(out.data().get());

	cufftExec(m_plan.get(), pre_patches[0].data().get(), out_ptr);
	cufftExec(m_plan.get(), pre_patches[1].data().get(), out_ptr + 1);
	cufftExec(m_plan.get(), pre_patches[2].data().get(), out_ptr + 2);
	check(cudaDeviceSynchronize(), cudaSuccess);

	return out;
}

device_patches<vec3<cuDoubleComplex>>
	sim_inv_dist::impl::afmt(const device_patches<vec3<double>>& i_patches, float i_sigma)
{
	// Due to alignment(?), the input data has to be copied first; the output need not be copied.
	auto pre_patches = pre_fft(i_patches, i_sigma);
	const auto double_prec = false;
	const auto pc = i_patches.patch_count();
	const auto o_stride = 3;
	const auto afmts_size = init(i_patches.rows_patches(), pc, double_prec, o_stride);

	auto out = device_patches<vec3<cuDoubleComplex>>{patch_index{pc}, afmts_size};
	auto out_ptr = reinterpret_cast<cuDoubleComplex*>(out.data().get());

	cufftExec(m_plan.get(), pre_patches[0].data().get(), out_ptr);
	cufftExec(m_plan.get(), pre_patches[1].data().get(), out_ptr + 1);
	cufftExec(m_plan.get(), pre_patches[2].data().get(), out_ptr + 2);
	check(cudaDeviceSynchronize(), cudaSuccess);

	return out;
}