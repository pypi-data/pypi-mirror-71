#include "../include/device_patches.h"
#include "../include/enums.h"
#include "../include/sample.h"
#include "../include/utils.h"
#include "../include/vec3.h"
#include "../include/warp_perspective.h"

#include <cuda_runtime.h>

using uint = unsigned int;

/*
**
*** Implementation for patches
**
*/

template<typename FloatVec>
__device__ void warp_perspective_px_device(const FloatVec* __restrict__ input,
										   const float* __restrict__ A,
										   FloatVec* __restrict__ output, int px, int rows,
										   int cols, bool col_maj, interpolation_t i_type)
{
	const auto x = static_cast<float>(col_maj ? px / rows : px % cols);
	const auto y = static_cast<float>(col_maj ? px % rows : px / cols);

	// Compute homogeneous coordinate (x,y,1) for the sampled pixel.
	const auto z_in = A[6] * x + A[7] * y + A[8];
	const auto x_in = (A[0] * x + A[1] * y + A[2]) / z_in;
	const auto y_in = (A[3] * x + A[4] * y + A[5]) / z_in;

	output[px] = sample(input, x_in, y_in, rows, cols, col_maj, i_type);
}

template<typename FloatVec>
__global__ void warp_perspective_patches_kernel(const FloatVec* __restrict__ input,
												const float* __restrict__ transforms,
												FloatVec* __restrict__ output, int rows, int cols,
												size_t patch_count, bool col_maj,
												interpolation_t i_type)
{
	const auto px = static_cast<int>(threadIdx.x); // safe because of max blockDim.x
	const auto in = input + blockIdx.x * rows * cols;
	const auto A = transforms + blockIdx.x * 3 * 3;
	auto out = output + blockIdx.x * rows * cols;

	extern __shared__ __align__(alignof(FloatVec)) unsigned char smem[];
	FloatVec* s = reinterpret_cast<FloatVec*>(smem);

	// Patch size is equal to block size.
	s[threadIdx.x] = in[threadIdx.x];
	__syncthreads();

	warp_perspective_px_device(s, A, out, px, rows, cols, col_maj, i_type);
}

template<typename FloatVec>
device_patches<FloatVec> warp_perspective_impl(const device_patches<FloatVec>& i_patches,
											   const device_patches<float>& i_transforms,
											   interpolation_t i_type)
{
	Expects(i_patches.patch_count() == i_transforms.patch_count());
	Expects(i_transforms.rows_patches() == 3);
	Expects(i_transforms.cols_patches() == 3);
	Expects(i_transforms.col_maj_patches() == false);

	constexpr auto MAX_SMEM_SIZE = 16 * 1024;
	const auto p_total = gsl::narrow<uint>(i_patches.total_per_patch());
	const auto smem = p_total * sizeof(FloatVec);
	if(smem > MAX_SMEM_SIZE)
	{
		throw std::runtime_error{"Only patches with a size of up to " +
								 std::to_string(MAX_SMEM_SIZE) + "bytes are supported."};
	}

	constexpr auto MAX_BLOCK_SIZE = 16 * 1024;
	if(p_total > MAX_BLOCK_SIZE)
	{
		throw std::runtime_error{"Only patches with a size of up to " +
								 std::to_string(MAX_BLOCK_SIZE) + "px are supported."};
	}

	const auto rows = gsl::narrow<int>(i_patches.rows_patches());
	const auto cols = gsl::narrow<int>(i_patches.cols_patches());
	const auto p_count = gsl::narrow<uint>(i_patches.patch_count());
	const auto col_maj = i_patches.col_maj_patches();
	auto out = device_patches<FloatVec>{patch_index{p_count}, i_patches.size_patches(), col_maj};

	// Each thread computes one pixel of a patch.
	const auto blockDim = dim3{p_total};
	const auto gridDim = dim3{p_count};

	warp_perspective_patches_kernel<<<gridDim, blockDim, smem>>>(
		i_patches.data().get(), i_transforms.data().get(), out.data().get(), rows, cols, p_count,
		col_maj, i_type);
	check(cudaDeviceSynchronize(), cudaSuccess);

	return out;
}

/*
**
*** Implementation for matrix
**
*/

template<typename FloatVec>
__device__ void warp_perspective_device(const FloatVec* __restrict__ input,
										const float* __restrict__ A, FloatVec* __restrict__ output,
										int rows, int cols, bool col_maj, interpolation_t i_type)
{
	if(col_maj)
	{
		for(int x = 0; x < cols; x++)
		{
			for(int y = 0; y < rows; y++)
			{
				// Compute homogeneous coordinate (x,y,1) for the sampled pixel.
				const auto z_in = A[6] * x + A[7] * y + A[8];
				const auto x_in = (A[0] * x + A[1] * y + A[2]) / z_in;
				const auto y_in = (A[3] * x + A[4] * y + A[5]) / z_in;

				output[y + x * rows] = sample(input, x_in, y_in, rows, cols, col_maj, i_type);
			}
		}
	}
	else
	{
		for(int y = 0; y < rows; y++)
		{
			for(int x = 0; x < cols; x++)
			{
				// Compute homogeneous coordinate (x,y,1) for the sampled pixel.
				const auto z_in = A[6] * x + A[7] * y + A[8];
				const auto x_in = (A[0] * x + A[1] * y + A[2]) / z_in;
				const auto y_in = (A[3] * x + A[4] * y + A[5]) / z_in;

				output[x + y * cols] = sample(input, x_in, y_in, rows, cols, col_maj, i_type);
			}
		}
	}
}

