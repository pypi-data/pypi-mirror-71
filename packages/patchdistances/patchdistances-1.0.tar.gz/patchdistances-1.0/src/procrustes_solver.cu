#include "../include/device_patches.h"
#include "../include/procrustes_solver.h"
#include "../include/unique_cublas_handle.h"
#include "../include/utils.h"
#include "../include/warp_perspective.h"

#include "../extern/gsl/gsl_assert"
#include "../extern/gsl/gsl_util"

#include <cublas_v2.h>
#include <cuda_runtime.h>
#include <thrust/device_vector.h>
#include <thrust/for_each.h>
#include <thrust/iterator/counting_iterator.h>

#include <utility>
#include <vector>

using uint = unsigned int;
using lli = long long int;
// using namespace impl;

/*
 * Thin wrappers for cublas functions.
 */

void gemm(cublasHandle_t handle, cublasOperation_t transa, cublasOperation_t transb, int m, int n,
		  int k, const float* alpha, const float* Aarray[], int lda, const float* Barray[], int ldb,
		  const float* beta, float* Carray[], int ldc, int batchCount)
{
	check_cublas(cublasSgemmBatched(handle, transa, transb, m, n, k, alpha, Aarray, lda, Barray,
									ldb, beta, Carray, ldc, batchCount));
	check(cudaDeviceSynchronize(), cudaSuccess);
}

void gemm(cublasHandle_t handle, cublasOperation_t transa, cublasOperation_t transb, int m, int n,
		  int k, const double* alpha, const double* Aarray[], int lda, const double* Barray[],
		  int ldb, const double* beta, double* Carray[], int ldc, int batchCount)
{
	check_cublas(cublasDgemmBatched(handle, transa, transb, m, n, k, alpha, Aarray, lda, Barray,
									ldb, beta, Carray, ldc, batchCount));
	check(cudaDeviceSynchronize(), cudaSuccess);
}

//! Matrix multiplication for patches.
/*!
 * \param i_alpha Scalar factor.
 * \param i_transA W/o transposing A.
 * \param i_A Patches.
 * \param i_transB W/o transposing B.
 * \param i_B Patches.
 * \param i_h Initialized cublas handle.
 * \return alpha * A[i] * B[i] + beta * C[i], where i denotes a patch.
 */
template<typename Float>
device_patches<Float> mat_mul(Float i_alpha, cublasOperation_t i_transA,
							  const device_patches<Float>& i_A, cublasOperation_t i_transB,
							  const device_patches<Float>& i_B, cublasHandle_t i_h)
{
	Expects(i_A.col_maj_patches());
	Expects(i_B.col_maj_patches());
	Expects(i_A.patch_count() == i_B.patch_count());

	const auto rows_A = i_transA == CUBLAS_OP_N ? i_A.rows_patches() : i_A.cols_patches();
	const auto cols_A = i_transA == CUBLAS_OP_N ? i_A.cols_patches() : i_A.rows_patches();
	const auto cols_B = i_transB == CUBLAS_OP_N ? i_B.cols_patches() : i_B.rows_patches();

	const auto beta = Float{0.0};
	const auto m = gsl::narrow<int>(rows_A);
	const auto n = gsl::narrow<int>(cols_B);
	const auto k = gsl::narrow<int>(cols_A);
	const auto lda = gsl::narrow<int>(i_A.ld_patches());
	const auto ldb = gsl::narrow<int>(i_B.ld_patches());
	const auto ldc = m;
	const auto batchCount = gsl::narrow<int>(i_A.patch_count());

	auto C = device_patches<Float>{patch_index{batchCount}, Rows{m}, Cols{n}};
	const auto A_stride = i_A.ld();
	const auto B_stride = i_B.ld();
	const auto C_stride = C.ld();
	const auto A_ptr = i_A.data().get();
	const auto B_ptr = i_B.data().get();
	const auto C_ptr = C.data().get();
	auto Aarray = thrust::device_vector<const Float*>(batchCount);
	auto Barray = thrust::device_vector<const Float*>(batchCount);
	auto Carray = thrust::device_vector<Float*>(batchCount);

	const auto begin = thrust::make_counting_iterator<size_t>(0);
	const auto end = thrust::make_counting_iterator<size_t>(batchCount);
	thrust::transform(begin, end, Aarray.begin(),
					  [A_ptr, A_stride] __device__(size_t pos) { return A_ptr + pos * A_stride; });
	thrust::transform(begin, end, Barray.begin(),
					  [B_ptr, B_stride] __device__(size_t pos) { return B_ptr + pos * B_stride; });
	thrust::transform(begin, end, Carray.begin(),
					  [C_ptr, C_stride] __device__(size_t pos) { return C_ptr + pos * C_stride; });

	gemm(i_h, i_transA, i_transB, m, n, k, &i_alpha, Aarray.data().get(), lda, Barray.data().get(),
		 ldb, &beta, Carray.data().get(), ldc, batchCount);

	return C;
}

