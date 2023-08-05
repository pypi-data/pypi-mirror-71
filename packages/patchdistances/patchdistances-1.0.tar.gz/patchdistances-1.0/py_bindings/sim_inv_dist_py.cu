#include "sim_inv_dist_py.h"

#include "../include/device_matrix.h"
#include "../include/enums.h"
#include "../include/extract_patches.h"
#include "../include/sim_inv_dist.h"
#include "../src/sim_inv_dist_impl.h"
#include "utils.h"

// Instantiate destructor.
#include "../src/pimpl_impl.h"
template class pimpl<sim_inv_dist_py::impl>;

class sim_inv_dist_py::impl final
{
  public:
	py_array_col_maj<double> distance_matrix(const py_array_row_maj<float>& i_patches_0,
											 const py_array_row_maj<float>& i_patches_1,
											 size_t i_lp_size, std::pair<size_t, size_t> i_fmt_size,
											 float i_sigma);

	std::pair<py_array_row_maj<float>, std::vector<size_t>>
		greedy_k_center(const py_array_col_maj<float>& i_image,
						const std::pair<size_t, size_t>& i_patch_size, size_t i_clusters,
						size_t i_first, size_t i_lp_size, std::pair<size_t, size_t> i_fmt_size,
						float i_sigma);

	std::pair<py_array_row_maj<float>, std::vector<size_t>>
		greedy_k_center(const py_array_row_maj<float>& i_patches, size_t i_clusters, size_t i_first,
						size_t i_lp_size, std::pair<size_t, size_t> i_fmt_size, float i_sigma);

	std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>>
		reconstruct(const py_array_col_maj<float>& i_image, const py_array_row_maj<float>& i_labels,
					rec_t i_type, size_t i_lp_size, std::pair<size_t, size_t> i_fmt_size,
					float i_sigma, interpolation_t i_interpolation);

	std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>>
		reconstruct_w_translation(const py_array_col_maj<float>& i_image,
								  const py_array_row_maj<float>& i_labels, rec_t i_type,
								  size_t i_lp_size, std::pair<size_t, size_t> i_fmt_size,
								  float i_sigma, interpolation_t i_interpolation);

  private:
	sim_inv_dist m{};
};

py_array_col_maj<double> sim_inv_dist_py::impl::distance_matrix(
	const py_array_row_maj<float>& i_patches_0, const py_array_row_maj<float>& i_patches_1,
	size_t i_lp_size, std::pair<size_t, size_t> i_fmt_size, float i_sigma)
{
	const auto params = [&] {
		auto tmp = sid_params{};
		tmp.log_polar_size = i_lp_size;
		tmp.descriptors_rows = Rows{std::get<0>(i_fmt_size)};
		tmp.descriptors_cols = Cols{std::get<1>(i_fmt_size)};
		tmp.sigma = i_sigma;
		return tmp;
	}();

	if(is_grey(i_patches_0) && is_grey(i_patches_1))
	{
		return download(m.distance_matrix(upload_patches(i_patches_0, float{}),
										  upload_patches(i_patches_1, float{}), params));
	}
	else if(is_rgb(i_patches_0) && is_rgb(i_patches_1))
	{
		return download(m.distance_matrix(upload_patches(i_patches_0, vec3<float>{}),
										  upload_patches(i_patches_1, vec3<float>{}), params));
	}
	else
	{
		throw std::runtime_error{"Error in distance_matrix. Both set of patches have to be of "
								 "the same type (float, double) and either grey-scale or rgb "
								 "(rgba is not supported)."};
	}
}

