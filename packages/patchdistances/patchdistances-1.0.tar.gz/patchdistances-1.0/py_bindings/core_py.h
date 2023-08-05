/*! \file core_py.h
	\brief Debugging python interop
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

//! Identity function used for debugging.
py::array identity(const py::array& arr);