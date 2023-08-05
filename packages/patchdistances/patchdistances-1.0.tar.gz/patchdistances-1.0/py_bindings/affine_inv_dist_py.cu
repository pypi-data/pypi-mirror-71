#include "affine_inv_dist_py.h"

#include "../include/affine_inv_dist.h"
#include "../include/device_matrix.h"
#include "../include/enums.h"
#include "../include/extract_patches.h"
#include "../src/affine_inv_dist_impl.h"
#include "utils.h"

// Instantiate destructor.
#include "../src/pimpl_impl.h"
template class pimpl<affine_inv_dist_py::impl>;

class affine_inv_dist_py::impl final
{
  public:
	py_array_col_maj<double> distance_matrix(const py_array_row_maj<float>& i_patches_0,
											 const py_array_row_maj<float>& i_patches_1,
											 const aid_params& i_params);

	std::pair<py_array_row_maj<float>, std::vector<size_t>>
		greedy_k_center(const py_array_col_maj<float>& i_image,
						const std::pair<size_t, size_t>& i_patch_size, size_t i_clusters,
						size_t i_first, const aid_params& i_params);

	std::pair<py_array_row_maj<float>, std::vector<size_t>>
		greedy_k_center(const py_array_row_maj<float>& i_patches, size_t i_clusters, size_t i_first,
						const aid_params& i_params);

	std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>>
		reconstruct(const py_array_col_maj<float>& i_image, const py_array_row_maj<float>& i_labels,
					rec_t i_type, const aid_params& i_params);

	std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>>
		reconstruct_w_translation(const py_array_col_maj<float>& i_image,
								  const py_array_row_maj<float>& i_labels, rec_t i_type,
								  const aid_params& i_params);

  private:
	affine_inv_dist m{};
};

py_array_col_maj<double>
	affine_inv_dist_py::impl::distance_matrix(const py_array_row_maj<float>& i_patches_0,
											  const py_array_row_maj<float>& i_patches_1,
											  const aid_params& i_params)
{
	if(is_grey(i_patches_0) && is_grey(i_patches_1))
	{
		return download(m.distance_matrix(upload_patches(i_patches_0, float{}),
										  upload_patches(i_patches_1, float{}), i_params));
	}
	else if(is_rgb(i_patches_0) && is_rgb(i_patches_1))
	{
		return download(m.distance_matrix(upload_patches(i_patches_0, vec3<float>{}),
										  upload_patches(i_patches_1, vec3<float>{}), i_params));
	}
	else
	{
		throw std::runtime_error{"Error in distance_matrix. Both set of patches have to be of "
								 "the same type (float, double) and either grey-scale or rgb "
								 "(rgba is not supported)."};
	}
}

