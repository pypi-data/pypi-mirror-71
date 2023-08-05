/*! \file utils.h
	\brief Various uitilty functions for device_matrix and device_patches.
	\sa device_matrix, device_patches.h
*/

#pragma once

#include "device_matrix.h"
#include "device_patches.h"
#include "vec3.h"

#include <cuda_runtime.h>
#include <thrust/device_ptr.h>
#include <thrust/device_vector.h>
#include <thrust/execution_policy.h>
#include <thrust/for_each.h>
#include <thrust/functional.h>
#include <thrust/host_vector.h>
#include <thrust/inner_product.h>
#include <thrust/iterator/counting_iterator.h>
#include <thrust/iterator/iterator_traits.h>
#include <thrust/sequence.h>
#include <thrust/system/cuda/error.h>
#include <thrust/system/error_code.h>
#include <thrust/system_error.h>

//! Implementation details.
namespace impl
{
//! CUDA kernel. Matrix transpose for patches, i.e., each patch will be transposed.
/*!
 * \param idata Continuous input matrix in device memory.
 * \param odata Initialized output data of size rows*cols*sizeof(T).
 * \param rows idata rows.
 * \param cols idata columns.
 * \tparam T Any data type.
 */
template<typename T>
__global__ void transpose_patches_kernel(const T* idata, T* odata, unsigned int rows,
										 unsigned int cols)
{
	const auto off = blockIdx.x * rows * cols;

	for(unsigned int i = 0; i < rows; i++)
	{
		for(unsigned int j = 0; j < cols; j++)
		{
			odata[off + j + i * cols] = idata[off + i + j * rows];
		}
	}
}

//! Matrix transpose for patches, i.e., each patch will be transposed.
/*!
 * \param p Device patches.
 * \param transpose_p If true transpose the patch dimension and keep the memory layout, otherwise
 * keep the dimension and change the memory layout. \tparam Any data type.
 * \tparam T Any data type.
 */
template<typename T>
device_patches<T> transpose_memory(const device_patches<T>& p, bool transpose_p)
{
	const auto count = gsl::narrow<unsigned int>(p.patch_count());
	const auto rows = gsl::narrow<unsigned int>(p.rows_patches());
	const auto cols = gsl::narrow<unsigned int>(p.cols_patches());
	const auto gridDim = dim3{count};
	const auto blockDim = dim3{1};
	auto out =
		transpose_p
			? device_patches<T>{patch_index{count}, Rows{cols}, Cols{rows}, p.col_maj_patches()}
			: device_patches<T>{patch_index{count}, Rows{rows}, Cols{cols}, !p.col_maj_patches()};

	if(p.col_maj_patches())
	{
		transpose_patches_kernel<T>
			<<<gridDim, blockDim>>>(p.data().get(), out.data().get(), rows, cols);
	}
	else
	{
		transpose_patches_kernel<T>
			<<<gridDim, blockDim>>>(p.data().get(), out.data().get(), cols, rows);
	}

	return out;
}

//! Block dimension of CUDA kernels transposing matrices.
constexpr auto BLOCK_DIM = 16u;

//! CUDA kernel. No bank-conflict matrix transpose.
/*!
 * \param idata Continuous input matrix in device memory.
 * \param odata Initialized output data of size rows*cols*sizeof(T).
 * \param rows idata rows.
 * \param cols idata columns.
 * \tparam T Any data type.
 */
template<typename T>
__global__ void transpose_matrix_kernel(const T* idata, T* odata, unsigned int rows,
										unsigned int cols)
{
	__shared__ T block[BLOCK_DIM][BLOCK_DIM];

	const auto row_in = blockIdx.x * BLOCK_DIM + threadIdx.x;
	const auto col_in = blockIdx.y * BLOCK_DIM + threadIdx.y;
	if((row_in < rows) && (col_in < cols))
	{
		block[threadIdx.y][threadIdx.x] = idata[row_in + col_in * rows];
	}

	__syncthreads();

	const auto row_out = blockIdx.y * BLOCK_DIM + threadIdx.x;
	const auto col_out = blockIdx.x * BLOCK_DIM + threadIdx.y;
	if((row_out < cols) && (col_out < rows))
	{
		odata[row_out + col_out * cols] = block[threadIdx.x][threadIdx.y];
	}
}

/*
 **
 *** to_cuda
 **
 */

//! \private
template<typename T>
struct to_cuda
{
	using type = T;
};

//! \private
template<>
struct to_cuda<vec3<float>>
{
	using type = float3;
};

//! \private
template<>
struct to_cuda<vec3<double>>
{
	using type = double3;
};

template<typename T>
using to_cuda_t = typename to_cuda<T>::type;
/**< Convenience overload for to_cuda<T>::type.*/

//! Matrix transpose.
/*!
 * \param m Device matrix.
 * \param transpose_m If true transpose matrix dimension and keep the memory layout, otherwise keep
 * the dimension and change the memory layout.
 * \tparam T Any data type.
 */
template<typename T>
device_matrix<T> transpose_memory(const device_matrix<T>& m, bool transpose_m)
{
	// Too small matrices can not be handled with the matrix specific kernel.
	if(m.rows() < BLOCK_DIM || m.cols() < BLOCK_DIM)
	{
		return copy(transpose_memory(device_patches<T>{m}, transpose_m), 0);
	}

	// The vec3 struct does not have the requirements to be used with CUDA static shared memory
	// (i.e., trivial, empty constructor with no initializer list). But it has the same memory
	// layout as CUDAs float3, which satisfies the requirements.
	using C = to_cuda_t<T>;

	const auto rows = gsl::narrow<unsigned int>(m.rows());
	const auto cols = gsl::narrow<unsigned int>(m.cols());
	const auto blockDim = dim3{BLOCK_DIM, BLOCK_DIM};
	auto out = transpose_m ? device_matrix<T>{Rows{cols}, Cols{rows}, m.col_maj()}
						   : device_matrix<T>{Rows{rows}, Cols{cols}, !m.col_maj()};

	if(m.col_maj())
	{
		const auto gridDim = dim3{rows / BLOCK_DIM + 1, cols / BLOCK_DIM + 1};
		transpose_matrix_kernel<C>
			<<<gridDim, blockDim>>>(reinterpret_cast<const C*>(m.data().get()),
									reinterpret_cast<C*>(out.data().get()), rows, cols);
	}
	else
	{
		const auto gridDim = dim3{cols / BLOCK_DIM + 1, rows / BLOCK_DIM + 1};
		transpose_matrix_kernel<C>
			<<<gridDim, blockDim>>>(reinterpret_cast<const C*>(m.data().get()),
									reinterpret_cast<C*>(out.data().get()), cols, rows);
	}

	return out;
}
} // namespace impl

