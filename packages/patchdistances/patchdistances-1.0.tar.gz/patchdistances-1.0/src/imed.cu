#include "../include/device_matrix.h"
#include "../include/imed.h"
#include "../include/utils.h"

#include "../extern/gsl/gsl_util"

#include <cuda_runtime.h>
#include <device_launch_parameters.h>

using uint = unsigned int;
constexpr auto SMEM_SIZE = 16 * 1024;

//! Templated CUDA kernel to compute the Convolution Standardized Transform (CFT) of patches.
/*!
 * gridDim: patch count; blockDim: patch size; smem: (patch_cols + 4) * (patch_rows + 4)
 * Each block computes a patch and each thread a pixel of a patch.
 * \param i_patches Input patches.
 * \param o_patches Convolved patches of the same size with boundary condition zero.
 * \param i_rows Rows of each patch i_patches.
 * \param i_cols
 * Columns of each patch i_patches.
 */
template<typename T>
__global__ void imed_cft_kernel_shared(const T* __restrict__ i_patches, T* __restrict__ o_patches,
									   uint i_rows, uint i_cols)
{
	// The convolution kernel is the Kronecker product of [0.0053, 0.2171, 0.5519, 0.2171, 0.0053].
	// Entries of the kernel.
	constexpr auto k00 = 2.809e-5;
	constexpr auto k10 = 1.15063e-3;
	constexpr auto k20 = 2.92507e-3;
	constexpr auto k30 = k10;
	constexpr auto k40 = k00;

	constexpr auto k01 = k10;
	constexpr auto k11 = 4.713241e-02;
	constexpr auto k21 = 1.1981749e-01;
	constexpr auto k31 = k11;
	constexpr auto k41 = k01;

	constexpr auto k02 = k20;
	constexpr auto k12 = k21;
	constexpr auto k22 = 3.0459361e-01;
	constexpr auto k32 = k12;
	constexpr auto k42 = k02;

	constexpr auto k03 = k30;
	constexpr auto k13 = k31;
	constexpr auto k23 = k32;
	constexpr auto k33 = k13;
	constexpr auto k43 = k03;

	constexpr auto k04 = k00;
	constexpr auto k14 = k10;
	constexpr auto k24 = k20;
	constexpr auto k34 = k30;
	constexpr auto k44 = k40;

	extern __shared__ __align__(alignof(T)) unsigned char smem[];
	T* s = reinterpret_cast<T*>(smem);

	// Load the patch including zero padding to shared memory.
	const auto padded_rows = i_rows + 4;
	const auto padded_cols = i_cols + 4;
	const auto padded_size = padded_rows * padded_cols;
	const auto idx = threadIdx.x + blockDim.x * blockIdx.x;
	const auto off_patch = blockIdx.x * i_rows * i_cols;

	for(uint i = threadIdx.x; i < padded_size; i += blockDim.x)
	{
		const auto padded_row = i % (i_rows + 4);
		const auto padded_col = i / (i_rows + 4);

		if(padded_row >= 2 && padded_row < i_rows + 2 && padded_col >= 2 && padded_col < i_cols + 2)
		{
			s[i] = i_patches[off_patch + padded_row - 2 + (padded_col - 2) * i_rows];
		}
		else
		{
			s[i] = T{0.0};
		}
	}
	__syncthreads();

	// Center coordinates of the current thread.
	// Upper left corner of the padded size.
	const auto row = threadIdx.x % i_rows;
	const auto col = threadIdx.x / i_rows;

	// Offset for each column.
	const auto col0 = row + col * padded_rows;
	const auto col1 = col0 + padded_rows;
	const auto col2 = col1 + padded_rows;
	const auto col3 = col2 + padded_rows;
	const auto col4 = col3 + padded_rows;

	const auto val00 = s[col0];
	const auto val10 = s[col0 + 1];
	const auto val20 = s[col0 + 2];
	const auto val30 = s[col0 + 3];
	const auto val40 = s[col0 + 4];

	const auto val01 = s[col1];
	const auto val11 = s[col1 + 1];
	const auto val21 = s[col1 + 2];
	const auto val31 = s[col1 + 3];
	const auto val41 = s[col1 + 4];

	const auto val02 = s[col2];
	const auto val12 = s[col2 + 1];
	const auto val22 = s[col2 + 2];
	const auto val32 = s[col2 + 3];
	const auto val42 = s[col2 + 4];

	const auto val03 = s[col3];
	const auto val13 = s[col3 + 1];
	const auto val23 = s[col3 + 2];
	const auto val33 = s[col3 + 3];
	const auto val43 = s[col3 + 4];

	const auto val04 = s[col4];
	const auto val14 = s[col4 + 1];
	const auto val24 = s[col4 + 2];
	const auto val34 = s[col4 + 3];
	const auto val44 = s[col4 + 4];

	// Column sums of the convolution, taking into account the symmetry of the kernel.
	const auto col0sum = val00 * k00 + val10 * k10 + val20 * k20 + val30 * k30 + val40 * k40;
	const auto col1sum = val01 * k01 + val11 * k11 + val21 * k21 + val31 * k31 + val41 * k41;
	const auto col2sum = val02 * k02 + val12 * k12 + val22 * k22 + val32 * k32 + val42 * k42;
	const auto col3sum = val03 * k03 + val13 * k13 + val23 * k23 + val33 * k33 + val43 * k43;
	const auto col4sum = val04 * k04 + val14 * k14 + val24 * k24 + val34 * k34 + val44 * k44;

	// It is safe to write, since loads are fenced by __syncthreads();
	o_patches[idx] = col0sum + col1sum + col2sum + col3sum + col4sum;
}

