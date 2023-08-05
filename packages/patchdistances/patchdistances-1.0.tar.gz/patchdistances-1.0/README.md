[![pipeline status](https://gitlab.com/a.schulze/invariant_patch_distances/badges/master/pipeline.svg)](https://gitlab.com/a.schulze/invariant_patch_distances/-/commits/master)

# Invariant patch distances and clustering

Library for clustering patches and reconstructing images using invariant patch distances.
The library also contains many general-purpose functions, which can be used for other patch based projects.
The code can be compiled to a static C++ library and python bindings.
The python bindings can also be installed using PyPI.

Doxygen generated documentation of the master branch can be found [here](https://aschulze.gitlab.io/invariant_patch_distances).

## Prerequisites

An NVIDIA graphics card of compute capability 3.x or higher, CUDA 10.0 and CMake 3.10.

## PyPI

```
pip install -U patchdistances
```

## TestPyPI for development builds

```
pip install -U --index-url https://test.pypi.org/simple/ patchdistances
```

## Building from repository

Clone the repository.
```
git clone git@gitlab.com:a.schulze/invariant_patch_distances.git
```

### C++ static library

```
mkdir build
cd build
cmake ..
make pd_static
```

### Python bindings

```
mkdir build
cd build
cmake ..
make patchdistances
```

### Unit tests

#### C++

```
mkdir build
cd build
cmake ..
make pd_tests
make test
```

#### C++ Benchmarks

```
mkdir build
cd build
cmake ..
make pd_tests
./pd_tests "[\!benchmark]"
```

#### Python

```
	pytest
```

### Example

The following examples show how to cluster patches and reconstruct an image using these clusters.

#### C++

```
// Load the image.
const std::vector<float> img_data = function_that_loads_the_image_data();
const auto img = device_matrix<float>{img_data, img_size, column_major};

// Extract all patches with full support.
const auto patches = extract_patches(img, Size{7_rows, 7_cols});

// Initialize the distance class and its parameters.
// Alternatively: similarity_inv_dist.
affine_inv_dist dist{};
constexpr auto params = []
{
	auto params = aid_params{};
	params.solver = solver_t::procrustes;
	params.func_family = func_family_t::clip;
	params.levels = 10;
	params.higher_order_moments = false;
	params.imed = false;
	params.interpolation = interpolation_t::bicubic;

	return params;
}();

// Greedy-k-center clustering of the image patches using the distance.
const auto label_count = 20;
const auto first_label = 0; // Initial patch to begin clustering with.
const auto labels_indices = dist.greedy_k_center(patches, label_count, first_label, params);
const auto labels = std::get<0>(labels_indices);
const auto indices_of_labels = std::get<1>(labels_indices);

// Reconstruct the image using the previously clustered patches.
// Alternatively: reconstruct_w_translation.
const auto image_nn = dist.reconstruct(patches, labels, img.size(), rec_t::mean, params);
const auto reconstructed_image = std::get<0>(image_nn); 
const auto nearest_neighbor_labeling = std::get<1>(image_nn); 
```

#### Python

```
import patchdistances as pd

# Load image as Float32 numpy array. It can either be gray-scale or rgb.
img = load_image()

// Initialize the distance class.
// Alternatively: similarity_inv_dist.
aid = pd.affine_inv_dist()

// Greedy-k-center clustering of the image patches using the distance.
labels, indices_of_labels = aid.greedy_k_center(
    image=img,
    patch_shape=(7,7),
    clusters=20,
    first_patch_idx=0,
    solver=pd.solver_t.procrustes,
    func_family=pd.func_t.superlevelsets,
    use_imed=False,
    interpolation=pd.inter_t.bicubic,
)

// Reconstruct the image using the previously clustered patches.
// Alternatively: reconstruct_w_translation.
reconstructed_image, nearest_neighbor_labeling = aid.reconstruct(
    image=img,
    labels=labels,
    rec_type=pd.rec_t.Median,
    solver=pd.solver_t.procrustes,
    func_family=pd.func_t.superlevelsets,
    use_imed=False,
    interpolation=pd.inter_t.bicubic,
)
```

## Built With

* [ms-gsl](https://github.com/microsoft/GSL) - Guidelines Support Library
* [pybind11](https://github.com/pybind/pybind11) - Seamless operability between C++11 and Python
* [Catch2](https://github.com/catchorg/Catch2) - A modern, C++-native, header-only, test framework for unit-tests, TDD and BDD

## Authors

* **André Schulze**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.