//! Template function that throws on general cuda errors.
/*!
 * \param status The status that will be checked for success.
 * \param success The success status.
 * \param message Optional error message.
 */
template<typename T>
void check(const T& status, const T& success, const char* message = "") noexcept(false)
{
	if(status != success)
	{
		throw thrust::system_error{status, thrust::cuda_category(), message};
	}
}

//! Returns a sequence from 0 to size-1 in device memory.
inline thrust::device_vector<std::size_t> d_seq(size_t size)
{
	auto seq = thrust::device_vector<std::size_t>(size);
	thrust::sequence(seq.begin(), seq.end(), std::size_t{0});
	return seq;
}

// A functions that returns the number of patches with full support.
/*!
 * \param i_img_size Image size.
 * \param i_patch_size Size of fully supported patches.
 */
inline Size patch_count_size(const Size& i_img_size, const Size& i_patch_size)
{
	return Size{Rows{i_img_size.rows() - i_patch_size.rows() + 1},
				Cols{i_img_size.cols() - i_patch_size.cols() + 1}};
}

//! A template function that copies a subset of patches.
/*!
 * \param i_patches Patches to copy.
 * \param i_indices Indices of patches to copy. Indices can show up multiple times.
 * \return Copied patches.
 */
template<typename T>
device_patches<T> copy(const device_patches<T>& i_patches, const std::vector<size_t>& i_indices)
{
	const auto col_maj_patch = i_patches.col_maj_patches();

	auto copies =
		device_patches<T>{patch_index{i_indices.size()}, i_patches.size_patches(), col_maj_patch};

	for(size_t i = 0; i < i_indices.size(); i++)
	{
		const auto odx = patch_index{i};
		const auto idx = patch_index{i_indices.at(i)};
		Expects(idx.value() < i_patches.patch_count());

		thrust::copy(i_patches.cbegin(idx), i_patches.cend(idx), copies.begin(odx));
	}

	return copies;
}

