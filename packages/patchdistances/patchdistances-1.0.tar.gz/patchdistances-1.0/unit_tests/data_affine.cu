#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_matrix.h"
#include "../include/device_patches.h"
#include "../include/vec3.h"
#include "data_affine.h"

#include <vector>

namespace data_affine
{
/*
 ** Patches which are common to multiple functions.
 */
const auto patch_base = std::vector<float>{
	0.0, 0.0, 0.0, 0.0, // col 0
	0.0, 0.0, 0.0, 0.0, // col 1
	0.0, 0.1, 0.8, 0.0, // col 2
	0.0, 0.6, 0.3, 0.0, // col 3
	0.0, 0.0, 0.0, 0.0, // col 4
	0.0, 0.0, 0.0, 0.0, // col 5
};
// scaling by 2 in x-direction
const auto patch_x2 = std::vector<float>{
	0.0, 0.1, 0.8, 0.0, // col 0
	0.0, 0.1, 0.8, 0.0, // col 1
	0.0, 0.1, 0.8, 0.0, // col 2
	0.0, 0.6, 0.3, 0.0, // col 3
	0.0, 0.6, 0.3, 0.0, // col 4
	0.0, 0.6, 0.3, 0.0, // col 5
};
// scaling by 2 in y-direction
const auto patch_y2 = std::vector<float>{
	0.0, 0.0, 0.0, 0.0, // col 0
	0.0, 0.0, 0.0, 0.0, // col 1
	0.1, 0.1, 0.8, 0.8, // col 2
	0.6, 0.6, 0.3, 0.3, // col 3
	0.0, 0.0, 0.0, 0.0, // col 4
	0.0, 0.0, 0.0, 0.0, // col 5
};
// translation in x-direction
const auto patch_xt = std::vector<float>{
	0.0, 0.1, 0.8, 0.0, // col 0
	0.0, 0.6, 0.3, 0.0, // col 1
	0.0, 0.0, 0.0, 0.0, // col 2
	0.0, 0.0, 0.0, 0.0, // col 3
	0.0, 0.0, 0.0, 0.0, // col 4
	0.0, 0.0, 0.0, 0.0, // col 5
};
// translation in y-direction
const auto patch_yt = std::vector<float>{
	0.0, 0.0, 0.0, 0.0, // col 0
	0.0, 0.0, 0.0, 0.0, // col 1
	0.0, 0.0, 0.1, 0.8, // col 2
	0.0, 0.0, 0.6, 0.3, // col 3
	0.0, 0.0, 0.0, 0.0, // col 4
	0.0, 0.0, 0.0, 0.0, // col 5
};
const auto patch_0 = std::vector<float>(patch_base.size(), 0.0);

device_patches<float> patches_lhs()
{
	auto data = patch_base;
	data.insert(data.end(), patch_base.cbegin(), patch_base.cend());
	data.insert(data.end(), patch_base.cbegin(), patch_base.cend());
	data.insert(data.end(), patch_base.cbegin(), patch_base.cend());
	data.insert(data.end(), patch_base.cbegin(), patch_base.cend());
	data.insert(data.end(), patch_base.cbegin(), patch_base.cend());

	return device_patches<float>{data, 6_patches, 4_rows, 6_cols};
}

device_patches<float> patches_rhs()
{
	auto data = patch_base;
	data.insert(data.end(), patch_x2.cbegin(), patch_x2.cend());
	data.insert(data.end(), patch_y2.cbegin(), patch_y2.cend());
	data.insert(data.end(), patch_xt.cbegin(), patch_xt.cend());
	data.insert(data.end(), patch_yt.cbegin(), patch_yt.cend());
	data.insert(data.end(), patch_0.cbegin(), patch_0.cend());

	return device_patches<float>{data, 6_patches, 4_rows, 6_cols};
}

//! Perspective transformations between the test patches.
device_patches<float> perspective_matrices()
{
	const auto row_maj = false;
	const auto data = std::vector<float>{
		// projective matrix
		1.0, 0.0, 0.0,	0.0, 1.0, 0.0,	0.0, 0.0, 1.0, // identity
		3.0, 0.0, -5.0, 0.0, 1.0, 0.0,	0.0, 0.0, 1.0, // scaling in x-direction
		1.0, 0.0, 0.0,	0.0, 2.0, -1.5, 0.0, 0.0, 1.0, // scaling in y-direction
		1.0, 0.0, -2.0, 0.0, 1.0, 0.0,	0.0, 0.0, 1.0, // translation in x-direction
		1.0, 0.0, 0.0,	0.0, 1.0, 1.0,	0.0, 0.0, 1.0, // translation in y-direction
		1.0, 0.0, 0.0,	0.0, 1.0, 0.0,	0.0, 0.0, 1.0, // identity
	};

	return device_patches<float>{data, 6_patches, 3_rows, 3_cols, row_maj};
}

void distance_matrix(const device_matrix<double>& dist_mat, double margin_low, double margin_high)
{
	REQUIRE(dist_mat.rows() == 6);
	REQUIRE(dist_mat.cols() == 6);

	CHECK(dist_mat.at(0_rows, 0_cols) == Approx{0.0}.margin(margin_low)); // id - id
	CHECK(dist_mat.at(1_rows, 0_cols) == Approx{0.0}.margin(margin_low)); // id - id
	CHECK(dist_mat.at(2_rows, 0_cols) == Approx{0.0}.margin(margin_low)); // id - id
	CHECK(dist_mat.at(3_rows, 0_cols) == Approx{0.0}.margin(margin_low)); // id - id
	CHECK(dist_mat.at(3_rows, 0_cols) == Approx{0.0}.margin(margin_low)); // id - id
	CHECK(dist_mat.at(3_rows, 0_cols) == Approx{0.0}.margin(margin_low)); // id - id

	CHECK(dist_mat.at(0_rows, 1_cols) == Approx{0.0}.margin(margin_low)); // id - scaling in x
	CHECK(dist_mat.at(1_rows, 1_cols) == Approx{0.0}.margin(margin_low)); // id - scaling in x
	CHECK(dist_mat.at(2_rows, 1_cols) == Approx{0.0}.margin(margin_low)); // id - scaling in x
	CHECK(dist_mat.at(3_rows, 1_cols) == Approx{0.0}.margin(margin_low)); // id - scaling in x
	CHECK(dist_mat.at(3_rows, 1_cols) == Approx{0.0}.margin(margin_low)); // id - scaling in x
	CHECK(dist_mat.at(3_rows, 1_cols) == Approx{0.0}.margin(margin_low)); // id - scaling in x

	CHECK(dist_mat.at(0_rows, 2_cols) == Approx{0.0}.margin(margin_low)); // id - scaling in y
	CHECK(dist_mat.at(1_rows, 2_cols) == Approx{0.0}.margin(margin_low)); // id - scaling in y
	CHECK(dist_mat.at(2_rows, 2_cols) == Approx{0.0}.margin(margin_low)); // id - scaling in y
	CHECK(dist_mat.at(3_rows, 2_cols) == Approx{0.0}.margin(margin_low)); // id - scaling in y
	CHECK(dist_mat.at(3_rows, 2_cols) == Approx{0.0}.margin(margin_low)); // id - scaling in y
	CHECK(dist_mat.at(3_rows, 2_cols) == Approx{0.0}.margin(margin_low)); // id - scaling in y

	CHECK(dist_mat.at(0_rows, 3_cols) == Approx{0.0}.margin(margin_low)); // id - translation in x
	CHECK(dist_mat.at(1_rows, 3_cols) == Approx{0.0}.margin(margin_low)); // id - translation in x
	CHECK(dist_mat.at(2_rows, 3_cols) == Approx{0.0}.margin(margin_low)); // id - translation in x
	CHECK(dist_mat.at(3_rows, 3_cols) == Approx{0.0}.margin(margin_low)); // id - translation in x
	CHECK(dist_mat.at(3_rows, 3_cols) == Approx{0.0}.margin(margin_low)); // id - translation in x
	CHECK(dist_mat.at(3_rows, 3_cols) == Approx{0.0}.margin(margin_low)); // id - translation in x

	CHECK(dist_mat.at(0_rows, 4_cols) == Approx{0.0}.margin(margin_low)); // id - translation in y
	CHECK(dist_mat.at(1_rows, 4_cols) == Approx{0.0}.margin(margin_low)); // id - translation in y
	CHECK(dist_mat.at(2_rows, 4_cols) == Approx{0.0}.margin(margin_low)); // id - translation in y
	CHECK(dist_mat.at(3_rows, 4_cols) == Approx{0.0}.margin(margin_low)); // id - translation in y
	CHECK(dist_mat.at(3_rows, 4_cols) == Approx{0.0}.margin(margin_low)); // id - translation in y
	CHECK(dist_mat.at(3_rows, 4_cols) == Approx{0.0}.margin(margin_low)); // id - translation in y

	CHECK(dist_mat.at(0_rows, 5_cols) > margin_high); // rot - zero
	CHECK(dist_mat.at(1_rows, 5_cols) > margin_high); // rot - zero
	CHECK(dist_mat.at(2_rows, 5_cols) > margin_high); // rot - zero
	CHECK(dist_mat.at(3_rows, 5_cols) > margin_high); // rot - zero
	CHECK(dist_mat.at(3_rows, 5_cols) > margin_high); // rot - zero
	CHECK(dist_mat.at(3_rows, 5_cols) > margin_high); // rot - zero
}
} // namespace data_affine