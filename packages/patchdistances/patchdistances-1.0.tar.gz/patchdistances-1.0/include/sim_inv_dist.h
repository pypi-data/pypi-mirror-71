/*! \file sim_inv_dist.h
	\brief Similarity invariant distance for patches
	\sa affine_inv_dist.h
*/

#pragma once

#include "Cols.h"
#include "Rows.h"
#include "enums.h"
#include "pimpl.h"

#include <memory>
#include <vector>

struct float2;
using cuComplex = float2;
/**< Forward declaration of cuComplex. */

struct double2;
using cuDoubleComplex = double2;
/**< Forward declaration of cuDoubleComplex. */

class Size;

template<typename T>
class vec3;

template<typename T>
class device_matrix;

template<typename T>
class device_patches;

//! Class that implements a similarity invariant image distance for patches.
class sim_inv_dist final
{
  public:
	//! A member computing the affine-invariant distance matrix between patches.
	/*!
	 * The input data has to lie in [0,1].
	 * \param i_patches0 Set of patches. Each row of the output contains the distances of one patch.
	 * \param i_patches1 Set of patches. Each column of the output contains the distances of one
	 * patch.
	 * \param i_params Parameters of the similarity invariant distance.
	 * \return Distance matrix.
	 */
	device_matrix<double> distance_matrix(const device_patches<float>& i_patches0,
										  const device_patches<float>& i_patches1,
										  const sid_params& i_params = sid_params{});

	/*!
	 * \overload
	 */
	device_matrix<double> distance_matrix(const device_patches<double>& i_patches0,
										  const device_patches<double>& i_patches1,
										  const sid_params& i_params = sid_params{});

	/*!
	 * \overload
	 */
	device_matrix<double> distance_matrix(const device_patches<vec3<float>>& i_patches0,
										  const device_patches<vec3<float>>& i_patches1,
										  const sid_params& i_params = sid_params{});

	/*!
	 * \overload
	 */
	device_matrix<double> distance_matrix(const device_patches<vec3<double>>& i_patches0,
										  const device_patches<vec3<double>>& i_patches1,
										  const sid_params& i_params = sid_params{});

	//! Optimized greedy k-center clustering.
	/*!
	 * The input data has to lie in [0,1].
	 * \param i_patches Patches to cluster.
	 * \param i_clusters Number of clusters.
	 * \param i_first Patch index of first center patch.
	 * \param i_params Parameters of the similarity invariant distance.
	 * \return Indices of clusters.
	 */
	std::pair<device_patches<float>, std::vector<size_t>>
		greedy_k_center(const device_patches<float>& i_patches, size_t i_clusters,
						size_t i_first = size_t{0}, const sid_params& i_params = sid_params{});

	/*!
	 * \overload
	 */
	std::pair<device_patches<double>, std::vector<size_t>>
		greedy_k_center(const device_patches<double>& i_patches, size_t i_clusters,
						size_t i_first = size_t{0}, const sid_params& i_params = sid_params{});

	/*!
	 * \overload
	 */
	std::pair<device_patches<vec3<float>>, std::vector<size_t>>
		greedy_k_center(const device_patches<vec3<float>>& i_patches, size_t i_clusters,
						size_t i_first = size_t{0}, const sid_params& i_params = sid_params{});

	/*!
	 * \overload
	 */
	std::pair<device_patches<vec3<double>>, std::vector<size_t>>
		greedy_k_center(const device_patches<vec3<double>>& i_patches, size_t i_clusters,
						size_t i_first = size_t{0}, const sid_params& i_params = sid_params{});

	//! A member reconstructing an image using its fully-supported patches and a set of labels.
	/*!
	 * The input data has to lie in [0,1].
	 * \param i_data_patches Large set of data patches.
	 * \param i_labels Smaller set with prior patches.
	 * \param i_img_size Size of the reconstructed image.
	 * \param i_type Pixelwise reconstruction type, i.e. median or mean.
	 * \param i_params Parameters of the similarity invariant distance.
	 * \param i_interpolation Interpolation method for the affine transformation of labels.
	 * \return Reconstructed image at position 0 and nearest neighbor at 1.
	 */
	std::pair<device_matrix<float>, device_matrix<size_t>>
		reconstruct(const device_patches<float>& i_data_patches,
					const device_patches<float>& i_labels, const Size& i_img_size, rec_t i_type,
					const sid_params& i_params = sid_params{},
					interpolation_t i_interpolation = interpolation_t::bicubic);

	/*!
	 * \overload
	 */
	std::pair<device_matrix<double>, device_matrix<size_t>>
		reconstruct(const device_patches<double>& i_data_patches,
					const device_patches<double>& i_labels, const Size& i_img_size, rec_t i_type,
					const sid_params& i_params = sid_params{},
					interpolation_t i_interpolation = interpolation_t::bicubic);

	/*!
	 * \overload
	 */
	std::pair<device_matrix<vec3<float>>, device_matrix<size_t>>
		reconstruct(const device_patches<vec3<float>>& i_data_patches,
					const device_patches<vec3<float>>& i_labels, const Size& i_img_size,
					rec_t i_type, const sid_params& i_params = sid_params{},
					interpolation_t i_interpolation = interpolation_t::bicubic);

