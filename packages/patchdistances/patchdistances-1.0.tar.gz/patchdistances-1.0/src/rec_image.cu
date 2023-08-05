#include "../include/device_matrix.h"
#include "../include/enums.h"
#include "../include/partition_NA.h"
#include "../include/quickselect.h"
#include "../include/rec_image.h"
#include "../include/utils.h"

#include "../extern/gsl/gsl_assert"

#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#include <thrust/device_vector.h>
#include <thrust/extrema.h>
#include <thrust/sequence.h>

//! A CUDA kernel that copies the projected patch pixels for each image pixel to a matrix.
/*!
 * BlockDim * GridDim >= i_cols_assigned * i_rows_assigned.
 * \param i_labels_idx The assigned label for each pixel. The size is
 * i_cols_assigned * i_rows_assigned.
 * \param i_cols_assigned The number of fully supported patches in column direction extracted from
 * the original image.
 * \param i_rows_assigned The number of fully supported patches in row direction extracted from
 * the original image.
 * \param i_labels The prototypical labels. Patches need to be stored continuously.
 * \param i_labels_cols Number of elements of one patch of i_labels.
 * \param i_labels_rows Number of labels in i_labels.
 * \param o_projection Contains the projected points for each image pixel. It is assumed that
 * i_labels_idx contains only the assigned labels for patches with a full support in the original
 * image. Thus this memory needs to be of size (i_cols_assigned + i_cols_patch - 1) *
 * (i_rows_assigned + i_rows_patch - 1) * max_proj_px. The output is row-major, where each row
 * contains the projected points for each pixel of the reconstructed image.
 */
template<typename T>
__global__ void copy_patches(const size_t* __restrict__ i_labels_idx, unsigned int i_cols_assigned,
							 unsigned int i_rows_assigned, const T* __restrict__ i_labels,
							 unsigned int i_labels_cols, unsigned int i_labels_rows,
							 T* __restrict__ o_projection)
{
	// Label index.
	const auto tid = threadIdx.x + blockIdx.x * blockDim.x;

	if(tid < i_cols_assigned * i_rows_assigned)
	{
		const auto i_off = i_labels_idx[tid] * i_labels_cols * i_labels_rows;
		const auto rows_img = i_rows_assigned + i_labels_rows - 1;

		// Pixel position in the original image that coincides with the upper left patch pixel.
		const auto px0_col = tid / i_rows_assigned;
		const auto px0_row = tid % i_rows_assigned;

		const auto max_proj_px =
			min(i_cols_assigned, i_labels_cols) * min(i_rows_assigned, i_labels_rows);

		// Copy the pixels of a fixed patch to the correct location of the projection.
		// Labels are stored column-major.
		auto label_px_idx = size_t{0};
		for(size_t j = 0; j < i_labels_cols; j++)
		{
			const auto px_col = px0_col + j;

			for(size_t i = 0; i < i_labels_rows; i++)
			{
				const auto px_row = px0_row + i;
				const auto img_px_idx = px_row + px_col * rows_img;
				const auto proj_row = img_px_idx * max_proj_px;
				const auto proj_idx = proj_row + (label_px_idx % max_proj_px);

				o_projection[proj_idx] = i_labels[i_off + label_px_idx];

				label_px_idx += 1;
			}
		}
	}
}

//! A function that collects in each row the pixel of every patch intersecting in the same pixel.
/*!
 * \param i_labels_idx The assigned label for each pixel.
 * \param i_labels The prototypical labels.
 * \return Matrix with projected patch values for one pixel in each row. Row size is (i_labels_idx +
 * size of labels). Row-major.
 */
template<typename T>
device_matrix<T> get_proj_points(const device_matrix<size_t>& i_labels_idx,
								 const device_patches<T>& i_labels)
{
	Expects(i_labels_idx.col_maj());
	Expects(i_labels.col_maj_patches());
	Expects(i_labels.patch_count() > 0);
	Expects(i_labels.total_per_patch() > 0);
	Expects(i_labels_idx.cols() > 0);
	Expects(i_labels_idx.rows() > 0);
	Expects(*thrust::max_element(i_labels_idx.cbegin(), i_labels_idx.cend()) <
			i_labels.patch_count());

	const auto cols_patch = gsl::narrow<unsigned int>(i_labels.cols_patches());
	const auto rows_patch = gsl::narrow<unsigned int>(i_labels.rows_patches());
	const auto cols_assigned = gsl::narrow<unsigned int>(i_labels_idx.cols());
	const auto rows_assigned = gsl::narrow<unsigned int>(i_labels_idx.rows());

	// This formula holds for any image and patch size!
	const auto cols_img = cols_assigned + cols_patch - 1;
	const auto rows_img = rows_assigned + rows_patch - 1;

	const auto max_proj_px =
		std::min(cols_assigned, cols_patch) * std::min(rows_assigned, rows_patch);
	const auto row_maj = false;
	auto proj =
		device_matrix<T>{Rows{cols_img * rows_img}, Cols{max_proj_px}, T{details::NA}, row_maj};

	const auto blockDim = dim3{1024};
	const auto gridDim = dim3{gsl::narrow<unsigned int>(i_labels_idx.total() / 1024 + 1)};

	copy_patches<<<gridDim, blockDim>>>(i_labels_idx.data().get(), cols_assigned, rows_assigned,
										i_labels.data().get(), cols_patch, rows_patch,
										proj.data().get());

	check(cudaDeviceSynchronize(), cudaSuccess);

	return proj;
}

