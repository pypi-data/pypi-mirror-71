/*! \file sim_inv_dist_py.h
	\brief Python wrapper for the similarity invariant distance sim_inv_dist
	\sa sim_inv_dist.h
*/

#pragma once

#include "../include/pimpl.h"

#include "../extern/pybind11/include/pybind11/numpy.h"
#include "../extern/pybind11/include/pybind11/pybind11.h"

#include <utility>

namespace py = pybind11;
// Dense array types!
template<typename T>
using py_array_col_maj = py::array_t<T, py::array::f_style>;
/**< Shorthand for py::array_t<T, py::array::f_style>. */
template<typename T>
using py_array_row_maj = py::array_t<T, py::array::c_style>;
/**< Shorthand for py::array_t<T, py::array::c_style>. */

enum class rec_t;
enum class interpolation_t;

//! Python wrapper for the similarity invariant distance sim_inv_dist.
class sim_inv_dist_py final
{
  public:
	//! Distance matrix of two sets of patches.
	/*!
	 * \param i_patches_0 Set of patches. A row in the output equals the distances of a patch.
	 * \param i_patches_1 Set of patches. A column in the output equals the distances of a patch.
	 * \param i_lp_size Size of the log polar interpolated patches. This has to be even and should
	 * be a power of 2.
	 * \param i_fmt_size Size (K,V) of the descriptors, such that 2K+1 <= M and 2V+1 <= M.
	 * \param i_sigma Fourier-Mellin-Coefficient.
	 * \sa pdtype
	 */
	py_array_col_maj<double> distance_matrix(const py_array_row_maj<float>& i_patches_0,
											 const py_array_row_maj<float>& i_patches_1,
											 size_t i_lp_size, std::pair<size_t, size_t> i_fmt_size,
											 float i_sigma);

	//! Greedy-k-center clustering for an image and its patches.
	/*!
	 * \param i_image An image of which patches with fully supported patches are extracted.
	 * \param i_patch_size Size of the extracted labels and returned labels.
	 * \param i_clusters The number of clusters.
	 * \param i_first Index of the first center patch.
	 * \param i_lp_size Size of the log polar interpolated patches. This has to be even and should
	 * be a power of 2.
	 * \param i_fmt_size Size (K,V) of the descriptors, such that 2K+1 <= M and 2V+1 <= M.
	 * \param i_sigma Fourier-Mellin-Coefficient.
	 * \return K patches and their indices
	 */
	std::pair<py_array_row_maj<float>, std::vector<size_t>>
		greedy_k_center_img(const py_array_col_maj<float>& i_image,
							const std::pair<size_t, size_t>& i_patch_size, size_t i_clusters,
							size_t i_first, size_t i_lp_size, std::pair<size_t, size_t> i_fmt_size,
							float i_sigma);

	//! Greedy-k-center clustering for a set of patches.
	/*!
	 * \param i_patches A set of patches.
	 * \param i_clusters The number of clusters.
	 * \param i_first Index of the first center patch.
	 * \param i_lp_size Size of the log polar interpolated patches. This has to be even and should
	 * be a power of 2.
	 * \param i_fmt_size Size (K,V) of the descriptors, such that 2K+1 <= M and 2V+1 <= M.
	 * \param i_sigma Fourier-Mellin-Coefficient.
	 * \return K patches and their indices
	 */
	std::pair<py_array_row_maj<float>, std::vector<size_t>>
		greedy_k_center_patches(const py_array_row_maj<float>& i_patches, size_t i_clusters,
								size_t i_first, size_t i_lp_size,
								std::pair<size_t, size_t> i_fmt_size, float i_sigma);

	//! A member reconstructing an image from a small set of labels.
	/*!
	 * The input data has to lie in [0,1].
	 * \param i_image Image that will be reconstructed using the given labels.
	 * \param i_labels Smaller set with prior patches.
	 * \param i_type Pixelwise reconstruction type, i.e. median or mean.
	 * \param i_lp_size Size of the log polar interpolated patches. This has to be even and should
	 * be a power of 2.
	 * \param i_fmt_size Size (K,V) of the descriptors, such that 2K+1 <= M and 2V+1 <= M.
	 * \param i_sigma Fourier-Mellin-Coefficient.
	 * \param i_interpolation Interpolation method for the affine transformation of labels.
	 * \return Reconstructed image at position 0 and nearest neighbor at 1.
	 */
	std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>>
		reconstruct(const py_array_col_maj<float>& i_image, const py_array_row_maj<float>& i_labels,
					rec_t i_type, size_t i_lp_size, std::pair<size_t, size_t> i_fmt_size,
					float i_sigma, interpolation_t i_interpolation);

	//! A member reconstructing an image from a small set of labels.
	//! This variant allows the translation of labels around their center pixels.
	/*!
	 * The input data has to lie in [0,1].
	 * \param i_image Image that will be reconstructed using the given labels.
	 * \param i_labels Smaller set with prior patches.
	 * \param i_type Pixelwise reconstruction type, i.e. median or mean.
	 * \param i_lp_size Size of the log polar interpolated patches. This has to be even and should
	 * be a power of 2.
	 * \param i_fmt_size Size (K,V) of the descriptors, such that 2K+1 <= M and 2V+1 <= M.
	 * \param i_sigma Fourier-Mellin-Coefficient.
	 * \param i_interpolation Interpolation method for the affine transformation of labels.
	 * \return Reconstructed image at position 0 and nearest neighbor at 1.
	 */
	std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>>
		reconstruct_w_translation(const py_array_col_maj<float>& i_image,
								  const py_array_row_maj<float>& i_labels, rec_t i_type,
								  size_t i_lp_size, std::pair<size_t, size_t> i_fmt_size,
								  float i_sigma, interpolation_t i_interpolation);

  private:
	class impl;
	::pimpl<impl> pimpl;
};