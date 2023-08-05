#include "../include/enums.h"
#include "affine_inv_dist_py.h"
#include "core_py.h"
#include "sim_inv_dist_py.h"

#include "../extern/pybind11/include/pybind11/pybind11.h"
#include "../extern/pybind11/include/pybind11/stl.h" // automatic conversion for std::vector

using namespace pybind11::literals;
using shape = std::pair<size_t, size_t>;

constexpr auto bicubic = interpolation_t::bicubic;
constexpr auto clip = func_family_t::clip;
constexpr auto least_squares = solver_t::least_squares;

PYBIND11_MODULE(patchdistances, m)
{
	m.doc() = "Library for extracting and clustering image patches with invariant distances.";

	m.def("identity", &identity, "array"_a,
		  "Unit testing: Matrix/ Patches identity. Copies data between Python, CUDA and back to "
		  "check conversion of memory layouts.");

	py::enum_<rec_t>{m, "rec_t"}.value("Median", rec_t::median).value("Mean", rec_t::mean);

	py::enum_<interpolation_t>{m, "inter_t"}
		.value("nearest_neighbor", interpolation_t::nn)
		.value("bicubic", interpolation_t::bicubic);

	py::enum_<func_family_t>{m, "func_t"}
		.value("superlevelsets", func_family_t::superlevelsets)
		.value("clip", func_family_t::clip);

	py::enum_<solver_t>{m, "solver_t"}
		.value("least_squares", solver_t::least_squares)
		.value("procrustes", solver_t::procrustes)
		.value("identity", solver_t::identity);

	py::class_<affine_inv_dist_py>(m, "affine_inv_dist")
		.def(py::init<>())
		.def("distance_matrix", &affine_inv_dist_py::distance_matrix, "patches_0"_a, "patches_1"_a,
			 "solver"_a = least_squares, "func_family"_a = clip, "func_family_size"_a = 10,
			 "higher_order_moments"_a = false, "use_imed"_a = false, "interpolation"_a = bicubic,
			 "Distance matrix for two set of patches. Distances of patches_0 are stored in rows. "
			 "Distances of patches_1 are stored in columns.")
		.def("greedy_k_center", &affine_inv_dist_py::greedy_k_center_img, "image"_a,
			 "patch_shape"_a, "clusters"_a, "first_patch_idx"_a = 0, "solver"_a = least_squares,
			 "func_family"_a = clip, "func_family_size"_a = 10, "higher_order_moments"_a = false,
			 "use_imed"_a = false, "interpolation"_a = bicubic,
			 "Greedy-k-center clustering for an image, meaning clustering all fully supported "
			 "patches.")
		.def("greedy_k_center", &affine_inv_dist_py::greedy_k_center_patches, "patches"_a,
			 "clusters"_a, "first_patch_idx"_a = 0, "solver"_a = least_squares,
			 "func_family"_a = clip, "func_family_size"_a = 10, "higher_order_moments"_a = false,
			 "use_imed"_a = false, "interpolation"_a = bicubic,
			 "Greedy-k-center clustering for a set of patches.")
		.def("reconstruct", &affine_inv_dist_py::reconstruct, "image"_a, "labels"_a,
			 "rec_type"_a = rec_t::mean, "solver"_a = least_squares, "func_family"_a = clip,
			 "func_family_size"_a = 10, "higher_order_moments"_a = false, "use_imed"_a = false,
			 "interpolation"_a = bicubic, "Reconstruction of an image using a set of labels.")
		.def("reconstruct_w_translation", &affine_inv_dist_py::reconstruct_w_translation, "image"_a,
			 "labels"_a, "rec_type"_a = rec_t::mean, "solver"_a = least_squares,
			 "func_family"_a = clip, "func_family_size"_a = 10, "higher_order_moments"_a = false,
			 "use_imed"_a = false, "interpolation"_a = bicubic,
			 "Reconstruction of an image using a set of labels. This variant allows the "
			 "translation of labels around their center pixel.")
		.def("__repr__", [](const affine_inv_dist_py& a) {
			return "Class that applies an affine invariant distance on sets of patches.";
		});

	py::class_<sim_inv_dist_py>(m, "similarity_inv_dist")
		.def(py::init<>())
		.def("distance_matrix", &sim_inv_dist_py::distance_matrix, "patches_0"_a, "patches_1"_a,
			 "log_polar_size"_a = 16, "fmt_shape"_a = shape{4, 4}, "sigma"_a = 0.5f,
			 "Distance matrix for two set of patches. Distances of patches_0 are stored in rows. "
			 "Distances of patches_1 are stored in columns.")
		.def("greedy_k_center", &sim_inv_dist_py::greedy_k_center_img, "image"_a, "patch_shape"_a,
			 "clusters"_a, "first_patch_idx"_a = 0, "log_polar_size"_a = 16,
			 "fmt_shape"_a = shape{4, 4}, "sigma"_a = 0.5f,
			 "Greedy-k-center clustering for an image, meaning clustering all fully supported "
			 "patches.")
		.def("greedy_k_center", &sim_inv_dist_py::greedy_k_center_patches, "patches"_a,
			 "clusters"_a, "first_patch_idx"_a = 0, "log_polar_size"_a = 16,
			 "fmt_shape"_a = shape{4, 4}, "sigma"_a = 0.5f,
			 "Greedy-k-center clustering for a set of patches.")
		.def("reconstruct", &sim_inv_dist_py::reconstruct, "image"_a, "labels"_a,
			 "rec_type"_a = rec_t::mean, "log_polar_size"_a = 16, "fmt_shape"_a = shape{4, 4},
			 "sigma"_a = 0.5f, "interpolation"_a = bicubic,
			 "Reconstruction of an image using a set of labels.")
		.def("reconstruct_w_translation", &sim_inv_dist_py::reconstruct_w_translation, "image"_a,
			 "labels"_a, "rec_type"_a = rec_t::mean, "log_polar_size"_a = 16,
			 "fmt_shape"_a = shape{4, 4}, "sigma"_a = 0.5f, "interpolation"_a = bicubic,
			 "Reconstruction of an image using a set of labels. This variant allows the "
			 "translation of labels around their center pixel.")
		.def("__repr__", [](const sim_inv_dist_py& a) {
			return "Class that applies an similarity invariant distance on sets of patches.";
		});
}