#include "../include/device_matrix.h"
#include "../include/nearest_neighbor.h"

#include "../extern/gsl/gsl_assert"

std::pair<device_matrix<size_t>, device_matrix<double>>
	nearest_neighbor_w_distances(const device_matrix<double>& i_dist_mat, const Size& i_image_size,
								 bool i_min)
{
	Expects(i_dist_mat.col_maj());
	Expects(i_dist_mat.rows() == i_image_size.total());

	const auto mat_ptr = i_dist_mat.data().get();
	const auto ld = i_dist_mat.ld();
	const auto cols = i_dist_mat.cols();

	const auto begin = thrust::counting_iterator<size_t>{0};
	const auto end = begin + i_dist_mat.rows();

	auto indices = device_matrix<size_t>{i_image_size};
	auto distances = device_matrix<double>{i_image_size};
	auto ind_ptr = indices.data().get();
	auto dist_ptr = distances.data().get();

	if(i_min) // nearest neighbor = minimum of a row
	{
		thrust::for_each(begin, end, [=] __device__(size_t row) {
			auto min = mat_ptr[row];
			auto ind = size_t{0};

			for(size_t i = 1; i < cols; i++)
			{
				const auto val = mat_ptr[row + i * ld];
				if(val < min)
				{
					min = val;
					ind = i;
				}
			}

			ind_ptr[row] = ind;
			dist_ptr[row] = min;
		});
	}
	else // nearest neighbor = maximum of a row
	{
		thrust::for_each(begin, end, [=] __device__(size_t row) {
			auto max = mat_ptr[row];
			auto ind = size_t{0};

			for(size_t i = 1; i < cols; i++)
			{
				const auto val = mat_ptr[row + i * ld];
				if(val > max)
				{
					max = val;
					ind = i;
				}
			}

			ind_ptr[row] = ind;
			dist_ptr[row] = max;
		});
	}

	return std::make_pair(std::move(indices), std::move(distances));
}

device_matrix<size_t> nearest_neighbor(const device_matrix<double>& i_dist_mat,
									   const Size& i_image_size, bool i_min)
{
	return std::get<0>(nearest_neighbor_w_distances(i_dist_mat, i_image_size, i_min));
}