	/*!
	 * \overload
	 */
	std::pair<device_matrix<vec3<double>>, device_matrix<size_t>>
		reconstruct(const device_patches<vec3<double>>& i_data_patches,
					const device_patches<vec3<double>>& i_labels, const Size& i_img_size,
					rec_t i_type, const sid_params& i_params = sid_params{},
					interpolation_t i_interpolation = interpolation_t::bicubic);

	//! A member reconstructing an image using its fully-supported patches and a set of labels.
	//! This variant allows the translation of labels around their center pixel.
	/*!
	 * The input data has to lie in [0,1].
	 * \param i_data_patches Large set of data patches.
	 * \param i_labels Smaller set with prior patches.
	 * \param i_img_size Size of the reconstructed image.
	 * \param i_type Pixelwise reconstruction type, i.e. median or mean.
	 * \param i_params Parameters of the similarity invariant distance.
	 * \param i_interpolation Interpolation method for the affine transformation of labels.
	 * \return Reconstructed image at position 0 and nearest neighbor at 1.
	 */
	std::pair<device_matrix<float>, device_matrix<size_t>>
		reconstruct_w_translation(const device_patches<float>& i_data_patches,
								  const device_patches<float>& i_labels, const Size& i_img_size,
								  rec_t i_type, const sid_params& i_params = sid_params{},
								  interpolation_t i_interpolation = interpolation_t::bicubic);

	/*!
	 * \overload
	 */
	std::pair<device_matrix<double>, device_matrix<size_t>>
		reconstruct_w_translation(const device_patches<double>& i_data_patches,
								  const device_patches<double>& i_labels, const Size& i_img_size,
								  rec_t i_type, const sid_params& i_params = sid_params{},
								  interpolation_t i_interpolation = interpolation_t::bicubic);

	/*!
	 * \overload
	 */
	std::pair<device_matrix<vec3<float>>, device_matrix<size_t>>
		reconstruct_w_translation(const device_patches<vec3<float>>& i_data_patches,
								  const device_patches<vec3<float>>& i_labels,
								  const Size& i_img_size, rec_t i_type,
								  const sid_params& i_params = sid_params{},
								  interpolation_t i_interpolation = interpolation_t::bicubic);

	/*!
	 * \overload
	 */
	std::pair<device_matrix<vec3<double>>, device_matrix<size_t>>
		reconstruct_w_translation(const device_patches<vec3<double>>& i_data_patches,
								  const device_patches<vec3<double>>& i_labels,
								  const Size& i_img_size, rec_t i_type,
								  const sid_params& i_params = sid_params{},
								  interpolation_t i_interpolation = interpolation_t::bicubic);

	//! A member that computes the similarity transformations between two sets of patches and
	//! returns them as perspective transformations. This function is only intended to be
	//! used for unit testing.
	/*!
	 * \param i_data_patches Left hand side patches.
	 * \param i_labels Right hand hand side patches.
	 * \param i_params Parameters of the similarity invariant distance.
	 * \return Perspective transformations from patches to labels or equivalently inverse
	 * transformations from labels to patches.
	 */
	device_patches<float> perspective_transformations(const device_patches<float>& i_data_patches,
													  const device_patches<float>& i_labels,
													  const sid_params& i_params);

	/*!
	 * \overload
	 */
	device_patches<float> perspective_transformations(const device_patches<double>& i_data_patches,
													  const device_patches<double>& i_labels,
													  const sid_params& i_params);

	/*!
	 * \overload
	 */
	device_patches<float>
		perspective_transformations(const device_patches<vec3<float>>& i_data_patches,
									const device_patches<vec3<float>>& i_labels,
									const sid_params& i_params);

	/*!
	 * \overload
	 */
	device_patches<float>
		perspective_transformations(const device_patches<vec3<double>>& i_data_patches,
									const device_patches<vec3<double>>& i_labels,
									const sid_params& i_params);

	//! A member that computes the analytic Fourier-Mellin transformation for log polar interpolated
	//! patches. (Interpolation needs to be done with a radius of exp(2*pi).)
	/*!
	 * \param i_patches Quadratic image patches with even dimension.
	 * \param i_sigma Fourier-Mellin-Coefficient.
	 * \return A matrix with the afmt coefficients for each patch. It only contains one
	 * half of the actual matrix due to symmetry.
	 */
	device_patches<cuComplex> afmt(const device_patches<float>& i_patches, float i_sigma);

	/*!
	 * \overload
	 */
	device_patches<cuDoubleComplex> afmt(const device_patches<double>& i_patches, float i_sigma);

	/*!
	 * \overload
	 */
	device_patches<vec3<cuComplex>> afmt(const device_patches<vec3<float>>& i_patches,
										 float i_sigma);

	/*!
	 * \overload
	 */
	device_patches<vec3<cuDoubleComplex>> afmt(const device_patches<vec3<double>>& i_patches,
											   float i_sigma);

  protected:
	class impl;
	::pimpl<impl> pimpl; /**< Pointer to implementation. */
};