//! Templated CUDA kernel to compute the Convolution Standardized Transform (CFT) of patches.
/*!
 * gridDim: patch count, patch rows, patch columns
 * Each block computes a patch and each thread a pixel of a patch.
 * This kernel is slow and only used for large images.
 * \param i_patches Input patches.
 * \param o_patches Convolved patches of the same size with boundary condition zero.
 * Columns of each patch i_patches.
 */
template<typename T>
__global__ void imed_cft_kernel(const T* __restrict__ i_patches, T* __restrict__ o_patches)
{
	// The convolution kernel is the Kronecker product of [0.0053, 0.2171, 0.5519, 0.2171, 0.0053].
	// Entries of the kernel.
	constexpr auto k00 = 2.809e-5;
	constexpr auto k10 = 1.15063e-3;
	constexpr auto k20 = 2.92507e-3;
	constexpr auto k30 = k10;
	constexpr auto k40 = k00;

	constexpr auto k01 = k10;
	constexpr auto k11 = 4.713241e-02;
	constexpr auto k21 = 1.1981749e-01;
	constexpr auto k31 = k11;
	constexpr auto k41 = k01;

	constexpr auto k02 = k20;
	constexpr auto k12 = k21;
	constexpr auto k22 = 3.0459361e-01;
	constexpr auto k32 = k12;
	constexpr auto k42 = k02;

	constexpr auto k03 = k30;
	constexpr auto k13 = k31;
	constexpr auto k23 = k32;
	constexpr auto k33 = k13;
	constexpr auto k43 = k03;

	constexpr auto k04 = k00;
	constexpr auto k14 = k10;
	constexpr auto k24 = k20;
	constexpr auto k34 = k30;
	constexpr auto k44 = k40;

	const auto patch_no = blockIdx.x;
	const auto row_u = blockIdx.y;
	const auto col_u = blockIdx.z;
	const auto rows_u = gridDim.y;
	const auto cols_u = gridDim.z;
	const auto patch_size = rows_u * cols_u;
	const auto patch_idx = row_u + col_u * rows_u;
	const auto global_idx = patch_idx + patch_no * patch_size;
	const auto s = i_patches + patch_no * patch_size;

	// Offset for each column.
	const auto row = static_cast<int>(row_u); // Casts are safe, numbers are small
	const auto col = static_cast<int>(col_u);
	const auto rows = static_cast<int>(rows_u);
	const auto cols = static_cast<int>(cols_u);
	// Upper left corner of the kernel size.
	const auto col0 = row - 2 + (col - 2) * rows;
	const auto col1 = col0 + rows;
	const auto col2 = col1 + rows;
	const auto col3 = col2 + rows;
	const auto col4 = col3 + rows;

	const auto val00 = row >= 2 && col >= 2 ? s[col0] : T{0.0};
	const auto val10 = row >= 1 && col >= 2 ? s[col0 + 1] : T{0.0};
	const auto val20 = col >= 2 ? s[col0 + 2] : T{0.0};
	const auto val30 = row < rows - 1 && col >= 2 ? s[col0 + 3] : T{0.0};
	const auto val40 = row < rows - 2 && col >= 2 ? s[col0 + 4] : T{0.0};

	const auto val01 = row >= 2 && col >= 1 ? s[col1] : T{0.0};
	const auto val11 = row >= 1 && col >= 1 ? s[col1 + 1] : T{0.0};
	const auto val21 = col >= 1 ? s[col1 + 2] : T{0.0};
	const auto val31 = row < rows - 1 && col >= 1 ? s[col1 + 3] : T{0.0};
	const auto val41 = row < rows - 2 && col >= 1 ? s[col1 + 4] : T{0.0};

	const auto val02 = row >= 2 ? s[col2] : T{0.0};
	const auto val12 = row >= 1 ? s[col2 + 1] : T{0.0};
	const auto val22 = s[col2 + 2];
	const auto val32 = row < rows - 1 ? s[col2 + 3] : T{0.0};
	const auto val42 = row < rows - 2 ? s[col2 + 4] : T{0.0};

	const auto val03 = row >= 2 && col < cols - 1 ? s[col3] : T{0.0};
	const auto val13 = row >= 1 && col < cols - 1 ? s[col3 + 1] : T{0.0};
	const auto val23 = col < cols - 1 ? s[col3 + 2] : T{0.0};
	const auto val33 = row < rows - 1 && col < cols - 1 ? s[col3 + 3] : T{0.0};
	const auto val43 = row < rows - 2 && col < cols - 1 ? s[col3 + 4] : T{0.0};

	const auto val04 = row >= 2 && col < cols - 2 ? s[col4] : T{0.0};
	const auto val14 = row >= 1 && col < cols - 2 ? s[col4 + 1] : T{0.0};
	const auto val24 = col < cols - 2 ? s[col4 + 2] : T{0.0};
	const auto val34 = row < rows - 1 && col < cols - 2 ? s[col4 + 3] : T{0.0};
	const auto val44 = row < rows - 2 && col < cols - 2 ? s[col4 + 4] : T{0.0};

	// Column sums of the convolution, taking into account the symmetry of the kernel.
	const auto col0sum = val00 * k00 + val10 * k10 + val20 * k20 + val30 * k30 + val40 * k40;
	const auto col1sum = val01 * k01 + val11 * k11 + val21 * k21 + val31 * k31 + val41 * k41;
	const auto col2sum = val02 * k02 + val12 * k12 + val22 * k22 + val32 * k32 + val42 * k42;
	const auto col3sum = val03 * k03 + val13 * k13 + val23 * k23 + val33 * k33 + val43 * k43;
	const auto col4sum = val04 * k04 + val14 * k14 + val24 * k24 + val34 * k34 + val44 * k44;

	o_patches[global_idx] = col0sum + col1sum + col2sum + col3sum + col4sum;
}

