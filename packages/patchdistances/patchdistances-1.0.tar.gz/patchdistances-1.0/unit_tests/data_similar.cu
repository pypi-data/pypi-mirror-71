#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_matrix.h"
#include "../include/device_patches.h"
#include "../include/utils.h"
#include "../include/vec3.h"
#include "data_similar.h"

#include <vector>

namespace data_similar
{
/*
 ** Patches which are common to multiple functions.
 */
// "rotation by 0deg"
template<typename Float>
auto patch0(Float /*tag*/)
{
	return std::vector<Float>{
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 0
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 1
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 2
		0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, // col 3
		0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, // col 4
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 5
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 6
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 7
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 8
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 9
	};
}
// rotation by -90deg
template<typename Float>
auto patch90(Float /*tag*/)
{
	return std::vector<Float>{
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 0
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 1
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 2
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 3
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 4
		0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, // col 5
		0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, // col 6
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 7
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 8
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 9
	};
}
// rotation by -180deg
template<typename Float>
auto patch180(Float /*tag*/)
{
	return std::vector<Float>{
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 0
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 1
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 2
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 3
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 4
		0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, // col 5
		0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, // col 6
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 7
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 8
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 9
	};
};
// rotation by -180deg
template<typename Float>
auto patch270(Float /*tag*/)
{
	return std::vector<Float>{
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 0
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 1
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 2
		0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, // col 3
		0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, // col 4
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 5
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 6
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 7
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 8
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 9
	};
}

// different patch "rotated by 0deg"
template<typename Float>
auto patch_0(Float /*tag*/)
{
	return std::vector<Float>{
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 0
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 1
		0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, // col 2
		0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, // col 3
		0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, // col 4
		0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, // col 5
		0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, // col 6
		0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, // col 7
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 8
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 9
	};
}
// scaled by 2/3
template<typename Float>
auto patch_x2(Float /*tag*/)
{
	return std::vector<Float>{
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 0
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 1
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 2
		0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, // col 3
		0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, // col 4
		0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, // col 5
		0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, // col 6
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 7
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 8
		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, // col 9
	};
}

// log polar transformation of patch0
template<typename Float>
auto patch0_lp(Float /*tag*/)
{
	return std::vector<Float>{
		0.245f, 0.240f, 0.228f, 0.201f, 0.145f, 0.040f, -0.037f, 0.000f, // col 0
		0.243f, 0.236f, 0.219f, 0.185f, 0.122f, 0.034f, 0.001f,	 0.000f, // col 1
		0.245f, 0.240f, 0.228f, 0.201f, 0.145f, 0.040f, -0.037f, 0.000f, // col 2
		0.250f, 0.250f, 0.249f, 0.245f, 0.227f, 0.150f, -0.038f, -0.019f, // col 3
		0.255f, 0.260f, 0.272f, 0.299f, 0.355f, 0.460f, 0.555f,	 0.357f, // col 4
		0.257f, 0.265f, 0.283f, 0.324f, 0.424f, 0.666f, 1.082f,	 1.173f, // col 5
		0.255f, 0.260f, 0.272f, 0.299f, 0.355f, 0.460f, 0.555f,	 0.357f, // col 6
		0.250f, 0.250f, 0.249f, 0.245f, 0.227f, 0.150f, -0.038f, -0.019f, // col 3
	};
}

// log polar transformation of patch90
// Rotation in the patch results in translation in the log polar transformation.
template<typename Float>
auto patch90_lp(Float /*tag*/)
{
	return std::vector<Float>{
		0.255f, 0.260f, 0.272f, 0.299f, 0.355f, 0.460f, 0.555f,	 0.357f, // col 0
		0.250f, 0.250f, 0.249f, 0.245f, 0.227f, 0.150f, -0.038f, -0.019f, // col 1
		0.245f, 0.240f, 0.228f, 0.201f, 0.145f, 0.040f, -0.037f, 0.000f, // col 2
		0.243f, 0.236f, 0.219f, 0.185f, 0.122f, 0.034f, 0.001f,	 0.000f, // col 3
		0.245f, 0.240f, 0.228f, 0.201f, 0.145f, 0.040f, -0.037f, 0.000f, // col 4
		0.250f, 0.250f, 0.249f, 0.245f, 0.227f, 0.150f, -0.038f, -0.019f, // col 5
		0.255f, 0.260f, 0.272f, 0.299f, 0.355f, 0.460f, 0.555f,	 0.357f, // col 6
		0.257f, 0.265f, 0.283f, 0.324f, 0.424f, 0.666f, 1.082f,	 1.173f, // col 7
	};
}

// log polar transformation of patch180
// Rotation in the patch results in translation in the log polar transformation.
template<typename Float>
auto patch180_lp(Float /*tag*/)
{
	return std::vector<Float>{
		0.255f, 0.260f, 0.272f, 0.299f, 0.355f, 0.460f, 0.555f,	 0.357f, // col 0
		0.257f, 0.265f, 0.283f, 0.324f, 0.424f, 0.666f, 1.082f,	 1.173f, // col 1
		0.255f, 0.260f, 0.272f, 0.299f, 0.355f, 0.460f, 0.555f,	 0.357f, // col 2
		0.250f, 0.250f, 0.249f, 0.245f, 0.227f, 0.150f, -0.038f, -0.019f, // col 3
		0.245f, 0.240f, 0.228f, 0.201f, 0.145f, 0.040f, -0.037f, 0.000f, // col 4
		0.243f, 0.236f, 0.219f, 0.185f, 0.122f, 0.034f, 0.001f,	 0.000f, // col 5
		0.245f, 0.240f, 0.228f, 0.201f, 0.145f, 0.040f, -0.037f, 0.000f, // col 6
		0.250f, 0.250f, 0.249f, 0.245f, 0.227f, 0.150f, -0.038f, -0.019f, // col 7
	};
}

// log polar transformation of patch270
// Rotation in the patch results in translation in the log polar transformation.
template<typename Float>
auto patch270_lp(Float /*tag*/)
{
	return std::vector<Float>{
		0.245f, 0.240f, 0.228f, 0.201f, 0.145f, 0.040f, -0.037f, 0.000f, // col 0
		0.250f, 0.250f, 0.249f, 0.245f, 0.227f, 0.150f, -0.038f, -0.019f, // col 1
		0.255f, 0.260f, 0.272f, 0.299f, 0.355f, 0.460f, 0.555f,	 0.357f, // col 2
		0.257f, 0.265f, 0.283f, 0.324f, 0.424f, 0.666f, 1.082f,	 1.173f, // col 3
		0.255f, 0.260f, 0.272f, 0.299f, 0.355f, 0.460f, 0.555f,	 0.357f, // col 4
		0.250f, 0.250f, 0.249f, 0.245f, 0.227f, 0.150f, -0.038f, -0.019f, // col 5
		0.245f, 0.240f, 0.228f, 0.201f, 0.145f, 0.040f, -0.037f, 0.000f, // col 6
		0.243f, 0.236f, 0.219f, 0.185f, 0.122f, 0.034f, 0.001f,	 0.000f, // col 7
	};
}

// log polar transformation of patch_x2
template<typename Float>
auto patch_x2_lp(Float /*tag*/)
{
	return std::vector<Float>{
		1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.037f, 0.715f, // col 0
		1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.007f, 1.135f, // col 1
		1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.037f, 0.715f, // col 2
		1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.007f, 1.135f, // col 3
		1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.037f, 0.715f, // col 4
		1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.007f, 1.135f, // col 5
		1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.037f, 0.715f, // col 6
		1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.007f, 1.135f, // col 7
	};
}

template<typename Float, typename = std::enable_if_t<std::is_floating_point<Float>::value>>
device_patches<Float> patches_lhs_impl(Float tag)
{
	const auto p = patch0(tag);
	const auto p_ = patch_0(tag);
	auto data = p;
	data.insert(data.end(), p.cbegin(), p.cend());
	data.insert(data.end(), p_.cbegin(), p_.cend());
	data.insert(data.end(), p_.cbegin(), p_.cend());

	return device_patches<Float>{data, 4_patches, 8_rows, 10_cols};
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
	const auto p0 = patch0(tag);
	const auto p90 = patch90(tag);
	const auto p_x2 = patch_x2(tag);
	const auto p00 = std::vector<Float>(p0.size(), 0.0);

	auto data = p0;
	data.insert(data.end(), p90.cbegin(), p90.cend());
	data.insert(data.end(), p_x2.cbegin(), p_x2.cend());
	data.insert(data.end(), p00.cbegin(), p00.cend());

	return device_patches<Float>{data, 4_patches, 8_rows, 10_cols};
}

device_patches<float> patches_rhs(float tag)
{
	return patches_rhs_impl(tag);
}

device_patches<double> patches_rhs(double tag)
{
	return patches_rhs_impl(tag);
}

template<typename Float>
device_patches<vec3<Float>> patches_lhs_impl(vec3<Float> /*tag*/)
{
	const auto p0 = patch0(Float{});
	const auto p90 = patch90(Float{});
	const auto p180 = patch180(Float{});
	const auto p_0 = patch_0(Float{});

	const auto ch0 = [&p0, &p_0] {
		auto tmp = p0;
		tmp.insert(tmp.end(), p0.cbegin(), p0.cend());
		tmp.insert(tmp.end(), p_0.cbegin(), p_0.cend());
		tmp.insert(tmp.end(), p_0.cbegin(), p_0.cend());
		return tmp;
	}();
	const auto ch1 = [&p90, &p_0] {
		auto tmp = p90;
		tmp.insert(tmp.end(), p90.cbegin(), p90.cend());
		tmp.insert(tmp.end(), p_0.cbegin(), p_0.cend());
		tmp.insert(tmp.end(), p_0.cbegin(), p_0.cend());
		return tmp;
	}();
	const auto ch2 = [&p180, &p_0] {
		auto tmp = p180;
		tmp.insert(tmp.end(), p180.cbegin(), p180.cend());
		tmp.insert(tmp.end(), p_0.cbegin(), p_0.cend());
		tmp.insert(tmp.end(), p_0.cbegin(), p_0.cend());
		return tmp;
	}();
	const auto d_ch0 = device_patches<Float>{ch0, 4_patches, 8_rows, 10_cols};
	const auto d_ch1 = device_patches<Float>{ch1, 4_patches, 8_rows, 10_cols};
	const auto d_ch2 = device_patches<Float>{ch2, 4_patches, 8_rows, 10_cols};

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
	const auto p0 = patch0(Float{});
	const auto p90 = patch90(Float{});
	const auto p180 = patch180(Float{});
	const auto p270 = patch270(Float{});
	const auto p_x2 = patch_x2(Float{});
	const auto p00 = std::vector<Float>(p0.size(), 0.0);

	// The first patch consists of an image rotated by 0, 90, 180 degrees.
	// The second patch consists of an image rotated by 90, 180, 270 degrees and scaled by 2.
	// Hence both rgb patches are related by a 90 degree rotation and scale 2.
	// The third patch is scaled by 2.
	// The fourth patch is zero and acts as a control.
	const auto ch0 = [&p0, &p90, &p_x2, &p00] {
		auto tmp = p0;
		tmp.insert(tmp.end(), p90.cbegin(), p90.cend());
		tmp.insert(tmp.end(), p_x2.cbegin(), p_x2.cend());
		tmp.insert(tmp.end(), p00.cbegin(), p00.cend());
		return tmp;
	}();
	const auto ch1 = [&p90, &p180, &p_x2, &p00] {
		auto tmp = p90;
		tmp.insert(tmp.end(), p180.cbegin(), p180.cend());
		tmp.insert(tmp.end(), p_x2.cbegin(), p_x2.cend());
		tmp.insert(tmp.end(), p00.cbegin(), p00.cend());
		return tmp;
	}();
	const auto ch2 = [&p180, &p270, &p_x2, &p00] {
		auto tmp = p180;
		tmp.insert(tmp.end(), p270.cbegin(), p270.cend());
		tmp.insert(tmp.end(), p_x2.cbegin(), p_x2.cend());
		tmp.insert(tmp.end(), p00.cbegin(), p00.cend());
		return tmp;
	}();
	const auto d_ch0 = device_patches<Float>{ch0, 4_patches, 8_rows, 10_cols};
	const auto d_ch1 = device_patches<Float>{ch1, 4_patches, 8_rows, 10_cols};
	const auto d_ch2 = device_patches<Float>{ch2, 4_patches, 8_rows, 10_cols};

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

template<typename Float, typename = std::enable_if_t<std::is_floating_point<Float>::value>>
device_patches<Float> patches_rhs_log_polar_impl(Float tag)
{
	const auto p0 = patch0_lp(tag);
	const auto p90 = patch90_lp(tag);
	const auto p_x2 = patch_x2_lp(tag);
	const auto p00 = std::vector<Float>(p0.size(), 0.0);

	auto data = p0;
	data.insert(data.end(), p90.cbegin(), p90.cend());
	data.insert(data.end(), p_x2.cbegin(), p_x2.cend());
	data.insert(data.end(), p00.cbegin(), p00.cend());

	return device_patches<Float>{data, 4_patches, 8_rows, 8_cols};
}

device_patches<float> patches_rhs_log_polar(float tag)
{
	return patches_rhs_log_polar_impl(tag);
}

device_patches<double> patches_rhs_log_polar(double tag)
{
	return patches_rhs_log_polar_impl(tag);
}

template<typename Float>
device_patches<vec3<Float>> patches_rhs_log_polar_impl(vec3<Float> /*tag*/)
{
	const auto p0 = patch0_lp(Float{});
	const auto p90 = patch90_lp(Float{});
	const auto p180 = patch180_lp(Float{});
	const auto p270 = patch270_lp(Float{});
	const auto p_x2 = patch_x2_lp(Float{});
	const auto p00 = std::vector<Float>(p0.size(), 0.0);

	// The first patch consists of an image rotated by 0, 90, 180 degrees.
	// The second patch consists of an image rotated by 90, 180, 270 degrees and scaled by 2.
	// Hence both rgb patches are related by a 90 degree rotation and scale 2.
	// The third patch is scaled by 2.
	// The fourth patch is zero and acts as a control.
	const auto ch0 = [&p0, &p90, &p_x2, &p00] {
		auto tmp = p0;
		tmp.insert(tmp.end(), p90.cbegin(), p90.cend());
		tmp.insert(tmp.end(), p_x2.cbegin(), p_x2.cend());
		tmp.insert(tmp.end(), p00.cbegin(), p00.cend());
		return tmp;
	}();
	const auto ch1 = [&p90, &p180, &p_x2, &p00] {
		auto tmp = p90;
		tmp.insert(tmp.end(), p180.cbegin(), p180.cend());
		tmp.insert(tmp.end(), p_x2.cbegin(), p_x2.cend());
		tmp.insert(tmp.end(), p00.cbegin(), p00.cend());
		return tmp;
	}();
	const auto ch2 = [&p180, &p270, &p_x2, &p00] {
		auto tmp = p180;
		tmp.insert(tmp.end(), p270.cbegin(), p270.cend());
		tmp.insert(tmp.end(), p_x2.cbegin(), p_x2.cend());
		tmp.insert(tmp.end(), p00.cbegin(), p00.cend());
		return tmp;
	}();
	const auto d_ch0 = device_patches<Float>{ch0, 4_patches, 8_rows, 8_cols};
	const auto d_ch1 = device_patches<Float>{ch1, 4_patches, 8_rows, 8_cols};
	const auto d_ch2 = device_patches<Float>{ch2, 4_patches, 8_rows, 8_cols};

	return join(d_ch0, d_ch1, d_ch2);
}

device_patches<vec3<float>> patches_rhs_log_polar(vec3<float> tag)
{
	return patches_rhs_log_polar_impl(tag);
}

device_patches<vec3<double>> patches_rhs_log_polar(vec3<double> tag)
{
	return patches_rhs_log_polar_impl(tag);
}

//! Perspective transformations between the test patches.
device_patches<float> perspective_matrices()
{
	const auto row_maj = false;
	const auto data = std::vector<float>{
		// projective matrix
		1.0, 0.0,  0.0,	  0.0, 1.0, 0.0,   0.0, 0.0, 1.0, // identity
		0.0, -1.0, 9.0,	  1.0, 0.0, 0.0,   0.0, 0.0, 1.0, // rotation by -90deg
		1.5, 0.0,  -2.25, 0.0, 1.5, -1.75, 0.0, 0.0, 1.0, // scaling by 2/3
		1.0, 0.0,  0.0,	  0.0, 1.0, 0.0,   0.0, 0.0, 1.0, // identity
	};

	return device_patches<float>{data, 4_patches, 3_rows, 3_cols, row_maj};
}

device_patches<float> clustering()
{
	const auto p0 = patch0(float{});
	const auto p90 = patch90(float{});
	const auto p180 = patch180(float{});
	const auto p270 = patch270(float{});
	const auto prand = std::vector<float>{
		// random patch
		0.5f, 0.7f,	 1.0f, 0.45f, 0.3f, 0.0f, 0.6f, 0.2f, // col 0
		0.7f, 0.7f,	 1.0f, 0.7f,  0.3f, 0.1f, 0.3f, 0.3f, // col 1
		1.0f, 1.0f,	 0.3f, 0.0f,  1.0f, 0.2f, 0.2f, 0.3f, // col 2
		0.5f, 0.15f, 0.3f, 0.4f,  0.2f, 0.4f, 0.4f, 0.4f, // col 3
		1.0f, 1.0f,	 0.9f, 0.2f,  0.4f, 1.0f, 0.3f, 0.5f, // col 4
		0.3f, 0.2f,	 0.0f, 1.0f,  1.0f, 1.0f, 0.3f, 0.6f, // col 5
		0.4f, 0.2f,	 0.0f, 1.0f,  0.2f, 0.4f, 0.4f, 0.4f, // col 6
		0.2f, 0.1f,	 0.3f, 0.4f,  0.3f, 0.2f, 0.8f, 0.2f, // col 7
		0.2f, 0.6f,	 0.0f, 0.9f,  0.3f, 0.1f, 0.3f, 0.3f, // col 8
		0.2f, 0.2f,	 0.0f, 0.3f,  0.3f, 0.8f, 0.2f, 0.2f, // col 9
	};
	const auto prand_ = std::vector<float>{
		// another random patch
		0.3f, 0.4f,	 0.4f, 0.8f, 0.2f, 0.1f, 0.3f, 0.3f, // col 0
		0.9f, 0.3f,	 1.0f, 0.7f, 0.3f, 0.9f, 0.9f, 0.2f, // col 1
		0.5f, 0.2f,	 0.9f, 1.0f, 1.0f, 0.5f, 0.2f, 0.1f, // col 2
		0.2f, 0.15f, 0.7f, 0.3f, 0.2f, 0.4f, 0.3f, 0.4f, // col 3
		0.3f, 0.4f,	 0.4f, 0.8f, 0.4f, 0.3f, 0.3f, 0.3f, // col 4
		0.6f, 1.0f,	 1.0f, 0.3f, 0.3f, 0.3f, 0.5f, 0.3f, // col 5
		0.6f, 0.3f,	 0.8f, 0.4f, 0.2f, 0.6f, 0.6f, 0.6f, // col 6
		0.8f, 0.2f,	 0.2f, 0.3f, 0.2f, 0.8f, 0.2f, 0.8f, // col 7
		0.3f, 0.8f,	 1.0f, 0.3f, 0.3f, 0.3f, 0.1f, 0.3f, // col 8
		0.3f, 0.1f,	 0.4f, 0.8f, 0.2f, 0.3f, 0.3f, 0.3f, // col 9
	};
	const auto ch6 = std::vector<float>(p0.size(), 0.0f);

	// Duplicates are intensional.
	auto data = p0; // 0
	data.insert(data.end(), p90.cbegin(), p90.cend()); // 1
	data.insert(data.end(), p180.cbegin(), p180.cend()); // 2
	data.insert(data.end(), prand.cbegin(), prand.cend()); // 3
	data.insert(data.end(), p180.cbegin(), p180.cend()); // 4
	data.insert(data.end(), prand.cbegin(), prand.cend()); // 5
	data.insert(data.end(), prand.cbegin(), prand.cend()); // 6
	data.insert(data.end(), prand_.cbegin(), prand_.cend()); // 7
	data.insert(data.end(), p270.cbegin(), p270.cend()); // 8
	data.insert(data.end(), ch6.cbegin(), ch6.cend()); // 9

	return device_patches<float>{data, 10_patches, 8_rows, 10_cols};
}

std::vector<size_t> clustering_solution()
{
	return std::vector<size_t>{1, 9, 7, 3};
}

// Distance matrix for lhs_patches x rhs_patches
void distance_matrix(const device_matrix<double>& dist_mat, double margin_low, double margin_high)
{
	REQUIRE(dist_mat.rows() == 4);
	REQUIRE(dist_mat.cols() == 4);

	CHECK(dist_mat.at(0_rows, 0_cols) == Approx{0.0}.margin(margin_low)); //  id - id
	CHECK(dist_mat.at(1_rows, 0_cols) == Approx{0.0}.margin(margin_low)); //  id - id
	CHECK(dist_mat.at(2_rows, 0_cols) > margin_high); //                      id - id_
	CHECK(dist_mat.at(3_rows, 0_cols) > margin_high); //                      id - id_

	CHECK(dist_mat.at(0_rows, 1_cols) == Approx{0.0}.margin(margin_low)); //  id  - rotation
	CHECK(dist_mat.at(1_rows, 1_cols) == Approx{0.0}.margin(margin_low)); //  id  - rotation
	CHECK(dist_mat.at(2_rows, 1_cols) > margin_high); //                      id_ - rotation
	CHECK(dist_mat.at(3_rows, 1_cols) > margin_high); //                      id_ - rotation

	CHECK(dist_mat.at(0_rows, 2_cols) > margin_high); //                     id  - scaling_
	CHECK(dist_mat.at(1_rows, 2_cols) > margin_high); //                     id  - scaling_
	CHECK(dist_mat.at(2_rows, 2_cols) == Approx{0.0}.margin(margin_low)); // id_ - scaling_
	CHECK(dist_mat.at(3_rows, 2_cols) == Approx{0.0}.margin(margin_low)); // id_ - scaling_

	CHECK(dist_mat.at(0_rows, 3_cols) > margin_high); // 					 id_ - zero
	CHECK(dist_mat.at(1_rows, 3_cols) > margin_high); // 					 id_ - zero
	CHECK(dist_mat.at(2_rows, 3_cols) > margin_high); // 					 id_ - zero
	CHECK(dist_mat.at(3_rows, 3_cols) > margin_high); // 					 id_ - zero
}
} // namespace data_similar