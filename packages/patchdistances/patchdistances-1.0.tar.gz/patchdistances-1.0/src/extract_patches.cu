#include "../include/device_matrix.h"
#include "../include/device_patches.h"
#include "../include/extract_patches.h"
#include "../include/vec3.h"

#include "../extern/gsl/gsl_assert"

#include <thrust/for_each.h>
#include <thrust/iterator/counting_iterator.h>

//! A function that extracts all patches with full support from an image.
/*
 * \param i_image The input image.
 * \param i_patch_rows Row count of the extracted patches.
 * \param i_patch_cols Column count of the extracted patches.
 * \return Matrix with one patch per row. Patches are are stored in column-major format.
 */
template<typename T>
device_patches<T> extract_patches_impl(const device_matrix<T>& i_image, Rows i_patch_rows,
									   Cols i_patch_cols)
{
	Expects(i_image.col_maj()); // TODO: remove limitation
	Expects(i_patch_rows.value() <= i_image.rows());
	Expects(i_patch_cols.value() <= i_image.cols());

	const auto cols = gsl::narrow_cast<int>(i_image.cols()); // safe: small value
	const auto rows = gsl::narrow_cast<int>(i_image.rows()); // safe: small value
	const auto ld = i_image.ld();
	const auto p_rows = gsl::narrow_cast<int>(i_patch_rows.value()); // safe: small value
	const auto p_cols = gsl::narrow_cast<int>(i_patch_cols.value()); // safe: small value
	const auto sub_cols = cols - p_rows + 1; // row pixels with full support patches
	const auto sub_rows = rows - p_cols + 1; // col pixels with full support patches
	const auto p_count = sub_cols * sub_rows; // number of patches with full support
	const auto p_total = p_rows * p_cols; // elements of each patch
	const auto p_stride = sub_rows * p_total; // stride between sub_row times patches in the output
	const auto image_ptr = i_image.data().get();

	const auto p_col_maj = true;
	auto o_patches = device_patches<T>{patch_index{p_count}, i_patch_rows, i_patch_cols, p_col_maj};
	auto o_patches_ptr = o_patches.data().get();

	// Iterate over every pixel in the input image.
	const auto first = thrust::counting_iterator<std::size_t>{0};
	const auto last = first + i_image.total();

	// Each thread copies one pixel from the input image to the right position in the
	// corresponding patches.
	thrust::for_each(first, last, [=] __device__(std::size_t idx) {
		const auto row = static_cast<int>(idx % ld); // safe: small value
		const auto col = static_cast<int>(idx / ld); // safe: small value

		const auto row_begin = max(0, row - p_rows + 1);
		const auto row_end = min(sub_rows, row + 1);
		const auto col_begin = max(0, col - p_cols + 1);
		const auto col_end = min(sub_cols, col + 1);

		const auto val = image_ptr[idx];

		// pixel position in the current patch
		auto p_col_local = min(col, p_cols - 1); // max(0, col - sub_cols + 1);
		for(auto j = col_begin; j < col_end; j++)
		{
			// pixel position in the current patch
			auto p_row_local = min(row, p_rows - 1); // max(0, row - sub_rows + 1);
			for(auto i = row_begin; i < row_end; i++)
			{
				// Patches are stored continuously beginning with the first pixel with a full
				// supported patch and then following the memory layout of the input image.
				// The patches itself are stored continuously in column-major format.
				const auto p_begin = i * p_total + j * p_stride;
				const auto p_idx_local = p_row_local + p_col_local * p_rows;
				const auto p_idx = p_begin + p_idx_local;
				o_patches_ptr[p_idx] = val;

				p_row_local--;
			}

			p_col_local--;
		}
	});

	return o_patches;
}

device_patches<float> extract_patches(const device_matrix<float>& i_image, Rows i_patch_rows,
									  Cols i_patch_cols)
{
	return extract_patches_impl(i_image, i_patch_rows, i_patch_cols);
}

device_patches<float> extract_patches(const device_matrix<float>& i_image, const Size& i_patch_size)
{
	return extract_patches_impl(i_image, Rows{i_patch_size.rows()}, Cols{i_patch_size.cols()});
}

device_patches<double> extract_patches(const device_matrix<double>& i_image, Rows i_patch_rows,
									   Cols i_patch_cols)
{
	return extract_patches_impl(i_image, i_patch_rows, i_patch_cols);
}

device_patches<double> extract_patches(const device_matrix<double>& i_image,
									   const Size& i_patch_size)
{
	return extract_patches_impl(i_image, Rows{i_patch_size.rows()}, Cols{i_patch_size.cols()});
}

device_patches<vec3<float>> extract_patches(const device_matrix<vec3<float>>& i_image,
											Rows i_patch_rows, Cols i_patch_cols)
{
	return extract_patches_impl(i_image, i_patch_rows, i_patch_cols);
}

device_patches<vec3<float>> extract_patches(const device_matrix<vec3<float>>& i_image,
											const Size& i_patch_size)
{
	return extract_patches_impl(i_image, Rows{i_patch_size.rows()}, Cols{i_patch_size.cols()});
}

device_patches<vec3<double>> extract_patches(const device_matrix<vec3<double>>& i_image,
											 Rows i_patch_rows, Cols i_patch_cols)
{
	return extract_patches_impl(i_image, i_patch_rows, i_patch_cols);
}

device_patches<vec3<double>> extract_patches(const device_matrix<vec3<double>>& i_image,
											 const Size& i_patch_size)
{
	return extract_patches_impl(i_image, Rows{i_patch_size.rows()}, Cols{i_patch_size.cols()});
}