std::pair<py_array_row_maj<float>, std::vector<size_t>> affine_inv_dist_py::impl::greedy_k_center(
	const py_array_col_maj<float>& i_image, const std::pair<size_t, size_t>& i_patch_size,
	size_t i_clusters, size_t i_first, const aid_params& i_params)
{
	const auto rows = Rows{std::get<0>(i_patch_size)};
	const auto cols = Cols{std::get<1>(i_patch_size)};

	if(is_grey(i_image))
	{
		const auto patches = extract_patches(upload_matrix(i_image, float{}), rows, cols);
		auto labels_ind = m.greedy_k_center(patches, i_clusters, i_first, i_params);

		return std::make_pair(download(std::move(std::get<0>(labels_ind))),
							  std::move(std::get<1>(labels_ind)));
	}
	else if(is_rgb(i_image))
	{
		const auto patches = extract_patches(upload_matrix(i_image, vec3<float>{}), rows, cols);
		auto labels_ind = m.greedy_k_center(patches, i_clusters, i_first, i_params);

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
	affine_inv_dist_py::impl::greedy_k_center(const py_array_row_maj<float>& i_patches,
											  size_t i_clusters, size_t i_first,
											  const aid_params& i_params)
{
	if(is_grey(i_patches))
	{
		auto labels_ind =
			m.greedy_k_center(upload_patches(i_patches, float{}), i_clusters, i_first, i_params);
		return std::make_pair(download(std::move(std::get<0>(labels_ind))),
							  std::move(std::get<1>(labels_ind)));
	}
	else if(is_rgb(i_patches))
	{
		auto labels_ind = m.greedy_k_center(upload_patches(i_patches, vec3<float>{}), i_clusters,
											i_first, i_params);
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
	affine_inv_dist_py::impl::reconstruct(const py_array_col_maj<float>& i_image,
										  const py_array_row_maj<float>& i_labels, rec_t i_type,
										  const aid_params& i_params)
{
	if(is_grey(i_image) && is_grey(i_labels))
	{
		const auto img = upload_matrix(i_image, float{});
		const auto labels = upload_patches(i_labels, float{});
		const auto patches = extract_patches(img, labels.size_patches());
		auto img_nn = m.reconstruct(patches, labels, img.size(), i_type, i_params);

		return std::make_pair(download(std::move(std::get<0>(img_nn))),
							  download(std::move(std::get<1>(img_nn))));
	}
	else if(is_rgb(i_image) && is_rgb(i_labels))
	{
		const auto img = upload_matrix(i_image, vec3<float>{});
		const auto labels = upload_patches(i_labels, vec3<float>{});
		const auto patches = extract_patches(img, labels.size_patches());
		auto img_nn = m.reconstruct(patches, labels, img.size(), i_type, i_params);

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
	affine_inv_dist_py::impl::reconstruct_w_translation(const py_array_col_maj<float>& i_image,
														const py_array_row_maj<float>& i_labels,
														rec_t i_type, const aid_params& i_params)
{
	if(is_grey(i_image) && is_grey(i_labels))
	{
		const auto img = upload_matrix(i_image, float{});
		const auto labels = upload_patches(i_labels, float{});
		const auto patches = extract_patches(img, labels.size_patches());
		auto img_nn = m.reconstruct_w_translation(patches, labels, img.size(), i_type, i_params);

		return std::make_pair(download(std::move(std::get<0>(img_nn))),
							  download(std::move(std::get<1>(img_nn))));
	}
	else if(is_rgb(i_image) && is_rgb(i_labels))
	{
		const auto img = upload_matrix(i_image, vec3<float>{});
		const auto labels = upload_patches(i_labels, vec3<float>{});
		const auto patches = extract_patches(img, labels.size_patches());
		auto img_nn = m.reconstruct_w_translation(patches, labels, img.size(), i_type, i_params);

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

py_array_col_maj<double> affine_inv_dist_py::distance_matrix(
	const py_array_row_maj<float>& i_patches_0, const py_array_row_maj<float>& i_patches_1,
	solver_t i_solver, func_family_t i_ff, size_t i_levels, bool i_higher_order_moments,
	bool i_imed, interpolation_t i_interpolation)
{
	auto params = aid_params{};
	params.solver = i_solver;
	params.func_family = i_ff;
	params.levels = i_levels;
	params.higher_order_moments = i_higher_order_moments;
	params.imed = i_imed;
	params.interpolation = i_interpolation;

	return pimpl->distance_matrix(i_patches_0, i_patches_1, params);
}

std::pair<py_array_row_maj<float>, std::vector<size_t>> affine_inv_dist_py::greedy_k_center_img(
	const py_array_col_maj<float>& i_image, const std::pair<size_t, size_t>& i_patch_size,
	size_t i_clusters, size_t i_first, solver_t i_solver, func_family_t i_ff, size_t i_levels,
	bool i_higher_order_moments, bool i_imed, interpolation_t i_interpolation)
{
	auto params = aid_params{};
	params.solver = i_solver;
	params.func_family = i_ff;
	params.levels = i_levels;
	params.higher_order_moments = i_higher_order_moments;
	params.imed = i_imed;
	params.interpolation = i_interpolation;

	return pimpl->greedy_k_center(i_image, i_patch_size, i_clusters, i_first, params);
}

std::pair<py_array_row_maj<float>, std::vector<size_t>> affine_inv_dist_py::greedy_k_center_patches(
	const py_array_row_maj<float>& i_patches, size_t i_clusters, size_t i_first, solver_t i_solver,
	func_family_t i_ff, size_t i_levels, bool i_higher_order_moments, bool i_imed,
	interpolation_t i_interpolation)
{
	auto params = aid_params{};
	params.solver = i_solver;
	params.func_family = i_ff;
	params.levels = i_levels;
	params.higher_order_moments = i_higher_order_moments;
	params.imed = i_imed;
	params.interpolation = i_interpolation;

	return pimpl->greedy_k_center(i_patches, i_clusters, i_first, params);
}

std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>> affine_inv_dist_py::reconstruct(
	const py_array_col_maj<float>& i_img, const py_array_row_maj<float>& i_labels, rec_t i_type,
	solver_t i_solver, func_family_t i_ff, size_t i_levels, bool i_higher_order_moments,
	bool i_imed, interpolation_t i_interpolation)
{
	auto params = aid_params{};
	params.solver = i_solver;
	params.func_family = i_ff;
	params.levels = i_levels;
	params.higher_order_moments = i_higher_order_moments;
	params.imed = i_imed;
	params.interpolation = i_interpolation;

	return pimpl->reconstruct(i_img, i_labels, i_type, params);
}

std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>>
	affine_inv_dist_py::reconstruct_w_translation(const py_array_col_maj<float>& i_img,
												  const py_array_row_maj<float>& i_labels,
												  rec_t i_type, solver_t i_solver,
												  func_family_t i_ff, size_t i_levels,
												  bool i_higher_order_moments, bool i_imed,
												  interpolation_t i_interpolation)
{
	auto params = aid_params{};
	params.solver = i_solver;
	params.func_family = i_ff;
	params.levels = i_levels;
	params.higher_order_moments = i_higher_order_moments;
	params.imed = i_imed;
	params.interpolation = i_interpolation;

	return pimpl->reconstruct_w_translation(i_img, i_labels, i_type, params);
}