//! A template function that copies one patch and returns it as a matrix.
/*!
 * \param i_patches Patches to copy.
 * \param i_index Index of patch to copy.
 * \return Copied patch as matrix.
 */
template<typename T>
device_matrix<T> copy(const device_patches<T>& i_patches, size_t i_index)
{
	const auto col_maj_patch = i_patches.col_maj_patches();
	auto copy = device_matrix<T>{i_patches.size_patches(), col_maj_patch};
	const auto idx = patch_index{i_index};

	thrust::copy(i_patches.cbegin(idx), i_patches.cend(idx), copy.begin());

	return copy;
}

//! A template function that splits rgb device_patches into three separate channels.
/*!
 * \param i_patches Patches to split.
 * \return Array of patches with each channel.
 */
template<typename T>
std::array<device_patches<T>, 3> split(const device_patches<vec3<T>>& i_patches)
{
	Expects(i_patches.patch_count() > 0);

	auto ch = std::array<device_patches<T>, 3>();
	ch.fill(device_patches<T>{patch_index{i_patches.patch_count()}, Rows{i_patches.rows_patches()},
							  Cols{i_patches.cols_patches()}, i_patches.col_maj_patches()});

	const auto in_ptr = i_patches.data().get();
	auto ch1_ptr = ch[0].data().get();
	auto ch2_ptr = ch[1].data().get();
	auto ch3_ptr = ch[2].data().get();

	const auto begin = thrust::make_counting_iterator<size_t>(0);
	const auto end = begin + i_patches.total();

	thrust::for_each(begin, end, [=] __device__(size_t idx) {
		const auto val = in_ptr[idx];
		ch1_ptr[idx] = val._1;
		ch2_ptr[idx] = val._2;
		ch3_ptr[idx] = val._3;
	});

	return ch;
}

//! A template function that joins three sets of patches to one set of multi-channel patches.
/*!
 * \param i_ch1 Patches for the first channel.
 * \param i_ch2 Patches for the second channel.
 * \param i_ch3 Patches for the third channel.
 * \return Three channel patches.
 */
template<typename T>
device_patches<vec3<T>> join(const device_patches<T>& i_ch1, const device_patches<T>& i_ch2,
							 const device_patches<T>& i_ch3)
{
	Expects(i_ch1.patch_count() > 0);
	Expects(i_ch1.patch_count() == i_ch2.patch_count());
	Expects(i_ch1.patch_count() == i_ch3.patch_count());
	Expects(i_ch1.size_patches() == i_ch2.size_patches());
	Expects(i_ch1.size_patches() == i_ch3.size_patches());
	Expects(i_ch1.col_maj_patches() == i_ch2.col_maj_patches());
	Expects(i_ch1.col_maj_patches() == i_ch3.col_maj_patches());

	auto img = device_patches<vec3<T>>{patch_index{i_ch1.patch_count()}, Rows{i_ch1.rows_patches()},
									   Cols{i_ch1.cols_patches()}, i_ch1.col_maj_patches()};

	auto img_ptr = img.data().get();
	const auto ch1_ptr = i_ch1.data().get();
	const auto ch2_ptr = i_ch2.data().get();
	const auto ch3_ptr = i_ch3.data().get();

	const auto begin = thrust::make_counting_iterator<size_t>(0);
	const auto end = begin + i_ch1.total();

	thrust::for_each(begin, end, [=] __device__(size_t idx) {
		img_ptr[idx] = vec3<T>{ch1_ptr[idx], ch2_ptr[idx], ch3_ptr[idx]};
	});

	return img;
}

//! A template function that returns the underlying data vector in host memory.
/*!
 * \param i_matrix Matrix.
 * \return Underlying data vector in host memory.
 */
template<typename T>
std::vector<T> get_host_vector(const device_matrix<T>& i_matrix)
{
	auto h_vec = thrust::host_vector<T>(i_matrix.cbegin(), i_matrix.cend());

	return std::vector<T>(h_vec.cbegin(), h_vec.cend());
}

