#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_matrix.h"
#include "../include/device_patches.h"
#include "../include/utils.h"
#include "../include/vec3.h"
#include "data_orthogonal.h"

#include <vector>

namespace data_orthogonal
{
/*
 ** Patches which are common to multiple functions.
 */
template<typename Float>
auto patch_base(Float /*tag*/)
{
	return std::vector<Float>{
		1.0,  1.0, 0.4,	 1.0, 0.0, // col 0
		1.0,  1.0, 1.0,	 1.0, 1.0, // col 1
		0.25, 0.5, 1.0,	 0.2, 1.0, // col 2
		1.0,  0.3, 1.0,	 1.0, 0.0, // col 3
		1.0,  1.0, 0.15, 1.0, 0.0, // col 4
	};
}
// rotation by -90 deg
template<typename Float>
auto patch90(Float /*tag*/)
{
	return std::vector<Float>{
		0.0, 1.0, 1.0,	0.0, 0.0, // col 0
		1.0, 1.0, 0.2,	1.0, 1.0, // col 1
		0.4, 1.0, 1.0,	1.0, 0.15, // col 2
		1.0, 1.0, 0.5,	0.3, 1.0, // col 3
		1.0, 1.0, 0.25, 1.0, 1.0, // col 4
	};
}
// rotation by -180 deg
template<typename Float>
auto patch180(Float /*tag*/)
{
	return std::vector<Float>{
		0.0, 1.0, 0.15, 1.0, 1.0, // col 0
		0.0, 1.0, 1.0,	0.3, 1.0, // col 1
		1.0, 0.2, 1.0,	0.5, 0.25, // col 2
		1.0, 1.0, 1.0,	1.0, 1.0, // col 3
		0.0, 1.0, 0.4,	1.0, 1.0, // col 4
	};
}
// rotation by -270 deg
template<typename Float>
auto patch270(Float /*tag*/)
{
	return std::vector<Float>{
		1.0,  1.0, 0.25, 1.0, 1.0, // col 0
		1.0,  0.3, 0.5,	 1.0, 1.0, // col 1
		0.15, 1.0, 1.0,	 1.0, 0.4, // col 2
		1.0,  1.0, 0.2,	 1.0, 1.0, // col 3
		0.0,  0.0, 1.0,	 1.0, 0.0, // col 4
	};
}
// reflection along y-axis
template<typename Float>
auto patch_yr(Float /*tag*/)
{
	return std::vector<Float>{
		1.0,  1.0, 0.15, 1.0, 0.0, // col 0
		1.0,  0.3, 1.0,	 1.0, 0.0, // col 1
		0.25, 0.5, 1.0,	 0.2, 1.0, // col 2
		1.0,  1.0, 1.0,	 1.0, 1.0, // col 3
		1.0,  1.0, 0.4,	 1.0, 0.0 // col4
	};
}

template<typename Float>
auto patch_base_moments(Float /*tag*/, bool high)
{
	const auto m_high = std::vector<Float>{
		5.35,	9.8,   13.8,	17.8, // col 0
		-0.225, -0.6,  -0.85,	-1.1, // col 1
		-0.775, -1.3,  -1.675,	-2.05, // col 2
		2.4625, 4.625, 6.625,	8.625, // col 3
		-0.125, -0.2,  -0.2625, -0.325, // col 4
		-0.125, -0.2,  -0.2625, -0.325, // col 5
		2.3625, 4.375, 6.3125,	8.25, // col 6
	};

	return high ? m_high : std::vector<Float>(m_high.cbegin(), m_high.cbegin() + 12);
}
template<typename Float>
auto patch90_moments(Float /*tag*/, bool high)
{
	const auto m_high = std::vector<Float>{
		5.35,	9.8,   13.8,   17.8, // col 0
		0.775,	1.3,   1.675,  2.05, // col 1
		-0.225, -0.6,  -0.85,  -1.1, // col 2
		2.3625, 4.375, 6.3125, 8.25, // col 3
		0.125,	0.2,   0.2625, 0.325, // col 4
		0.125,	0.2,   0.2625, 0.325, // col 5
		2.4625, 4.625, 6.625,  8.625, // col 6
	};

	return high ? m_high : std::vector<Float>(m_high.cbegin(), m_high.cbegin() + 12);
}
template<typename Float>
auto patch_yr_moments(Float /*tag*/, bool high)
{
	const auto m_high = std::vector<Float>{
		5.35,	9.8,   13.8,   17.8, // col 0
		0.225,	0.6,   0.85,   1.1, // col 1
		-0.775, -1.3,  -1.675, -2.05, // col 2
		2.4625, 4.625, 6.625,  8.625, // col 3
		0.125,	0.2,   0.2625, 0.325, // col 4
		0.125,	0.2,   0.2625, 0.325, // col 5
		2.3625, 4.375, 6.3125, 8.25, // col 6
	};

	return high ? m_high : std::vector<Float>(m_high.cbegin(), m_high.cbegin() + 12);
}

template<typename Float, typename = std::enable_if_t<std::is_floating_point<Float>::value>>
device_patches<Float> patches_lhs_impl(Float tag)
{
	const auto patch = patch_base(tag);
	auto data = patch;
	data.insert(data.end(), patch.cbegin(), patch.cend());
	data.insert(data.end(), patch.cbegin(), patch.cend());
	data.insert(data.end(), patch.cbegin(), patch.cend());

	return device_patches<Float>{data, 4_patches, 5_rows, 5_cols};
}

device_patches<float> patches_lhs(float tag)
{
	return patches_lhs_impl(tag);
}

device_patches<double> patches_lhs(double tag)
{
	return patches_lhs_impl(tag);
}

template<typename Float, typename = std::enable_if_t<std::is_floating_point<Float>::value>>
device_patches<Float> patches_rhs_impl(Float tag)
{
	const auto patch0 = patch_base(tag);
	const auto patch1 = patch90(tag);
	const auto patch2 = patch_yr(tag);
	const auto patch3 = std::vector<Float>(patch0.size(), 0.0);
	auto data = patch0;
	data.insert(data.end(), patch1.cbegin(), patch1.cend());
	data.insert(data.end(), patch2.cbegin(), patch2.cend());
	data.insert(data.end(), patch3.cbegin(), patch3.cend());

	return device_patches<Float>{data, 4_patches, 5_rows, 5_cols};
}

device_patches<float> patches_rhs(float tag)
{
	return patches_rhs_impl(tag);
}

device_patches<double> patches_rhs(double tag)
{
	return patches_rhs_impl(tag);
}

//! Perspective transformations between the test patches.
template<typename Float, typename = std::enable_if_t<std::is_floating_point<Float>::value>>
device_patches<float> perspective_matrices_impl(Float /*tag*/)
{
	const auto row_maj = false;
	const auto data = std::vector<float>{
		// projective matrix
		1.0,  0.0,	0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, // identity
		0.0,  -1.0, 4.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, // rotation
		-1.0, 0.0,	4.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, // reflection
		1.0,  0.0,	0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, // identity
	};

	return device_patches<float>{data, 4_patches, 3_rows, 3_cols, row_maj};
}

device_patches<float> perspective_matrices(float tag)
{
	return perspective_matrices_impl(tag);
}

device_patches<float> perspective_matrices(double tag)
{
	return perspective_matrices_impl(tag);
}

template<typename Float>
device_patches<vec3<Float>> patches_lhs_impl(vec3<Float> /*tag*/)
{
	const auto ch0 = patch_base(Float{});
	const auto ch1 = patch90(Float{});
	const auto ch2 = patch180(Float{});
	const auto data0 = [&ch0] {
		auto tmp = ch0;
		tmp.insert(tmp.end(), ch0.cbegin(), ch0.cend());
		tmp.insert(tmp.end(), ch0.cbegin(), ch0.cend());
		tmp.insert(tmp.end(), ch0.cbegin(), ch0.cend());
		return tmp;
	}();
	const auto data1 = [&ch1] {
		auto tmp = ch1;
		tmp.insert(tmp.end(), ch1.cbegin(), ch1.cend());
		tmp.insert(tmp.end(), ch1.cbegin(), ch1.cend());
		tmp.insert(tmp.end(), ch1.cbegin(), ch1.cend());
		return tmp;
	}();
	const auto data2 = [&ch2] {
		auto tmp = ch2;
		tmp.insert(tmp.end(), ch2.cbegin(), ch2.cend());
		tmp.insert(tmp.end(), ch2.cbegin(), ch2.cend());
		tmp.insert(tmp.end(), ch2.cbegin(), ch2.cend());
		return tmp;
	}();
	const auto d_ch0 = device_patches<Float>{data0, 4_patches, 5_rows, 5_cols};
	const auto d_ch1 = device_patches<Float>{data1, 4_patches, 5_rows, 5_cols};
	const auto d_ch2 = device_patches<Float>{data2, 4_patches, 5_rows, 5_cols};

	return join(d_ch0, d_ch1, d_ch2);
}

device_patches<vec3<float>> patches_lhs(vec3<float> tag)
{
	return patches_lhs_impl(tag);
}

device_patches<vec3<double>> patches_lhs(vec3<double> tag)
{
	return patches_lhs_impl(tag);
}

template<typename Float>
device_patches<vec3<Float>> patches_rhs_impl(vec3<Float> /*tag*/)
{
	const auto patch0 = patch_base(Float{});
	const auto patch1 = patch90(Float{});
	const auto patch2 = patch180(Float{});
	const auto patch3 = patch270(Float{});
	const auto patch4 = std::vector<Float>(patch0.size(), 0.0);

	// The first patch consists of an image rotated by 0, 90, 180 degrees.
	// The second/ third patch consists of an image rotated by 90, 180, 270 degrees.
	// Hence both rgb patches are related by a 90 degree rotation.
	// The last patch is zero and acts as a control.
	const auto ch0 = [&patch0, &patch1, &patch4] {
		auto tmp = patch0;
		tmp.insert(tmp.end(), patch1.cbegin(), patch1.cend());
		tmp.insert(tmp.end(), patch1.cbegin(), patch1.cend());
		tmp.insert(tmp.end(), patch4.cbegin(), patch4.cend());
		return tmp;
	}();
	const auto ch1 = [&patch1, &patch2, &patch4] {
		auto tmp = patch1;
		tmp.insert(tmp.end(), patch2.cbegin(), patch2.cend());
		tmp.insert(tmp.end(), patch2.cbegin(), patch2.cend());
		tmp.insert(tmp.end(), patch4.cbegin(), patch4.cend());
		return tmp;
	}();
	const auto ch2 = [&patch2, &patch3, &patch4] {
		auto tmp = patch2;
		tmp.insert(tmp.end(), patch3.cbegin(), patch3.cend());
		tmp.insert(tmp.end(), patch3.cbegin(), patch3.cend());
		tmp.insert(tmp.end(), patch4.cbegin(), patch4.cend());
		return tmp;
	}();
	const auto d_ch0 = device_patches<Float>{ch0, 4_patches, 5_rows, 5_cols};
	const auto d_ch1 = device_patches<Float>{ch1, 4_patches, 5_rows, 5_cols};
	const auto d_ch2 = device_patches<Float>{ch2, 4_patches, 5_rows, 5_cols};

	return join(d_ch0, d_ch1, d_ch2);
}

device_patches<vec3<float>> patches_rhs(vec3<float> tag)
{
	return patches_rhs_impl(tag);
}

device_patches<vec3<double>> patches_rhs(vec3<double> tag)
{
	return patches_rhs_impl(tag);
}

//! Perspective transformations between the test patches.
template<typename Float>
device_patches<float> perspective_matrices_impl(vec3<Float> /*tag*/)
{
	const auto row_maj = false;
	const auto data = std::vector<float>{
		// projective matrix
		1.0, 0.0,  0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, // identity
		0.0, -1.0, 4.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, // rotation
		0.0, -1.0, 4.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, // rotation
		1.0, 0.0,  0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, // identity
	};

	return device_patches<float>{data, 2_patches, 3_rows, 3_cols, row_maj};
}

device_patches<float> perspective_matrices_impl(vec3<float> tag)
{
	return perspective_matrices_impl(tag);
}

device_patches<float> perspective_matrices_impl(vec3<double> tag)
{
	return perspective_matrices_impl(tag);
}

template<typename Float, typename = std::enable_if_t<std::is_floating_point<Float>::value>>
device_patches<Float> moments_rhs_impl(Float tag, bool high_order)
{
	const auto patch0 = patch_base_moments(tag, high_order);
	const auto patch1 = patch90_moments(tag, high_order);
	const auto patch2 = patch_yr_moments(tag, high_order);
	const auto patch3 = std::vector<Float>(patch0.size(), 0.0);

	auto data = patch0;
	data.insert(data.end(), patch1.cbegin(), patch1.cend());
	data.insert(data.end(), patch2.cbegin(), patch2.cend());
	data.insert(data.end(), patch3.cbegin(), patch3.cend());

	return high_order ? device_patches<Float>{data, 4_patches, 4_rows, 7_cols}
					  : device_patches<Float>{data, 4_patches, 4_rows, 3_cols};
}

device_patches<float> moments_clip_rhs(float tag, bool high_order)
{
	return moments_rhs_impl(tag, high_order);
}

device_patches<double> moments_clip_rhs(double tag, bool high_order)
{
	return moments_rhs_impl(tag, high_order);
}

device_patches<float> clustering()
{
	const auto patch0 = patch_base(float{});
	const auto patch1 = patch90(float{});
	const auto patch2 = patch180(float{});
	const auto patch3 = patch270(float{});
	const auto patch4 = std::vector<float>{
		// random patch
		0.7f,  1.0f, 0.45f, 0.3f, 0.0f, // col 0
		1.0f,  0.3f, 0.0f,	1.0f, 0.2f, // col 1
		0.15f, 0.3f, 0.4f,	0.2f, 0.4f, // col 2
		1.0f,  0.9f, 0.2f,	0.4f, 1.0f, // col 3
		0.2f,  0.0f, 1.0f,	1.0f, 1.0f, // col 4f
	};
	const auto patch5 = std::vector<float>{
		// another random patch
		0.3f,  1.0f, 0.7f, 0.3f, 0.9f, // col 0
		0.2f,  0.9f, 1.0f, 1.0f, 0.5f, // col 1
		0.15f, 0.7f, 0.3f, 0.2f, 0.4f, // col 2
		0.4f,  0.4f, 0.8f, 0.4f, 0.3f, // col 3
		1.0f,  1.0f, 0.3f, 0.3f, 0.3f, // col 4
	};
	const auto patch6 = std::vector<float>(patch0.size(), 0.0f);

	// Duplicates are intensional.
	auto data = patch0;
	data.insert(data.end(), patch1.cbegin(), patch1.cend()); // 1
	data.insert(data.end(), patch2.cbegin(), patch2.cend()); // 2
	data.insert(data.end(), patch4.cbegin(), patch4.cend()); // 3
	data.insert(data.end(), patch2.cbegin(), patch2.cend()); // 4
	data.insert(data.end(), patch4.cbegin(), patch4.cend()); // 5
	data.insert(data.end(), patch4.cbegin(), patch4.cend()); // 6
	data.insert(data.end(), patch5.cbegin(), patch5.cend()); // 7
	data.insert(data.end(), patch3.cbegin(), patch3.cend()); // 8
	data.insert(data.end(), patch6.cbegin(), patch6.cend()); // 9

	return device_patches<float>{data, 10_patches, 5_rows, 5_cols};
}

std::vector<size_t> clustering_solution()
{
	// See also clustering function.
	// The first index is chosen randomly, the others accordingly.
	return std::vector<size_t>{1, 9, 3, 7};
}

void distance_matrix(const device_matrix<double>& dist_mat, double margin_low, double margin_high)
{
	REQUIRE(dist_mat.rows() == 4);
	REQUIRE(dist_mat.cols() == 4);

	CHECK(dist_mat.at(0_rows, 0_cols) == Approx{0.0}.margin(margin_low)); // id - id
	CHECK(dist_mat.at(1_rows, 0_cols) == Approx{0.0}.margin(margin_low)); // id - id
	CHECK(dist_mat.at(2_rows, 0_cols) == Approx{0.0}.margin(margin_low)); // id - id
	CHECK(dist_mat.at(3_rows, 0_cols) == Approx{0.0}.margin(margin_low)); // id - id

	CHECK(dist_mat.at(0_rows, 1_cols) == Approx{0.0}.margin(margin_low)); // id - rot
	CHECK(dist_mat.at(1_rows, 1_cols) == Approx{0.0}.margin(margin_low)); // id - rot
	CHECK(dist_mat.at(2_rows, 1_cols) == Approx{0.0}.margin(margin_low)); // id - rot
	CHECK(dist_mat.at(3_rows, 1_cols) == Approx{0.0}.margin(margin_low)); // id - rot

	CHECK(dist_mat.at(0_rows, 2_cols) == Approx{0.0}.margin(margin_low)); // id - reflection
	CHECK(dist_mat.at(1_rows, 2_cols) == Approx{0.0}.margin(margin_low)); // id - reflection
	CHECK(dist_mat.at(2_rows, 2_cols) == Approx{0.0}.margin(margin_low)); // id - reflection
	CHECK(dist_mat.at(3_rows, 2_cols) == Approx{0.0}.margin(margin_low)); // id - reflection

	CHECK(dist_mat.at(0_rows, 3_cols) > margin_high); // rot - zero
	CHECK(dist_mat.at(1_rows, 3_cols) > margin_high); // rot - zero
	CHECK(dist_mat.at(2_rows, 3_cols) > margin_high); // rot - zero
	CHECK(dist_mat.at(3_rows, 3_cols) > margin_high); // rot - zero
}
} // namespace data_orthogonal