std::pair<py_array_row_maj<float>, std::vector<size_t>>
	sim_inv_dist_py::impl::greedy_k_center(const py_array_col_maj<float>& i_image,
										   const std::pair<size_t, size_t>& i_patch_size,
										   size_t i_clusters, size_t i_first, size_t i_lp_size,
										   std::pair<size_t, size_t> i_fmt_size, float i_sigma)
{
	const auto rows = Rows{std::get<0>(i_patch_size)};
	const auto cols = Cols{std::get<1>(i_patch_size)};
	const auto params = [&] {
		auto tmp = sid_params{};
		tmp.log_polar_size = i_lp_size;
		tmp.descriptors_rows = Rows{std::get<0>(i_fmt_size)};
		tmp.descriptors_cols = Cols{std::get<1>(i_fmt_size)};
		tmp.sigma = i_sigma;
		return tmp;
	}();

	if(is_grey(i_image))
	{
		const auto patches = extract_patches(upload_matrix(i_image, float{}), rows, cols);
		auto labels_ind = m.greedy_k_center(patches, i_clusters, i_first, params);

		return std::make_pair(download(std::move(std::get<0>(labels_ind))),
							  std::move(std::get<1>(labels_ind)));
	}
	else if(is_rgb(i_image))
	{
		const auto patches = extract_patches(upload_matrix(i_image, vec3<float>{}), rows, cols);
		auto labels_ind = m.greedy_k_center(patches, i_clusters, i_first, params);

		return std::make_pair(download(std::move(std::get<0>(labels_ind))),
							  std::move(std::get<1>(labels_ind)));
	}
	else
	{
		throw std::runtime_error{"Error in greedy k-center. Image has to be either "
								 "grey-scale or rgb (rgba is not supported)."};
	}
}

std::pair<py_array_row_maj<float>, std::vector<size_t>>
	sim_inv_dist_py::impl::greedy_k_center(const py_array_row_maj<float>& i_patches,
										   size_t i_clusters, size_t i_first, size_t i_lp_size,
										   std::pair<size_t, size_t> i_fmt_size, float i_sigma)
{
	const auto params = [&] {
		auto tmp = sid_params{};
		tmp.log_polar_size = i_lp_size;
		tmp.descriptors_rows = Rows{std::get<0>(i_fmt_size)};
		tmp.descriptors_cols = Cols{std::get<1>(i_fmt_size)};
		tmp.sigma = i_sigma;
		return tmp;
	}();

	if(is_grey(i_patches))
	{
		auto labels_ind =
			m.greedy_k_center(upload_patches(i_patches, float{}), i_clusters, i_first, params);
		return std::make_pair(download(std::move(std::get<0>(labels_ind))),
							  std::move(std::get<1>(labels_ind)));
	}
	else if(is_rgb(i_patches))
	{
		auto labels_ind = m.greedy_k_center(upload_patches(i_patches, vec3<float>{}), i_clusters,
											i_first, params);
		return std::make_pair(download(std::move(std::get<0>(labels_ind))),
							  std::move(std::get<1>(labels_ind)));
	}
	else
	{
		throw std::runtime_error{"Error in greedy k-center. Patches have to be either "
								 "grey-scale or rgb (rgba is not supported)."};
	}
}

std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>>
	sim_inv_dist_py::impl::reconstruct(const py_array_col_maj<float>& i_image,
									   const py_array_row_maj<float>& i_labels, rec_t i_type,
									   size_t i_lp_size, std::pair<size_t, size_t> i_fmt_size,
									   float i_sigma, interpolation_t i_interpolation)
{
	const auto params = [&] {
		auto tmp = sid_params{};
		tmp.log_polar_size = i_lp_size;
		tmp.descriptors_rows = Rows{std::get<0>(i_fmt_size)};
		tmp.descriptors_cols = Cols{std::get<1>(i_fmt_size)};
		tmp.sigma = i_sigma;
		return tmp;
	}();

	if(is_grey(i_image) && is_grey(i_labels))
	{
		const auto img = upload_matrix(i_image, float{});
		const auto labels = upload_patches(i_labels, float{});
		const auto patches = extract_patches(img, labels.size_patches());
		auto img_nn = m.reconstruct(patches, labels, img.size(), i_type, params, i_interpolation);

		return std::make_pair(download(std::move(std::get<0>(img_nn))),
							  download(std::move(std::get<1>(img_nn))));
	}
	else if(is_rgb(i_image) && is_rgb(i_labels))
	{
		const auto img = upload_matrix(i_image, vec3<float>{});
		const auto labels = upload_patches(i_labels, vec3<float>{});
		const auto patches = extract_patches(img, labels.size_patches());
		auto img_nn = m.reconstruct(patches, labels, img.size(), i_type, params, i_interpolation);

		return std::make_pair(download(std::move(std::get<0>(img_nn))),
							  download(std::move(std::get<1>(img_nn))));
	}
	else
	{
		throw std::runtime_error{"Error in reconstruct. Both set of patches have to be of "
								 "the same type (float, double) and either grey-scale or rgb "
								 "(rgba is not supported)."};
	}
}

