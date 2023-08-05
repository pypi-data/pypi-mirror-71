/*! \file affine_inv_dist_py.h
	\brief Python wrapper for the affine invariant distance affine_inv_dist
	\sa affine_inv_dist.h
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

enum class func_family_t;
enum class interpolation_t;
enum class rec_t;
enum class solver_t;

//! Python wrapper for the affine invariant distance affine_inv_dist.
class affine_inv_dist_py final
{
  public:
	//! Distance matrix of two sets of patches.
	/*!
	 * \param i_patches_0 Set of patches. A row in the output equals the distances of a patch.
	 * \param i_patches_1 Set of patches. A column in the output equals the distances of a patch.
	 * \param i_solver Method solving overdetermined linear systems.
	 * \param i_ff Type of the function family.
	 * \param i_levels Size of the function family.
	 * \param i_higher_order_moments Uf true, use higher order moments, otherwise first order
	 * moments.
	 * \param i_imed If true, use Image euclidean distance, otherwise euclidean distance.
	 * \param i_interpolation Interpolation method for the affine transformation of labels.
	 * \sa pdtype
	 */
	py_array_col_maj<double> distance_matrix(const py_array_row_maj<float>& i_patches_0,
											 const py_array_row_maj<float>& i_patches_1,
											 solver_t i_solver, func_family_t i_ff, size_t i_levels,
											 bool i_higher_order_moments, bool i_imed,
											 interpolation_t i_interpolation);

	//! Greedy-k-center clustering for an image and its patches.
	/*!
	 * \param i_image An image of which patches with fully supported patches are extracted.
	 * \param i_patch_size Size of the extracted labels and returned labels.
	 * \param i_clusters The number of clusters.
	 * \param i_first of the first center patch.
	 * \param i_solver Method solving overdetermined linear systems.
	 * \param i_ff Type of the function family.
	 * \param i_levels Size of the function family.
	 * \param i_higher_order_moments Uf true, use higher order moments, otherwise first order
	 * moments.
	 * \param i_imed If true, use Image euclidean distance, otherwise euclidean distance.
	 * \param i_interpolation Interpolation method for the affine transformation of labels.
	 * \return K patches and their indices
	 */
	std::pair<py_array_row_maj<float>, std::vector<size_t>> greedy_k_center_img(
		const py_array_col_maj<float>& i_image, const std::pair<size_t, size_t>& i_patch_size,
		size_t i_clusters, size_t i_first, solver_t i_solver, func_family_t i_ff, size_t i_levels,
		bool i_higher_order_moments, bool i_imed, interpolation_t i_interpolation);

	//! Greedy-k-center clustering for a set of patches.
	/*!
	 * \param i_patches A set of patches.
	 * \param i_clusters The number of clusters.
	 * \param i_first of the first center patch.
	 * \param i_solver Method solving overdetermined linear systems.
	 * \param i_ff Type of the function family.
	 * \param i_levels Size of the function family.
	 * \param i_higher_order_moments Uf true, use higher order moments, otherwise first order
	 * moments.
	 * \param i_imed If true, use Image euclidean distance, otherwise euclidean distance.
	 * \param i_interpolation Interpolation method for the affine transformation of labels.
	 * \return K patches and their indices
	 */
	std::pair<py_array_row_maj<float>, std::vector<size_t>>
		greedy_k_center_patches(const py_array_row_maj<float>& i_patches, size_t i_clusters,
								size_t i_first, solver_t i_solver, func_family_t i_ff,
								size_t i_levels, bool i_higher_order_moments, bool i_imed,
								interpolation_t i_interpolation);

	//! A member reconstructing an image using its fully-supported patches and a set of labels.
	/*!
	 * The input data has to lie in [0,1].
	 * \param i_image Image that will be reconstructed using the given labels.
	 * \param i_labels Smaller set with prior patches.
	 * \param i_type Pixelwise reconstruction type, i.e. median or mean.
	 * \param i_solver Method solving overdetermined linear systems.
	 * \param i_ff Type of the function family.
	 * \param i_levels Size of the function family.
	 * \param i_higher_order_moments Uf true, use higher order moments, otherwise first order
	 * moments.
	 * \param i_imed If true, use Image euclidean distance, otherwise euclidean distance.
	 * \param i_interpolation Interpolation method for the affine transformation of labels.
	 * \return Reconstructed image at position 0 and nearest neighbor at 1.
	 */
	std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>>
		reconstruct(const py_array_col_maj<float>& i_image, const py_array_row_maj<float>& i_labels,
					rec_t i_type, solver_t i_solver, func_family_t i_ff, size_t i_levels,
					bool i_higher_order_moments, bool i_imed, interpolation_t i_interpolation);

	//! A member reconstructing an image using its fully-supported patches and a set of labels.
	//! This variant allows the translation of labels around their center pixel.
	/*!
	 * The input data has to lie in [0,1].
	 * \param i_image Image that will be reconstructed using the given labels.
	 * \param i_labels Smaller set with prior patches.
	 * \param i_type Pixelwise reconstruction type, i.e. median or mean.
	 * \param i_solver Method solving overdetermined linear systems.
	 * \param i_ff Type of the function family.
	 * \param i_levels Size of the function family.
	 * \param i_higher_order_moments Uf true, use higher order moments, otherwise first order
	 * moments.
	 * \param i_imed If true, use Image euclidean distance, otherwise euclidean distance.
	 * \param i_interpolation Interpolation method for the affine transformation of labels.
	 * \return Reconstructed image at position 0 and nearest neighbor at 1.
	 */
	std::pair<py_array_col_maj<float>, py_array_col_maj<size_t>> reconstruct_w_translation(
		const py_array_col_maj<float>& i_image, const py_array_row_maj<float>& i_labels,
		rec_t i_type, solver_t i_solver, func_family_t i_ff, size_t i_levels,
		bool i_higher_order_moments, bool i_imed, interpolation_t i_interpolation);

  private:
	class impl;
	::pimpl<impl> pimpl;
};