//! A template function that returns the underlying data vector in host memory.
/*!
 * \param i_patches Patches.
 * \return Underlying data vector in host memory.
 */
template<typename T>
std::vector<T> get_host_vector(const device_patches<T>& i_patches)
{
	auto h_vec = thrust::host_vector<T>(i_patches.cbegin(), i_patches.cend());

	return std::vector<T>(h_vec.cbegin(), h_vec.cend());
}

//! A template function that changes the memory layout of a matrix to column-major.
/*!
 * \param m Matrix.
 * \return Column-major input matrix.
 */
template<typename T>
device_matrix<T> to_col_maj(const device_matrix<T>& m)
{
	if(!m.col_maj())
	{
		const auto change_mem_layout_tag = false;
		return impl::transpose_memory(m, change_mem_layout_tag);
	}
	else
	{
		return m;
	}
}

//! A template function that changes the memory layout of a matrix to column-major.
/*!
 * \param m Matrix.
 * \return Column-major input matrix.
 */
template<typename T>
device_matrix<T> to_col_maj(device_matrix<T>&& m)
{
	if(!m.col_maj())
	{
		const auto change_mem_layout_tag = false;
		return impl::transpose_memory(m, change_mem_layout_tag);
	}
	else
	{
		return m;
	}
}

//! A template function that changes the memory layout of patches to column-major.
/*!
 * \param p Patches.
 * \return Column-major input patches.
 */
template<typename T>
device_patches<T> to_col_maj(const device_patches<T>& p)
{
	if(!p.col_maj_patches())
	{
		const auto change_mem_layout_tag = false;
		return impl::transpose_memory(p, change_mem_layout_tag);
	}
	else
	{
		return p;
	}
}

//! A template function that changes the memory layout of patches to column-major.
/*!
 * \param p Patches.
 * \return Column-major input patches.
 */
template<typename T>
device_patches<T> to_col_maj(device_patches<T>&& p)
{
	if(!p.col_maj_patches())
	{
		const auto change_mem_layout_tag = false;
		return impl::transpose_memory(p, change_mem_layout_tag);
	}
	else
	{
		return p;
	}
}

//! A template function that changes the memory layout of a matrix to row-major.
/*!
 * \param m Matrix.
 * \return Row-major input matrix.
 */
template<typename T>
device_matrix<T> to_row_maj(const device_matrix<T>& m)
{
	if(m.col_maj())
	{
		const auto change_mem_layout_tag = false;
		return impl::transpose_memory(m, change_mem_layout_tag);
	}
	else
	{
		return m;
	}
}

//! A template function that changes the memory layout of a matrix to row-major.
/*!
 * \param m Matrix.
 * \return Row-major input matrix.
 */
template<typename T>
device_matrix<T> to_row_maj(device_matrix<T>&& m)
{
	if(m.col_maj())
	{
		const auto change_mem_layout_tag = false;
		return impl::transpose_memory(m, change_mem_layout_tag);
	}
	else
	{
		return m;
	}
}

//! A template function that changes the memory layout of patches to row-major.
/*!
 * \param p Patches.
 * \return Row-major input patches.
 */
template<typename T>
device_patches<T> to_row_maj(const device_patches<T>& p)
{
	if(p.col_maj_patches())
	{
		const auto change_mem_layout_tag = false;
		return impl::transpose_memory(p, change_mem_layout_tag);
	}
	else
	{
		return p;
	}
}

//! A template function that changes the memory layout of patches to row-major.
/*!
 * \param p Patches.
 * \return Row-major input patches.
 */
template<typename T>
device_patches<T> to_row_maj(device_patches<T>&& p)
{
	if(p.col_maj_patches())
	{
		const auto change_mem_layout_tag = false;
		return impl::transpose_memory(p, change_mem_layout_tag);
	}
	else
	{
		return p;
	}
}

//! A template function that tranposes a matrix.
/*!
 * \param m Matrix.
 * \return Transposed matrix.
 */
template<typename T>
device_patches<T> transpose(const device_matrix<T>& m)
{
	const auto transpose = true;
	return impl::transpose_memory(m, transpose);
}

//! A template function that tranposes each patch.
/*!
 * \param p Patches.
 * \return Transposed patches.
 */