//! A function that returns the first order moments for given image moments (not including zero-th
//! moments).
/*!
 * \param moments Image moments.
 * \return First order image moments (not including zero-th moments).
 */
template<typename Float>
device_patches<Float> get_first_order_moments(const device_patches<Float>& moments)
{
	Expects(moments.cols_patches() >= 3);
	Expects(moments.col_maj_patches());

	const auto p_count = moments.patch_count();
	const auto rows = moments.rows_patches();
	const auto m_stride = moments.ld();
	const auto m_ptr = moments.data().get();
	auto first_order_moments = device_patches<Float>{patch_index{p_count}, Rows{rows}, Cols{2}};
	auto fom_ptr = first_order_moments.data().get();

	const auto begin = thrust::make_counting_iterator<size_t>(0);
	const auto end = thrust::make_counting_iterator<size_t>(p_count);

	thrust::for_each(begin, end, [m_ptr, fom_ptr, m_stride, rows] __device__(size_t patch) {
		const auto m_off = patch * m_stride + rows;
		const auto fom_off = patch * 2 * rows;
		for(size_t i = 0; i < 2 * rows; i++)
		{
			fom_ptr[fom_off + i] = m_ptr[m_off + i];
		}
	});

	return first_order_moments;
}

//! Singular value decomposition for 2x2 matrices.
/*!
 * \param a Input matrix.
 * \param u Left hand side singular vector.
 * \param v Right hand side singular vector.
 */
template<typename Float>
__host__ __device__ void svd_2x2_impl(const Float* a, Float u[4], Float v[4])
{
	if(a[0] == 0.0 && a[1] == 0.0 && a[2] == 0.0 && a[3] == 0.0)
	{
		u[0] = 1.0;
		u[1] = 0.0;
		u[2] = 0.0;
		u[3] = 1.0;

		v[0] = 1.0;
		v[1] = 0.0;
		v[2] = 0.0;
		v[3] = 1.0;
	}
	else
	{
		const auto a0_a3 = (a[0] - a[3]) * (a[0] - a[3]);
		const auto a0pa3 = (a[0] + a[3]) * (a[0] + a[3]);
		const auto a1pa2 = (a[1] + a[2]) * (a[1] + a[2]);
		const auto a1_a2 = (a[1] - a[2]) * (a[1] - a[2]);

		const auto s0 = 0.5f * (sqrt(a0_a3 + a1pa2) + sqrt(a0pa3 + a1_a2));
		const auto s1 = abs(s0 - sqrt(a0_a3 + a1pa2));

		const auto y = 2 * (a[0] * a[1] + a[2] * a[3]);
		const auto x = a[0] * a[0] - a[1] * a[1] + a[2] * a[2] - a[3] * a[3];

		u[2] = (s0 > s1) ? -sin(0.5f * atan2(y, x)) : 0;
		u[0] = -sqrt(1 - u[2] * u[2]);
		u[1] = u[2];
		u[3] = -u[0];

		v[0] = (s0 != 0) ? (a[0] * u[0] + a[1] * u[2]) / s0 : 1;
		v[2] = (s0 != 0) ? (a[2] * u[0] + a[3] * u[2]) / s0 : 0;
		v[1] = (s1 != 0) ? (a[0] * u[1] + a[1] * u[3]) / s1 : -v[2];
		v[3] = (s1 != 0) ? (a[2] * u[1] + a[3] * u[3]) / s1 : v[0];
	}
}

__host__ __device__ void svd_2x2(const float* a, float u[4], float v[4])
{
	return svd_2x2_impl(a, u, v);
}

__host__ __device__ void svd_2x2(const double* a, double u[4], double v[4])
{
	return svd_2x2_impl(a, u, v);
}

//! Singular value decomposition for 2x2 matrices.
/*!
 * \param u Left hand side matrix.
 * \param v Right hand side matrix.
 * \param uv Matrix product u*v.
 */
