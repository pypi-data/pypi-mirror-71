#include "../include/determinant.h"
#include "../include/device_patches.h"
#include "../include/least_squares_solver.h"
#include "../include/unique_cublas_handle.h"
#include "../include/utils.h"
#include "../include/warp_perspective.h"

#include "../extern/gsl/gsl_assert"
#include "../extern/gsl/gsl_util"

#include <cublas_v2.h>
#include <cuda_runtime.h>
#include <thrust/device_vector.h>
#include <thrust/iterator/counting_iterator.h>
#include <thrust/transform.h>

using uint = unsigned int;

inline __device__ float my_quiet_nan()
{
	return __int_as_float(0x7fffffff);
}

/*
 * Thin wrappers for cublas functions.
 */

void gels(cublasHandle_t handle, cublasOperation_t trans, int m, int n, int nrhs, float* Aarray[],
		  int lda, float* Carray[], int ldc, int batchSize)
{
	auto info = int{1};
	check_cublas(cublasSgelsBatched(handle, trans, m, n, nrhs, Aarray, lda, Carray, ldc, &info,
									nullptr, batchSize));
	check(cudaDeviceSynchronize(), cudaSuccess);

	Ensures(info == 0);
}

void gels(cublasHandle_t handle, cublasOperation_t trans, int m, int n, int nrhs, double* Aarray[],
		  int lda, double* Carray[], int ldc, int batchSize)
{
	auto info = int{1};
	check_cublas(cublasDgelsBatched(handle, trans, m, n, nrhs, Aarray, lda, Carray, ldc, &info,
									nullptr, batchSize));
	check(cudaDeviceSynchronize(), cudaSuccess);

	Ensures(info == 0);
}

//! Least squares for overdetermined systems, A * X = B.
/*!
 * \param lhs Matrix A.
 * \param rhs Matrix B.
 * \param handle Initialized cublas handle.
 * \return Matrix X.
 */
template<typename Float>
device_patches<Float> least_squares(const device_patches<Float>& lhs,
									const device_patches<Float>& rhs, cublasHandle_t handle)
{
	Expects(lhs.col_maj_patches());
	Expects(rhs.col_maj_patches());
	Expects(lhs.rows_patches() == rhs.rows_patches());
	Expects(lhs.rows_patches() >= lhs.cols_patches());
	Expects(rhs.rows_patches() >= rhs.cols_patches());

	// The casts are safe, since the dimensions are small enough.
	const auto m = gsl::narrow_cast<int>(lhs.rows_patches());
	const auto n = gsl::narrow_cast<int>(lhs.cols_patches());
	const auto nrhs = gsl::narrow_cast<int>(rhs.cols_patches());
	const auto lda = gsl::narrow_cast<int>(lhs.ld_patches());
	const auto ldc = gsl::narrow_cast<int>(rhs.ld_patches());
	const auto batchSize = gsl::narrow_cast<int>(lhs.patch_count());

	// Solutions will overwrite inputs.
	auto _lhs = lhs;
	auto _rhs = rhs;
	const auto _lhs_ptr = _lhs.data().get();
	const auto _rhs_ptr = _rhs.data().get();
	const auto lhs_stride = lhs.ld();
	const auto rhs_stride = rhs.ld();

	// Gels needs device array of device pointer to each patch.
	auto _lhs_ptr_vec = thrust::device_vector<Float*>(batchSize);
	auto _rhs_ptr_vec = thrust::device_vector<Float*>(batchSize);

	const auto begin = thrust::make_counting_iterator<size_t>(0);
	const auto end = thrust::make_counting_iterator<size_t>(batchSize);

	thrust::transform(
		begin, end, _lhs_ptr_vec.begin(),
		[_lhs_ptr, lhs_stride] __device__(size_t pos) { return _lhs_ptr + pos * lhs_stride; });
	thrust::transform(
		begin, end, _rhs_ptr_vec.begin(),
		[_rhs_ptr, rhs_stride] __device__(size_t pos) { return _rhs_ptr + pos * rhs_stride; });

	gels(handle, CUBLAS_OP_N, m, n, nrhs, _lhs_ptr_vec.data().get(), lda, _rhs_ptr_vec.data().get(),
		 ldc, batchSize);

	return _rhs;
}

//! Templated CUDA kernel that extracts the affine transformation from the least squares solution
//! of least_squares.
/*!
 * blockDim: 1, gridDim: patch count
 * \param i_Dt Solved linear systems from least squares.
 * The solution starts in the second column
 * D^t = [A^t | b^t]. i_Dt is not allowed to overlap with o_transform.
 * \param i_det Determimants (inverse) of i_Dt.
 * \param o_transform Extracted affine transformation (2x3) that is compatible with column-major
 * images and nppi -> [A^t | (-b2, -b1)^t] because of the identity Ax + b = A^t * x^t + (-b2, -b1).
 * o_transform is not allowed to overlap with i_Dt.
 * \param i_ld_patches The rows/ stride of i_Dt.
 * \param i_ld The stride between patches of i_Dt.
 * \param i_patch_size Size of the image patches.
 */
