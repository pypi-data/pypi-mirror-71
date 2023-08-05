/*! \file affine_inv_dist.h
	\brief Affine invariant distance for patches
	\sa sim_inv_dist.h
*/

#pragma once

#include "enums.h"
#include "pimpl.h"
#include "rec_image.h"

#include <utility>
#include <vector>

template<typename T>
class device_matrix;

template<typename T>
class device_patches;

class Size;

//! Class for computing the affine invariant distance of patches. Based on UME of Hagege(2016).
class affine_inv_dist final
{
  public:
	//! A member computing the affine-invariant distance matrix between patches.
	/*!
	 * The input data has to lie in [0,1].
	 * \param i_patches0 Set of patches. Each row of the output contains the distances of one patch.
	 * \param i_patches1 Set of patches. Each column of the output contains the distances of one
	 * patch.
	 * \param i_params Parameters for the affine invariant distance.
	 * \return Distance matrix.
	 */
	device_matrix<double> distance_matrix(const device_patches<float>& i_patches0,
										  const device_patches<float>& i_patches1,
										  const aid_params& i_params = aid_params{});

	/*!
	 * \overload
	 */
	device_matrix<double> distance_matrix(const device_patches<double>& i_patches0,
										  const device_patches<double>& i_patches1,
										  const aid_params& i_params = aid_params{});

	/*!
	 * \overload
	 */
	device_matrix<double> distance_matrix(const device_patches<vec3<float>>& i_patches0,
										  const device_patches<vec3<float>>& i_patches1,
										  const aid_params& i_params = aid_params{});

	/*!
	 * \overload
	 */
	device_matrix<double> distance_matrix(const device_patches<vec3<double>>& i_patches0,
										  const device_patches<vec3<double>>& i_patches1,
										  const aid_params& i_params = aid_params{});

	//! Greedy k-center clustering.
	/*!
	 * The input data has to lie in [0,1].
	 * This function only works on linux 64 bit and device linked-code to the static cufft library.
	 * Otherwise an exception will be thrown on execution.
	 * \param i_patches Patches to cluster.
	 * \param i_clusters Number of clusters.
	 * \param i_first Patch index of first center patch.
	 * \param i_params Parameters for the affine invariant distance.
	 * \return Cluster centers and their indices.
	 */
	std::pair<device_patches<float>, std::vector<size_t>>
		greedy_k_center(const device_patches<float>& i_patches, size_t i_clusters,
						std::size_t i_first = std::size_t{0},
						const aid_params& i_params = aid_params{});

	/*!
	 * \overload
	 */
	std::pair<device_patches<double>, std::vector<size_t>>
		greedy_k_center(const device_patches<double>& i_patches, size_t i_clusters,
						std::size_t i_first = std::size_t{0},
						const aid_params& i_params = aid_params{});

	/*!
	 * \overload
	 */
	std::pair<device_patches<vec3<float>>, std::vector<size_t>>
		greedy_k_center(const device_patches<vec3<float>>& i_patches, size_t i_clusters,
						std::size_t i_first = std::size_t{0},
						const aid_params& i_params = aid_params{});

	/*!
	 * \overload
	 */
	std::pair<device_patches<vec3<double>>, std::vector<size_t>>
		greedy_k_center(const device_patches<vec3<double>>& i_patches, size_t i_clusters,
						std::size_t i_first = std::size_t{0},
						const aid_params& i_params = aid_params{});

	//! A member reconstructing an image using its fully-supported patches and a set of labels.
	/*!
	 * The input data has to lie in [0,1].
	 * \param i_data_patches Large set of data patches.
	 * \param i_labels Smaller set with prior patches.
	 * \param i_img_size Size of the reconstructed image.
	 * \param i_type Pixelwise reconstruction type, i.e. median or mean.
	 * \param i_params Parameters for the affine invariant distance.
	 * \return Reconstructed image at position 0 and nearest neighbor at 1.
	 */
	std::pair<device_matrix<float>, device_matrix<size_t>>
		reconstruct(const device_patches<float>& i_data_patches,
					const device_patches<float>& i_labels, const Size& i_img_size, rec_t i_type,
					const aid_params& i_params = aid_params{});

	/*!
	 * \overload
	 */
	std::pair<device_matrix<double>, device_matrix<size_t>>
		reconstruct(const device_patches<double>& i_data_patches,
					const device_patches<double>& i_labels, const Size& i_img_size, rec_t i_type,
					const aid_params& i_params = aid_params{});

	/*!
	 * \overload
	 */
	std::pair<device_matrix<vec3<float>>, device_matrix<size_t>>
		reconstruct(const device_patches<vec3<float>>& i_data_patches,
					const device_patches<vec3<float>>& i_labels, const Size& i_img_size,
					rec_t i_type, const aid_params& i_params = aid_params{});

	/*!
	 * \overload
	 */
	std::pair<device_matrix<vec3<double>>, device_matrix<size_t>>
		reconstruct(const device_patches<vec3<double>>& i_data_patches,
					const device_patches<vec3<double>>& i_labels, const Size& i_img_size,
					rec_t i_type, const aid_params& i_params = aid_params{});

	//! A member reconstructing an image using its fully-supported patches and a set of labels.
	//! This variant allows the translation of labels around their center pixel.
	/*!
	 * The input data has to lie in [0,1].
	 * \param i_data_patches Large set of data patches.
	 * \param i_labels Smaller set with prior patches.
	 * \param i_img_size Size of the reconstructed image.
	 * \param i_type Pixelwise reconstruction type, i.e. median or mean.
	 * \param i_params Parameters for the affine invariant distance.
	 * \return Reconstructed image at position 0 and nearest neighbor at 1.
	 */
	std::pair<device_matrix<float>, device_matrix<size_t>>
		reconstruct_w_translation(const device_patches<float>& i_data_patches,
								  const device_patches<float>& i_labels, const Size& i_img_size,
								  rec_t i_type, const aid_params& i_params);

	/*!
	 * \overload
	 */
	std::pair<device_matrix<double>, device_matrix<size_t>>
		reconstruct_w_translation(const device_patches<double>& i_data_patches,
								  const device_patches<double>& i_labels, const Size& i_img_size,
								  rec_t i_type, const aid_params& i_params);

	/*!
	 * \overload
	 */
	std::pair<device_matrix<vec3<float>>, device_matrix<size_t>>
		reconstruct_w_translation(const device_patches<vec3<float>>& i_data_patches,
								  const device_patches<vec3<float>>& i_labels,
								  const Size& i_img_size, rec_t i_type, const aid_params& i_params);

	/*!
	 * \overload
	 */
	std::pair<device_matrix<vec3<double>>, device_matrix<size_t>>
		reconstruct_w_translation(const device_patches<vec3<double>>& i_data_patches,
								  const device_patches<vec3<double>>& i_labels,
								  const Size& i_img_size, rec_t i_type, const aid_params& i_params);

  private:
	class impl;
	::pimpl<impl> pimpl;
};