template<typename T>
device_patches<T> transpose(const device_patches<T>& p)
{
	const auto transpose = true;
	return impl::transpose_memory(p, transpose);
}

//! Template function that copies patches onto a larger background with an offset.
/*!
 * \param i_patches Patches. Must have column-major memory layout.
 * \param i_offsets Offset for each patch, where (0,0) denotes a centered patch. If the center is
 * not a discrete value, it will be shifted to the nearest upper left pixel.
 * \param i_emb_size Size of the embedded patches. Must be larger than i_patches.
 * \param i_background Background value of the embedded patches.
 * \return Embedded patches.
 */
template<typename T>
device_patches<T> embed(const device_patches<T>& i_patches,
						const device_matrix<thrust::pair<int, int>>& i_offsets,
						const Size& i_emb_size, T i_background)
{
	Expects(i_patches.col_maj_patches());
	Expects(i_patches.rows_patches() <= i_emb_size.rows());
	Expects(i_patches.cols_patches() <= i_emb_size.cols());
	Expects(i_patches.patch_count() == i_offsets.total());

	const auto itotal = i_patches.total_per_patch();
	const auto icount = i_patches.patch_count();
	const auto irows = i_patches.rows_patches();
	const auto icols = i_patches.cols_patches();

	const auto etotal = i_emb_size.total();
	const auto erows = i_emb_size.rows();
	const auto ecols = i_emb_size.cols();

	// Offset such that embedded patches are centered.
	const auto off_x = (ecols - icols) / 2;
	const auto off_y = (erows - irows) / 2;

	const auto begin = thrust::counting_iterator<size_t>{0};
	const auto end = begin + icount;

	auto embedded = device_patches<T>{patch_index{icount}, i_emb_size, i_background};
	auto eptr = embedded.data().get();
	const auto pptr = i_patches.data().get();
	const auto optr = i_offsets.data().get();

	// Each thread computes one patch.
	thrust::for_each(begin, end, [=] __device__(size_t patch) {
		// Offset for the current patch
		const auto x = optr[patch].first;
		const auto y = optr[patch].second;

		// Iterate over each pixel of the input patch.
		for(size_t i = 0; i < itotal; i++)
		{
			const auto ix = i / irows;
			const auto iy = i % irows;

			const auto ex = ix + off_x + x;
			const auto ey = iy + off_y + y;

			if(ex >= 0 && ex < ecols && ey >= 0 && ey < erows)
			{
				eptr[patch * etotal + ey + ex * erows] = pptr[patch * itotal + i];
			}
		}
	});

	return embedded;
}

//! Template function that crops a matrix around the center point.
/*!
 * \param i_matrix Matrix.
 * \param i_size Size of the cropped image.
 * \return Cropped image, which is centered around the center point. If the center is not an integer
 * value, then the center gets rounded towards the nearest upper left image pixel.
 */
template<typename T>
device_matrix<T> crop(const device_matrix<T>& i_matrix, const Size& i_size)
{
	Expects(i_matrix.rows() >= i_size.rows());
	Expects(i_matrix.cols() >= i_size.cols());

	// Upper left pixel of the output image.
	const auto y = (i_matrix.rows() - i_size.rows()) / 2;
	const auto x = (i_matrix.cols() - i_size.cols()) / 2;

	const auto irows = i_matrix.rows();
	const auto icols = i_matrix.cols();

	const auto crows = i_size.rows();
	const auto ccols = i_size.cols();

	const auto cmaj = i_matrix.col_maj();

	const auto begin = thrust::counting_iterator<size_t>{0};
	const auto end = begin + i_size.total();

	auto cropped = device_matrix<T>{i_size, cmaj};
	auto cptr = cropped.data().get();
	const auto iptr = i_matrix.data().get();

	// Iterate over all cropped image pixels.
	thrust::for_each(begin, end, [=] __device__(size_t cpx) {
		// Cropped image coordinate
		const auto cy = cmaj ? cpx % crows : cpx / ccols;
		const auto cx = cmaj ? cpx / crows : cpx % ccols;

		// i_matrix coordinate
		const auto iy = y + cy;
		const auto ix = x + cx;
		const auto ipx = cmaj ? iy + ix * irows : ix + iy * icols;

		cptr[cpx] = iptr[ipx];
	});

	return cropped;
}