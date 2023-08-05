#include "../include/device_matrix.h"
#include "../include/device_patches.h"
#include "../include/local_nearest_neighbor.h"
#include "../include/nearest_neighbor.h"

#include "../extern/gsl/gsl_assert"
#include "../extern/gsl/gsl_util"

#include <thrust/for_each.h>
#include <thrust/iterator/counting_iterator.h>

#include <cstddef>

labeling local_nearest_neighbor(const device_matrix<double>& i_dist_mat,
								const Size& i_patches_shape, const Size& i_patch_size)
{
	Expects(i_patch_size.rows() % 2 == 1);
	Expects(i_patch_size.cols() % 2 == 1);

	const auto labels_distances = nearest_neighbor_w_distances(i_dist_mat, i_patches_shape);

	// Signed values are used to avoid unsigned underflow in the loops (See min(0, ...)).
	const auto begin = thrust::counting_iterator<int>{0};
	const auto end = begin + std::get<0>(labels_distances).total();

	// Safe because of small dimensions.
	const auto rows = gsl::narrow_cast<int>(std::get<0>(labels_distances).rows());
	const auto cols = gsl::narrow_cast<int>(std::get<0>(labels_distances).cols());
	const auto size = std::get<0>(labels_distances).size();

	const auto row_radius = gsl::narrow_cast<int>(i_patch_size.rows()) / 2;
	const auto col_radius = gsl::narrow_cast<int>(i_patch_size.cols()) / 2;

	auto labels = labeling{device_matrix<size_t>{size}, device_matrix<size_t>{size},
						   device_matrix<labeling::point>{size}};
	auto labels_ptr = labels.labels.data().get();
	auto patches_ptr = labels.patches.data().get();
	auto offsets_ptr = labels.offsets.data().get();
	const auto nn_labels_ptr = std::get<0>(labels_distances).data().get();
	const auto nn_dist_ptr = std::get<1>(labels_distances).data().get();

	// Iterate over every element in the nearest neighbor labeling and find the smallest distance in
	// the neighborhood.
	thrust::for_each(begin, end, [=] __device__(int ind) {
		const auto row = ind % rows;
		const auto col = ind / rows;

		// Given a pixel (center of an image patch). We consider all translations of a label
		// (patches), such that the label still coincides with the pixel. Additionally, near the
		// image border translation is limited, since those pixel do not correlate to image patches
		// (=are not the center of an image patch). Otherwise, after translation these may not be
		// covered anymore by a label.

		// Possible translation
		const auto row_t = min(min(row, rows - 1 - row), row_radius);
		const auto col_t = min(min(col, cols - 1 - col), col_radius);

		const auto row_begin = max(0, row - row_t);
		const auto row_end = min(rows, row + 1 + row_t);
		const auto col_begin = max(0, col - col_t);
		const auto col_end = min(cols, col + 1 + col_t);

		// Default is the coordinate of the current patch (no translation).
		auto off_rows = 0;
		auto off_cols = 0;
		auto off_ind = row + col * rows;
		auto min = nn_dist_ptr[off_ind];

		for(int j = col_begin; j < col_end; j++)
		{
			for(int i = row_begin; i < row_end; i++)
			{
				const auto loop_ind = i + j * rows;
				const auto val = nn_dist_ptr[loop_ind];
				if(val < min)
				{
					off_rows = i - row;
					off_cols = j - col;
					off_ind = loop_ind;
					min = val;
				}
			}
		}

		labels_ptr[ind] = nn_labels_ptr[off_ind];
		patches_ptr[ind] = off_ind;
		offsets_ptr[ind] = thrust::make_pair(off_cols, off_rows); // (x,y)
	});

	return labels;
}