template<typename T>
device_patches<T> imed_cft_impl(const device_patches<T>& i_patches)
{
	Expects(i_patches.col_maj_patches());

	const auto in_ptr = i_patches.data().get();
	const auto rows = gsl::narrow<uint>(i_patches.rows_patches());
	const auto cols = gsl::narrow<uint>(i_patches.cols_patches());
	const auto count = gsl::narrow<uint>(i_patches.patch_count());
	const auto smem = (rows + 4) * (cols + 4) * sizeof(T);
	auto out = device_patches<T>{patch_index{count}, i_patches.size_patches()};
	auto out_ptr = out.data().get();

	if(smem <= SMEM_SIZE)
	{
		const auto gridDim = dim3{count};
		const auto blockDim = dim3{rows * cols};
		imed_cft_kernel_shared<<<gridDim, blockDim, smem>>>(in_ptr, out_ptr, rows, cols);
	}
	else
	{
		const auto gridDim = dim3{count, rows, cols};
		const auto blockDim = dim3{1};
		imed_cft_kernel<<<gridDim, blockDim>>>(in_ptr, out_ptr);
	}

	check(cudaDeviceSynchronize(), cudaSuccess);

	return out;
}

device_patches<float> imed_cft(const device_patches<float>& i_patches)
{
	return imed_cft_impl(i_patches);
}

device_patches<double> imed_cft(const device_patches<double>& i_patches)
{
	return imed_cft_impl(i_patches);
}

device_patches<vec3<float>> imed_cft(const device_patches<vec3<float>>& i_patches)
{
	return imed_cft_impl(i_patches);
}

device_patches<vec3<double>> imed_cft(const device_patches<vec3<double>>& i_patches)
{
	return imed_cft_impl(i_patches);
}