template<typename FloatVec>
__global__ void warp_perspective_matrix_kernel(const FloatVec* __restrict__ input,
											   const float* __restrict__ transforms,
											   FloatVec* __restrict__ output, int rows, int cols,
											   size_t patch_count, bool col_maj,
											   interpolation_t i_type)
{
	const auto patch = threadIdx.x + blockIdx.x * blockDim.x;
	const auto smem_size = rows * cols;

	extern __shared__ __align__(alignof(FloatVec)) unsigned char smem[];
	FloatVec* s = reinterpret_cast<FloatVec*>(smem);

	for(auto i = threadIdx.x; i < smem_size; i += blockDim.x)
	{
		s[i] = input[i];
	}
	__syncthreads();

	if(patch < patch_count)
	{
		const auto A = transforms + patch * 3 * 3;
		auto out = output + patch * rows * cols;

		warp_perspective_device(s, A, out, rows, cols, col_maj, i_type);
	}
}

template<typename FloatVec>
device_patches<FloatVec> warp_perspective_impl(const device_matrix<FloatVec>& i_matrix,
											   const device_patches<float>& i_transforms,
											   interpolation_t i_type)
{
	Expects(i_transforms.rows_patches() == 3);
	Expects(i_transforms.cols_patches() == 3);
	Expects(i_transforms.col_maj_patches() == false);

	constexpr auto MAX_SMEM_SIZE = 16 * 1024;
	const auto smem = i_matrix.total() * sizeof(FloatVec);
	if(smem > MAX_SMEM_SIZE)
	{
		throw std::runtime_error{"Only matrices with a size of up to " +
								 std::to_string(MAX_SMEM_SIZE) + "bytes are supported."};
	}

	const auto rows = gsl::narrow<int>(i_matrix.rows());
	const auto cols = gsl::narrow<int>(i_matrix.cols());
	const auto p_count = gsl::narrow<uint>(i_transforms.patch_count());
	const auto col_maj = i_matrix.col_maj();
	auto out = device_patches<FloatVec>{patch_index{p_count}, i_matrix.size(), col_maj};

	// The threads are divided into large blocks to facilitate shared memory and reduce bank
	// conflicts when loading the input.
	const auto blockDim = dim3{256}; // Max blockDim.
	const auto gridDim = dim3{p_count / 256 + 1};

	warp_perspective_matrix_kernel<<<gridDim, blockDim, smem>>>(
		i_matrix.data().get(), i_transforms.data().get(), out.data().get(), rows, cols, p_count,
		col_maj, i_type);

	check(cudaDeviceSynchronize(), cudaSuccess);

	return out;
}

/*
**
*** Specializations
**
*/

device_patches<float> warp_perspective(const device_patches<float>& i_patches,
									   const device_patches<float>& i_transforms,
									   interpolation_t i_type)
{
	return warp_perspective_impl(i_patches, i_transforms, i_type);
}

device_patches<double> warp_perspective(const device_patches<double>& i_patches,
										const device_patches<float>& i_transforms,
										interpolation_t i_type)
{
	return warp_perspective_impl(i_patches, i_transforms, i_type);
}

device_patches<vec3<float>> warp_perspective(const device_patches<vec3<float>>& i_patches,
											 const device_patches<float>& i_transforms,
											 interpolation_t i_type)
{
	return warp_perspective_impl(i_patches, i_transforms, i_type);
}

device_patches<vec3<double>> warp_perspective(const device_patches<vec3<double>>& i_patches,
											  const device_patches<float>& i_transforms,
											  interpolation_t i_type)
{
	return warp_perspective_impl(i_patches, i_transforms, i_type);
}

device_patches<float> warp_perspective(const device_matrix<float>& i_matrix,
									   const device_patches<float>& i_transforms,
									   interpolation_t i_type)
{
	return warp_perspective_impl(i_matrix, i_transforms, i_type);
}

device_patches<double> warp_perspective(const device_matrix<double>& i_matrix,
										const device_patches<float>& i_transforms,
										interpolation_t i_type)
{
	return warp_perspective_impl(i_matrix, i_transforms, i_type);
}

device_patches<vec3<float>> warp_perspective(const device_matrix<vec3<float>>& i_patches,
											 const device_patches<float>& i_transforms,
											 interpolation_t i_type)
{
	return warp_perspective_impl(i_patches, i_transforms, i_type);
}

device_patches<vec3<double>> warp_perspective(const device_matrix<vec3<double>>& i_patches,
											  const device_patches<float>& i_transforms,
											  interpolation_t i_type)
{
	return warp_perspective_impl(i_patches, i_transforms, i_type);
}