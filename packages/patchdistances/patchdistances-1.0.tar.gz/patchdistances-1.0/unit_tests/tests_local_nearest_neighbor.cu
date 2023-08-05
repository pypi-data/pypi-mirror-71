// Has to be visible to catch.
#include <ostream>
#include <thrust/pair.h>
std::ostream& operator<<(std::ostream& os, const thrust::pair<int, int>& value)
{
	os << "(" << value.first << "," << value.second << ")";
	return os;
}

#define CATCH_CONFIG_ENABLE_BENCHMARKING

#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_patches.h"
#include "../include/local_nearest_neighbor.h"
#include "../include/utils.h"
#include "utils.h"

#include <thrust/device_vector.h>

#include <vector>

TEST_CASE("Local nearest neighbor", "[local_nearest_neighbour]")
{
	// The number of image patches (patch_count) is determined by img_size and patch_size.
	const auto patches_shape = Size{3_rows, 3_cols}; // Number of image patches (with full support).
	const auto patch_size = Size{3_rows, 3_cols};
	const auto patch_count = Size{3_rows, 3_cols};
	const auto rows = 9_rows; // Number of image patches (with full support) (=patch_count).
	const auto cols = 2_cols; // Number of labels.
	const auto col_maj = true;

	// Data of the distance matrix. Each column represents the distances of a label to all image
	// patches. The distances are chosen such that the neighborhood computation can be checked at
	// the border and the center and is unique.
	const auto distance_data = std::vector<double>{
		0.8, 1.0, 1.0, 1.0, 3.0, 1.0, 1.0, 1.0, 1.0, // label 0
		2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.9, // label 1
	};

	const auto labels_data = std::vector<size_t>{0, 0, 0, 0, 0, 1, 0, 1, 1};
	const auto patches_data = std::vector<size_t>{0, 0, 2, 0, 0, 8, 6, 8, 8};

	const auto distance_mat = device_matrix<double>{distance_data, rows, cols, col_maj};
	const auto solution_labels = device_matrix<size_t>{labels_data, patch_count, col_maj};
	const auto solution_patches = device_matrix<size_t>{patches_data, patch_count, col_maj};

	const auto labels = local_nearest_neighbor(distance_mat, patches_shape, patch_size);

	const auto eps = 0.0;
	const auto margin = 0.0;
	is_equal(labels.labels, solution_labels, eps, margin);
	is_equal(labels.patches, solution_patches, eps, margin);

	// is_equal() can no be applied to labels.offsets.
	// Note that for the current dimensions the centered patches are given by (1,1).
	using point = thrust::pair<int, int>;
	REQUIRE(labels.offsets.size() == patch_size);
	CHECK(point{labels.offsets.at(0_rows, 0_cols)} == point{0, 0});
	CHECK(point{labels.offsets.at(1_rows, 0_cols)} == point{0, -1});
	CHECK(point{labels.offsets.at(2_rows, 0_cols)} == point{0, 0});
	CHECK(point{labels.offsets.at(0_rows, 1_cols)} == point{-1, 0});
	CHECK(point{labels.offsets.at(1_rows, 1_cols)} == point{-1, -1});
	CHECK(point{labels.offsets.at(2_rows, 1_cols)} == point{1, 0});
	CHECK(point{labels.offsets.at(0_rows, 2_cols)} == point{0, 0});
	CHECK(point{labels.offsets.at(1_rows, 2_cols)} == point{0, 1});
	CHECK(point{labels.offsets.at(2_rows, 2_cols)} == point{0, 0});
}

TEST_CASE("Local nearest neighbor labeling (benchmark)", "[local_nearest_neighbor][!benchmark]")
{
	const auto rows = Rows{PATCH_COUNT_BENCHMARK.value()};
	const auto cols = Cols{LABEL_COUNT_BENCHMARK.value()};
	const auto matrix = rand_matrix(Size{rows, cols}, double{});

	BENCHMARK("Nearest neighbor")
	{
		return local_nearest_neighbor(matrix, PATCH_COUNT_SIZE_BENCHMARK, PATCH_SIZE_BENCHMARK);
	};
}