template<typename T>
__device__ T mean(const T* ptr, size_t size)
{
	auto sum = T{0};
	for(size_t i = 0; i < size; i++)
	{
		sum += ptr[i];
	}

	return sum / static_cast<T>(size);
}

template<typename T>
__device__ vec3<T> mean(const vec3<T>* ptr, size_t size)
{
	auto sum = vec3<T>{0};
	for(size_t i = 0; i < size; i++)
	{
		sum += ptr[i];
	}

	return sum / static_cast<T>(size);
}

template<typename T>
device_matrix<T> rec_image_impl(const device_matrix<size_t>& i_labels_idx,
								const device_patches<T>& i_labels, rec_t i_type)
{
	if(i_type != rec_t::median && i_type != rec_t::mean)
	{
		std::runtime_error("Error in function rec_image. Reconstruction type is not supported.");
		return device_matrix<T>{Rows{}, Cols{}}; // Otherwise nvcc is complaining.
	}

	auto proj = get_proj_points(i_labels_idx, i_labels);
	Ensures(!proj.col_maj()); // continuous rows/ projected points

	const auto img_rows = i_labels_idx.rows() + i_labels.rows_patches() - 1;
	const auto img_cols = i_labels_idx.cols() + i_labels.cols_patches() - 1;
	auto img = device_matrix<T>{Rows{img_rows}, Cols{img_cols}, i_labels_idx.col_maj()};
	auto img_ptr = img.data().get();
	auto proj_ptr = proj.data().get();
	const auto proj_cols = gsl::narrow<int>(proj.cols());
	const auto row_stride = proj.ld();
	const auto begin = thrust::counting_iterator<size_t>{0};
	const auto end = begin + proj.rows();

	// Iterate over each row of the projection/ each pixel in the reconstructed image.
	if(i_type == rec_t::median)
	{
		thrust::for_each(begin, end, [=] __device__(size_t idx) {
			const auto offset = idx * row_stride;
			const auto n_size = partition_NA(proj_ptr + offset, proj_cols);

			img_ptr[idx] = quickselect(proj_ptr + offset, n_size, n_size / 2);
			if(n_size % 2 == 0)
			{
				img_ptr[idx] =
					0.5 * (img_ptr[idx] + quickselect(proj_ptr + offset, n_size, n_size / 2 - 1));
			}
		});
	}
	else if(i_type == rec_t::mean)
	{
		thrust::for_each(begin, end, [=] __device__(size_t idx) {
			const auto offset = idx * row_stride;
			const auto n_size = partition_NA(proj_ptr + offset, proj_cols);
			img_ptr[idx] = mean(proj_ptr + offset, n_size);
		});
	}
	else
	{
		throw std::runtime_error{"Error in rec_image_impl: Reconstruction type not supported."};
	}

	return img;
}

template<typename T>
device_matrix<T> rec_image_impl(const device_patches<T>& i_labels, const Size& i_img_size,
								rec_t i_type)
{
	const auto labels_idx = [i_img_size, &i_labels] {
		const auto labels_size = patch_count_size(i_img_size, i_labels.size_patches());

		Expects(i_labels.patch_count() == labels_size.total());

		return device_matrix<std::size_t>{d_seq(i_labels.patch_count()), Rows{labels_size.rows()},
										  Cols{labels_size.cols()}};
	}();

	return rec_image_impl(labels_idx, i_labels, i_type);
}

/*
 * template instantiations
 */

device_matrix<float> rec_image(const device_matrix<size_t>& i_labels_idx,
							   const device_patches<float>& i_labels, rec_t i_type)
{
	return rec_image_impl(i_labels_idx, i_labels, i_type);
}

device_matrix<double> rec_image(const device_matrix<size_t>& i_labels_idx,
								const device_patches<double>& i_labels, rec_t i_type)
{
	return rec_image_impl(i_labels_idx, i_labels, i_type);
}

device_matrix<vec3<float>> rec_image(const device_matrix<size_t>& i_labels_idx,
									 const device_patches<vec3<float>>& i_labels, rec_t i_type)
{
	return rec_image_impl(i_labels_idx, i_labels, i_type);
}

device_matrix<vec3<double>> rec_image(const device_matrix<size_t>& i_labels_idx,
									  const device_patches<vec3<double>>& i_labels, rec_t i_type)
{
	return rec_image_impl(i_labels_idx, i_labels, i_type);
}

device_matrix<float> rec_image(const device_patches<float>& i_labels, const Size& i_img_size,
							   rec_t i_type)
{
	return rec_image_impl(i_labels, i_img_size, i_type);
}

device_matrix<double> rec_image(const device_patches<double>& i_labels, const Size& i_img_size,
								rec_t i_type)
{
	return rec_image_impl(i_labels, i_img_size, i_type);
}

device_matrix<vec3<float>> rec_image(const device_patches<vec3<float>>& i_labels,
									 const Size& i_img_size, rec_t i_type)
{
	return rec_image_impl(i_labels, i_img_size, i_type);
}

device_matrix<vec3<double>> rec_image(const device_patches<vec3<double>>& i_labels,
									  const Size& i_img_size, rec_t i_type)
{
	return rec_image_impl(i_labels, i_img_size, i_type);
}