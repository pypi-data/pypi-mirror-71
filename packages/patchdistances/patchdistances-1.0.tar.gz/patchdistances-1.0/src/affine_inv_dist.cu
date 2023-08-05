#include "../include/affine_inv_dist.h"
#include "../src/affine_inv_dist_impl.h"

device_matrix<double> affine_inv_dist::distance_matrix(const device_patches<float>& i_patches0,
													   const device_patches<float>& i_patches1,
													   const aid_params& i_params)
{
	return pimpl->distance_matrix(i_patches0, i_patches1, i_params);
}

device_matrix<double> affine_inv_dist::distance_matrix(const device_patches<double>& i_patches0,
													   const device_patches<double>& i_patches1,
													   const aid_params& i_params)
{
	return pimpl->distance_matrix(i_patches0, i_patches1, i_params);
}

device_matrix<double>
	affine_inv_dist::distance_matrix(const device_patches<vec3<float>>& i_patches0,
									 const device_patches<vec3<float>>& i_patches1,
									 const aid_params& i_params)
{
	return pimpl->distance_matrix(i_patches0, i_patches1, i_params);
}

device_matrix<double>
	affine_inv_dist::distance_matrix(const device_patches<vec3<double>>& i_patches0,
									 const device_patches<vec3<double>>& i_patches1,
									 const aid_params& i_params)
{
	return pimpl->distance_matrix(i_patches0, i_patches1, i_params);
}

std::pair<device_patches<float>, std::vector<size_t>>
	affine_inv_dist::greedy_k_center(const device_patches<float>& i_patches, size_t i_clusters,
									 std::size_t i_first, const aid_params& i_params)
{
	return pimpl->greedy_k_center(i_patches, i_clusters, i_first, i_params);
}

std::pair<device_patches<double>, std::vector<size_t>>
	affine_inv_dist::greedy_k_center(const device_patches<double>& i_patches, size_t i_clusters,
									 std::size_t i_first, const aid_params& i_params)
{
	return pimpl->greedy_k_center(i_patches, i_clusters, i_first, i_params);
}

std::pair<device_patches<vec3<float>>, std::vector<size_t>>
	affine_inv_dist::greedy_k_center(const device_patches<vec3<float>>& i_patches,
									 size_t i_clusters, std::size_t i_first,
									 const aid_params& i_params)
{
	return pimpl->greedy_k_center(i_patches, i_clusters, i_first, i_params);
}

std::pair<device_patches<vec3<double>>, std::vector<size_t>>
	affine_inv_dist::greedy_k_center(const device_patches<vec3<double>>& i_patches,
									 size_t i_clusters, std::size_t i_first,
									 const aid_params& i_params)
{
	return pimpl->greedy_k_center(i_patches, i_clusters, i_first, i_params);
}

std::pair<device_matrix<float>, device_matrix<size_t>>
	affine_inv_dist::reconstruct(const device_patches<float>& i_data_patches,
								 const device_patches<float>& i_labels, const Size& i_img_size,
								 rec_t i_type, const aid_params& i_params)
{
	return pimpl->reconstruct(i_data_patches, i_labels, i_img_size, i_type, i_params);
}

std::pair<device_matrix<double>, device_matrix<size_t>>
	affine_inv_dist::reconstruct(const device_patches<double>& i_data_patches,
								 const device_patches<double>& i_labels, const Size& i_img_size,
								 rec_t i_type, const aid_params& i_params)
{
	return pimpl->reconstruct(i_data_patches, i_labels, i_img_size, i_type, i_params);
}

std::pair<device_matrix<vec3<float>>, device_matrix<size_t>>
	affine_inv_dist::reconstruct(const device_patches<vec3<float>>& i_data_patches,
								 const device_patches<vec3<float>>& i_labels,
								 const Size& i_img_size, rec_t i_type, const aid_params& i_params)
{
	return pimpl->reconstruct(i_data_patches, i_labels, i_img_size, i_type, i_params);
}

std::pair<device_matrix<vec3<double>>, device_matrix<size_t>>
	affine_inv_dist::reconstruct(const device_patches<vec3<double>>& i_data_patches,
								 const device_patches<vec3<double>>& i_labels,
								 const Size& i_img_size, rec_t i_type, const aid_params& i_params)
{
	return pimpl->reconstruct(i_data_patches, i_labels, i_img_size, i_type, i_params);
}

std::pair<device_matrix<float>, device_matrix<size_t>> affine_inv_dist::reconstruct_w_translation(
	const device_patches<float>& i_data_patches, const device_patches<float>& i_labels,
	const Size& i_img_size, rec_t i_type, const aid_params& i_params)
{
	return pimpl->reconstruct_w_translation(i_data_patches, i_labels, i_img_size, i_type, i_params);
}

std::pair<device_matrix<double>, device_matrix<size_t>> affine_inv_dist::reconstruct_w_translation(
	const device_patches<double>& i_data_patches, const device_patches<double>& i_labels,
	const Size& i_img_size, rec_t i_type, const aid_params& i_params)
{
	return pimpl->reconstruct_w_translation(i_data_patches, i_labels, i_img_size, i_type, i_params);
}

std::pair<device_matrix<vec3<float>>, device_matrix<size_t>>
	affine_inv_dist::reconstruct_w_translation(const device_patches<vec3<float>>& i_data_patches,
											   const device_patches<vec3<float>>& i_labels,
											   const Size& i_img_size, rec_t i_type,
											   const aid_params& i_params)
{
	return pimpl->reconstruct_w_translation(i_data_patches, i_labels, i_img_size, i_type, i_params);
}

std::pair<device_matrix<vec3<double>>, device_matrix<size_t>>
	affine_inv_dist::reconstruct_w_translation(const device_patches<vec3<double>>& i_data_patches,
											   const device_patches<vec3<double>>& i_labels,
											   const Size& i_img_size, rec_t i_type,
											   const aid_params& i_params)
{
	return pimpl->reconstruct_w_translation(i_data_patches, i_labels, i_img_size, i_type, i_params);
}