template<typename Float>
__host__ __device__ void mat_mul_2x2_impl(const Float u[4], const Float v[4], Float* uv)
{
	// u, v, uv column major
	uv[0] = u[0] * v[0] + u[2] * v[1];
	uv[1] = u[1] * v[0] + u[3] * v[1];
	uv[2] = u[0] * v[2] + u[2] * v[3];
	uv[3] = u[1] * v[2] + u[3] * v[3];
}

__host__ __device__ void mat_mul_2x2(const float u[4], const float v[4], float* uv)
{
	return mat_mul_2x2_impl(u, v, uv);
}
__host__ __device__ void mat_mul_2x2(const double u[4], const double v[4], double* uv)
{
	return mat_mul_2x2_impl(u, v, uv);
}

//! CUDA kernel that computes the perspective transformations from a 2x2 patches.
/*!
 * \param A Patches of size 2x2.
 * \param transformations Output perspective transformations.
 * \param patch_size Size of the corresponding image patches.
 */
template<typename Float>
__global__ void procrustes_transforms_kernel(const Float* __restrict__ A,
											 float* __restrict__ transformations, Size patch_size)
{
	const auto off_in = blockIdx.x * 2 * 2;
	const auto off_out = blockIdx.x * 3 * 3;
	Float u[4];
	Float v[4];
	Float uv[4];

	svd_2x2(A + off_in, u, v);
	mat_mul_2x2(u, v, uv);

	// a = uv^t
	// uv has column major layout, a has row-major layout
	const auto a11 = static_cast<float>(uv[0]);
	const auto a12 = static_cast<float>(uv[2]);
	const auto a21 = static_cast<float>(uv[1]);
	const auto a22 = static_cast<float>(uv[3]);
	const auto b1 = 0.0f;
	const auto b2 = 0.0f;

	// Non invertible matrices have to be explicitly excluded.
	const auto det = a11 * a22 - a12 * a21;
	if(abs(det) > 0.001)
	{
		perspective_matrix(a11, a12, b1, a21, a22, b2, patch_size, transformations + off_out);
	}
	else // identity
	{
		perspective_matrix(1.0f, 0.0f, 0.0f, 0.0f, 1.0f, 0.0f, patch_size,
						   transformations + off_out);
	}
}

//! A function that computes the perspective transformations from a 2x2 patches.
/*!
 * \param A Patches of size 2x2.
 * \param patch_size Size of the corresponding image patches.
 * \return Perspective transformations.
 */
template<typename Float>
device_patches<float> procrustes_transforms(const device_patches<Float>& A, const Size& patch_size)
{
	Expects(A.col_maj_patches());
	Expects(A.rows_patches() == 2);
	Expects(A.cols_patches() == 2);

	const auto blockDim = dim3{1};
	const auto gridDim = dim3{gsl::narrow<uint>(A.patch_count())};
	const auto row_maj = false;
	auto transformations =
		device_patches<float>{patch_index{A.patch_count()}, 3_rows, 3_cols, row_maj};

	procrustes_transforms_kernel<<<gridDim, blockDim>>>(A.data().get(),
														transformations.data().get(), patch_size);
	check(cudaDeviceSynchronize(), cudaSuccess);

	return transformations;
}

//! A function computing the affine transformations of image patches, based on the image moments.
/*!
 * \param lhs Image moments.
 * \param rhs Image moments.
 * \param patch_size Size of the images corresponding to the moments.
 * \param cublas_h Initialized cublas handle.
 * \return Perspective transformation for each pair of patches.
 */
template<typename Float>
device_patches<float> procrustes_solver_impl(const device_patches<Float>& lhs,
											 const device_patches<Float>& rhs,
											 const Size& patch_size, cublasHandle_t cublas_h)
{
	const auto lhs1 = get_first_order_moments(lhs);
	const auto rhs1 = get_first_order_moments(rhs);

	const auto alpha = Float{1.0};
	auto lhs1t_rhs1 = mat_mul(alpha, CUBLAS_OP_T, rhs1, CUBLAS_OP_N, lhs1, cublas_h); // rhs1^t*lhs1

	return procrustes_transforms(lhs1t_rhs1, patch_size);
}

device_patches<float> procrustes_solver(const device_patches<float>& lhs,
										const device_patches<float>& rhs, const Size& patch_size,
										cublasHandle_t cublas_h)
{
	return procrustes_solver_impl(lhs, rhs, patch_size, cublas_h);
}

device_patches<float> procrustes_solver(const device_patches<double>& lhs,
										const device_patches<double>& rhs, const Size& patch_size,
										cublasHandle_t cublas_h)
{
	return procrustes_solver_impl(lhs, rhs, patch_size, cublas_h);
}