/*! \file utils.h
	\brief Converting device_matrix and device_patches to/ from Python array
	\sa device_matrix.h, device_patches.h
*/

#pragma once

#include "../extern/pybind11/include/pybind11/numpy.h"
#include "../extern/pybind11/include/pybind11/pybind11.h"

namespace py = pybind11;
// Dense array types!
template<typename T>
using py_array_col_maj = py::array_t<T, py::array::f_style>;
/**< Shorthand for py::array_t<T, py::array::f_style>. */
template<typename T>
using py_array_row_maj = py::array_t<T, py::array::c_style>;
/**< Shorthand for py::array_t<T, py::array::c_style>. */

template<typename T>
struct vec3;

template<typename T>
class device_matrix;

template<typename T>
class device_patches;

//! Returns true if array represents a gray-scale image, otherwise false.
bool is_grey(const py::array& array);
//! Returns true if array represents an rgb  image, otherwise false.
bool is_rgb(const py::array& array);
//! Returns true if array represents a matrix, otherwise false.
bool is_matrix(const py::array& array);
//! Returns true if array represents a set of patches, otherwise false.
bool is_patches(const py::array& array);

//! Uploads python array to device memory.
/*!
 * \param i_matrix Python array in matrix representation, i.e., 2-dimensional or 3-dimensional with
 * third dimension of size 3 depending on overload.
 * \param tag Tag to select function overload.
 */
device_matrix<size_t> upload_matrix(const py_array_col_maj<size_t>& i_matrix, size_t tag);

/*!
 * \overload
 */
device_matrix<double> upload_matrix(const py_array_col_maj<double>& i_matrix, double tag);

/*!
 * \overload
 */
device_matrix<float> upload_matrix(const py_array_col_maj<float>& i_matrix, float tag);

/*!
 * \overload
 */
device_matrix<vec3<float>> upload_matrix(const py_array_row_maj<float>& i_matrix, vec3<float> tag);

//! Uploads python array to device memory.
/*!
 * \param i_patches Python array in patches representation, i.e., 3-dimensional or 4-dimensional
 * with fourth dimension of size 3 depending on overload.
 * \param tag Tag to select function overload.
 */
device_patches<float> upload_patches(const py_array_row_maj<float>& i_patches, float tag);

/*!
 * \overload
 */
device_patches<vec3<float>> upload_patches(const py_array_row_maj<float>& i_patches,
										   vec3<float> tag);

//! Downloads device memory to python array.
py_array_col_maj<size_t> download(const device_matrix<size_t>& i_matrix);
//! Downloads device memory to python array.
py_array_col_maj<float> download(const device_matrix<float>& i_matrix);
//! Downloads device memory to python array.
py_array_col_maj<double> download(const device_matrix<double>& i_matrix);
//! Downloads device memory to python array.
py_array_col_maj<float> download(const device_matrix<vec3<float>>& i_matrix);
//! Downloads device memory to python array.
py_array_row_maj<float> download(const device_patches<float>& i_patches);
//! Downloads device memory to python array.
py_array_row_maj<float> download(const device_patches<vec3<float>>& i_patches);