template<typename Float>
__global__ void least_squares_transforms_kernel(const Float* __restrict__ i_Dt,
												const Float* __restrict__ i_det,
												float* __restrict__ o_transform, uint i_ld_patches,
												uint i_ld, Size i_patch_size)
{
	// Skipping first column. This is the unit vector.
	const auto off_i1 = blockIdx.x * i_ld + i_ld_patches;
	const auto off_i2 = blockIdx.x * i_ld + 2 * i_ld_patches;
	const auto off_o = blockIdx.x * 3 * 3; // Size of projective transformations: 3x3.

	// The input transformation applies to the coordinate system scaled to [-1,1].
	// D^t = [A^t | b^t
	const auto d = i_det[blockIdx.x];
	const auto a_11 = static_cast<float>(d * i_Dt[off_i1 + 1]);
	const auto a_12 = static_cast<float>(d * i_Dt[off_i1 + 2]);
	const auto a_21 = static_cast<float>(d * i_Dt[off_i2 + 1]);
	const auto a_22 = static_cast<float>(d * i_Dt[off_i2 + 2]);
	const auto b_1 = static_cast<float>(d * i_Dt[off_i1]);
	const auto b_2 = static_cast<float>(d * i_Dt[off_i2]);

	const auto det = a_11 * a_22 - a_12 * a_21;

	// Only allow reasonable matrices (up to rounding errors).
	if(abs(det) > 0.01f && abs(det) < 10.0f)
	{
		perspective_matrix(a_11, a_12, b_1, a_21, a_22, b_2, i_patch_size, o_transform + off_o);
	}
	else // Identity
	{
		perspective_matrix(1.0f, 0.0f, 0.0f, 0.0f, 1.0f, 0.0f, i_patch_size, o_transform + off_o);
	}
}

//! Templated function that extracts the affine transformation from the least squares solution
//! of least_squares.
/*!
 * \param sol Solution from least_squares().
 * \param det Determinants (inverse) of the affine transformation.
 * \param size_patches Size of the image patches, corresponding to the transformations.
 * \param batch_no Determines the memory position of the stored transformations.
 * \return Perspective transformations.
 */
template<typename Float>
device_patches<float> least_squares_transforms(const device_patches<Float>& sol,
											   const thrust::device_vector<Float>& det,
											   const Size& size_patches)
{
	Expects(sol.patch_count() == det.size());

	const auto row_maj = false;
	auto transformations =
		device_patches<float>{patch_index{sol.patch_count()}, 3_rows, 3_cols, row_maj};

	const auto ld_patches = gsl::narrow_cast<uint>(sol.ld_patches());
	const auto ld = gsl::narrow_cast<uint>(sol.ld());
	const auto sol_ptr = sol.data().get();
	const auto det_ptr = det.data().get();
	auto trans_ptr = transformations.data().get();

	const auto blockDim = dim3{1};
	const auto gridDim = dim3{gsl::narrow_cast<uint>(sol.patch_count())};

	least_squares_transforms_kernel<<<gridDim, blockDim>>>(sol_ptr, det_ptr, trans_ptr, ld_patches,
														   ld, size_patches);
	check(cudaDeviceSynchronize(), cudaSuccess);

	return transformations;
}

//! Least squares for image moments.
/*!
 * \param lhs Image moments.
 * \param rhs Image moments.
 * \param patch_size Patch size associated to the affine transformations.
 * \param cublas_h Initialized cublas handle.
 * \return Affine transformations associated to the image moments.
 */
template<typename Float>
device_patches<float> least_squares_solver_impl(const device_patches<Float>& lhs,
												const device_patches<Float>& rhs,
												const Size& patch_size, cublasHandle_t cublas_h)
{
	const auto solutions = least_squares(lhs, rhs, cublas_h);
	const auto dets = determinant(lhs, rhs);

	return least_squares_transforms(solutions, dets, patch_size);
}

device_patches<float> least_squares_solver(const device_patches<float>& lhs,
										   const device_patches<float>& rhs, const Size& patch_size,
										   cublasHandle_t handle)
{
	return least_squares_solver_impl(lhs, rhs, patch_size, handle);
}

device_patches<float> least_squares_solver(const device_patches<double>& lhs,
										   const device_patches<double>& rhs,
										   const Size& patch_size, cublasHandle_t handle)
{
	return least_squares_solver_impl(lhs, rhs, patch_size, handle);
}