#include "../include/device_matrix.h"
#include "../include/device_patches.h"
#include "../include/utils.h"
#include "../include/vec3.h"

#include <cuComplex.h>

#include <vector>

namespace data_afmt
{
template<typename Float>
auto patch0(Float /*tag*/)
{
	return std::vector<Float>{
		1.0, 0.0, 0.0, 0.0, // col 0
		0.0, 0.0, 0.0, 0.0, // col 1
		0.0, 0.0, 0.0, 0.0, // col 2
		0.0, 0.0, 0.0, 0.0, // col 3
	};
}
template<typename Float>
auto patch1(Float /*tag*/)
{
	return std::vector<Float>{
		1.0, 1.0, 0.0, 0.0, // col 0
		1.0, 1.0, 0.0, 0.0, // col 1
		0.0, 0.0, 0.0, 0.0, // col 2
		0.0, 0.0, 0.0, 0.0, // col 3
	};
}
template<typename Float>
auto patch2(Float /*tag*/)
{
	return std::vector<Float>{
		0.0, 0.0, 0.0, 0.0, // col 0
		0.0, 1.0, 1.0, 0.0, // col 1
		0.0, 1.0, 1.0, 0.0, // col 2
		0.0, 0.0, 0.0, 0.0, // col 3
	};
}

template<typename Complex>
auto patch_afmt0(Complex /*tag*/)
{
	return std::vector<Complex>{
		Complex{1.571f, 0.0f}, Complex{1.571f, 0.0f}, Complex{1.571f, 0.0f}, // col 0
		Complex{1.571f, 0.0f}, Complex{1.571f, 0.0f}, Complex{1.571f, 0.0f}, // col 1
		Complex{1.571f, 0.0f}, Complex{1.571f, 0.0f}, Complex{1.571f, 0.0f}, // col 2
		Complex{1.571f, 0.0f}, Complex{1.571f, 0.0f}, Complex{1.571f, 0.0f}, // col 3
	};
}
template<typename Complex>
auto patch_afmt1(Complex /*tag*/)
{
	return std::vector<Complex>{
		Complex{0.0f, 0.0f}, Complex{-1.874f, -1.874f}, Complex{-3.749f, 0.0f}, // col 0
		Complex{0.0f, 0.0f}, Complex{-1.874f, 5.016f},	Complex{3.142f, 6.890f}, // col 1
		Complex{0.0f, 0.0f}, Complex{5.016f, 5.016f},	Complex{10.032f, 0.0f}, // col 2
		Complex{0.0f, 0.0f}, Complex{5.016f, -1.874f},	Complex{3.142f, -6.890f}, // col 3
	};
}
template<typename Complex>
auto patch_afmt2(Complex /*tag*/)
{
	return std::vector<Complex>{
		Complex{0.0f, 0.0f}, Complex{-4.111f, 4.111f},	 Complex{8.222f, 0.0f}, // col 0
		Complex{0.0f, 0.0f}, Complex{4.111f, -11.001f},	 Complex{-15.113f, 6.890f}, // col 1
		Complex{0.0f, 0.0f}, Complex{-11.001f, 11.001f}, Complex{22.003f, 0.0f}, // col 2
		Complex{0.0f, 0.0f}, Complex{11.001f, -4.111f},	 Complex{-15.113f, -6.890f}, // col 3
	};
}

template<typename Float, typename = std::enable_if_t<std::is_floating_point<Float>::value>>
device_patches<Float> patches_impl(Float tag)
{
	const auto patch0_ = patch0(tag);
	const auto patch1_ = patch1(tag);
	const auto patch2_ = patch2(tag);
	auto data = patch0_;
	data.insert(data.end(), patch1_.cbegin(), patch1_.cend());
	data.insert(data.end(), patch2_.cbegin(), patch2_.cend());

	return device_patches<Float>{data, 3_patches, 4_rows, 4_cols};
}

device_patches<float> patches(float tag)
{
	return patches_impl(tag);
}

device_patches<double> patches(double tag)
{
	return patches_impl(tag);
}

template<typename Complex>
device_patches<Complex> patches_afmt_impl(Complex tag)
{
	const auto patch0_ = patch_afmt0(tag);
	const auto patch1_ = patch_afmt1(tag);
	const auto patch2_ = patch_afmt2(tag);
	auto data = patch0_;
	data.insert(data.end(), patch1_.cbegin(), patch1_.cend());
	data.insert(data.end(), patch2_.cbegin(), patch2_.cend());

	return device_patches<Complex>{data, 3_patches, 3_rows, 4_cols};
}

device_patches<cuComplex> patches_afmt(cuComplex tag)
{
	return patches_afmt_impl(tag);
}

device_patches<cuDoubleComplex> patches_afmt(cuDoubleComplex tag)
{
	return patches_afmt_impl(tag);
}
} // namespace data_afmt