std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>>
	sim_inv_dist_py::impl::reconstruct_w_translation(const py_array_col_maj<float>& i_image,
													 const py_array_row_maj<float>& i_labels,
													 rec_t i_type, size_t i_lp_size,
													 std::pair<size_t, size_t> i_fmt_size,
													 float i_sigma, interpolation_t i_interpolation)
{
	const auto params = [&] {
		auto tmp = sid_params{};
		tmp.log_polar_size = i_lp_size;
		tmp.descriptors_rows = Rows{std::get<0>(i_fmt_size)};
		tmp.descriptors_cols = Cols{std::get<1>(i_fmt_size)};
		tmp.sigma = i_sigma;
		return tmp;
	}();

	if(is_grey(i_image) && is_grey(i_labels))
	{
		const auto img = upload_matrix(i_image, float{});
		const auto labels = upload_patches(i_labels, float{});
		const auto patches = extract_patches(img, labels.size_patches());
		auto img_nn = m.reconstruct_w_translation(patches, labels, img.size(), i_type, params,
												  i_interpolation);

		return std::make_pair(download(std::move(std::get<0>(img_nn))),
							  download(std::move(std::get<1>(img_nn))));
	}
	else if(is_rgb(i_image) && is_rgb(i_labels))
	{
		const auto img = upload_matrix(i_image, vec3<float>{});
		const auto labels = upload_patches(i_labels, vec3<float>{});
		const auto patches = extract_patches(img, labels.size_patches());
		auto img_nn = m.reconstruct_w_translation(patches, labels, img.size(), i_type, params,
												  i_interpolation);

		return std::make_pair(download(std::move(std::get<0>(img_nn))),
							  download(std::move(std::get<1>(img_nn))));
	}
	else
	{
		throw std::runtime_error{"Error in reconstruct. Both set of patches have to be of "
								 "the same type (float, double) and either grey-scale or rgb "
								 "(rgba is not supported)."};
	}
}

py_array_col_maj<double>
	sim_inv_dist_py::distance_matrix(const py_array_row_maj<float>& i_patches_0,
									 const py_array_row_maj<float>& i_patches_1, size_t i_lp_size,
									 std::pair<size_t, size_t> i_fmt_size, float i_sigma)
{
	return pimpl->distance_matrix(i_patches_0, i_patches_1, i_lp_size, i_fmt_size, i_sigma);
}

std::pair<py_array_row_maj<float>, std::vector<size_t>>
	sim_inv_dist_py::greedy_k_center_img(const py_array_col_maj<float>& i_image,
										 const std::pair<size_t, size_t>& i_patch_size,
										 size_t i_clusters, size_t i_first, size_t i_lp_size,
										 std::pair<size_t, size_t> i_fmt_size, float i_sigma)
{
	return pimpl->greedy_k_center(i_image, i_patch_size, i_clusters, i_first, i_lp_size, i_fmt_size,
								  i_sigma);
}

std::pair<py_array_row_maj<float>, std::vector<size_t>>
	sim_inv_dist_py::greedy_k_center_patches(const py_array_row_maj<float>& i_patches,
											 size_t i_clusters, size_t i_first, size_t i_lp_size,
											 std::pair<size_t, size_t> i_fmt_size, float i_sigma)
{
	return pimpl->greedy_k_center(i_patches, i_clusters, i_first, i_lp_size, i_fmt_size, i_sigma);
}

std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>>
	sim_inv_dist_py::reconstruct(const py_array_col_maj<float>& i_image,
								 const py_array_row_maj<float>& i_labels, rec_t i_type,
								 size_t i_lp_size, std::pair<size_t, size_t> i_fmt_size,
								 float i_sigma, interpolation_t i_interpolation)
{
	return pimpl->reconstruct(i_image, i_labels, i_type, i_lp_size, i_fmt_size, i_sigma,
							  i_interpolation);
}

std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>>
	sim_inv_dist_py::reconstruct_w_translation(const py_array_col_maj<float>& i_image,
											   const py_array_row_maj<float>& i_labels,
											   rec_t i_type, size_t i_lp_size,
											   std::pair<size_t, size_t> i_fmt_size, float i_sigma,
											   interpolation_t i_interpolation)
{
	return pimpl->reconstruct_w_translation(i_image, i_labels, i_type, i_lp_size, i_fmt_size,
											i_sigma, i_interpolation);
}