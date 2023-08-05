#define CATCH_CONFIG_ENABLE_BENCHMARKING

#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_matrix.h"
#include "../include/extract_patches.h"
#include "../include/utils.h"
#include "utils.h"

#include "thrust/inner_product.h"
#include <thrust/device_vector.h>
#include <thrust/iterator/counting_iterator.h>
#include <thrust/pair.h>
#include <thrust/random.h>
#include <thrust/transform.h>

#include <algorithm>
#include <cstddef>
#include <vector>

template<typename Float>
vec3<Float>& operator++(vec3<Float>& obj)
{
	obj._1 += Float{1.0};
	obj._2 += Float{1.0};
	obj._3 += Float{1.0};
	return obj;
}

template<typename Numeric>
inline thrust::device_vector<Numeric> sequence(size_t size, Numeric /*tag*/)
{
	auto seq = std::vector<Numeric>(size);
	std::iota(seq.begin(), seq.end(), Numeric{0});
	return seq;
}

TEST_CASE("Integer sequence", "[utils]")
{
	const auto size = 10u;
	const auto h_vector = sequence(size, size_t{});
	const auto d_vector = d_seq(size); // function to test

	const auto err = thrust::inner_product(d_vector.cbegin(), d_vector.cend(), h_vector.cbegin(), 0,
										   thrust::plus<size_t>(), thrust::minus<size_t>());

	CHECK(err == 0);
}

TEST_CASE("Number of patches in a matrix", "[utils]")
{
	const auto img_size = Size{10_rows, 11_cols};
	const auto patch_size = Size{3_rows, 3_cols};
	const auto solution = Size{8_rows, 9_cols};
	const auto patch_count = patch_count_size(img_size, patch_size);

	CHECK(patch_count == solution);
}

TEMPLATE_TEST_CASE("Copy a subset of patches", "[utils]", float, double, vec3<float>, vec3<double>)
{
	const auto patch_count = 10_patches;
	const auto patch_size = Size{4_rows, 3_cols};
	const auto patch_data = sequence(patch_count.value() * patch_size.total(), TestType{});
	const auto col_maj = true;
	const auto patches_c = device_patches<TestType>{patch_data, patch_count, patch_size, col_maj};
	const auto patches_r = to_row_maj(patches_c);

	const auto solution_c = [patch_size] {
		const auto indices = std::vector<TestType>{TestType{1}, TestType{4}, TestType{6}};
		auto patch0 = std::vector<TestType>(patch_size.total());
		auto patch1 = std::vector<TestType>(patch_size.total());
		auto patch2 = std::vector<TestType>(patch_size.total());
		const auto total = TestType{static_cast<float>(patch_size.total())};
		std::iota(patch0.begin(), patch0.end(), indices.at(0) * total);
		std::iota(patch1.begin(), patch1.end(), indices.at(1) * total);
		std::iota(patch2.begin(), patch2.end(), indices.at(2) * total);
		auto patches = patch0;
		patches.insert(patches.end(), patch1.cbegin(), patch1.cend());
		patches.insert(patches.end(), patch2.cbegin(), patch2.cend());
		const auto patch_count_copied = patch_index{indices.size()};
		return std::make_pair(device_patches<TestType>{patches, patch_count_copied, patch_size},
							  device_matrix<TestType>{patch0, patch_size});
	}();
	const auto solution_r =
		std::make_pair(to_row_maj(std::get<0>(solution_c)), to_row_maj(std::get<1>(solution_c)));

	// Test row and column major layout.
	const auto indices = std::vector<size_t>{1, 4, 6};
	const auto copied_patches_c = copy(patches_c, indices);
	const auto copied_patch_c = copy(patches_c, indices.at(0));
	const auto copied_patches_r = copy(patches_r, indices);
	const auto copied_patch_r = copy(patches_r, indices.at(0));

	const auto eps = 0.0;
	const auto margin = 0.0;
	is_equal(copied_patches_c, std::get<0>(solution_c), eps, margin);
	is_equal(copied_patch_c, std::get<1>(solution_c), eps, margin);
	is_equal(copied_patches_r, std::get<0>(solution_r), eps, margin);
	is_equal(copied_patch_r, std::get<1>(solution_r), eps, margin);
}

template<typename Float>
struct make_vec
{
	__device__ vec3<Float> operator()(size_t i) const noexcept
	{
		return vec3<Float>{ch0[i], ch1[i], ch2[i]};
	}

	const Float* ch0;
	const Float* ch1;
	const Float* ch2;
};

TEMPLATE_TEST_CASE("Split color channels", "[utils]", float, double)
{
	const auto patch_count = 10_patches;
	const auto patch_size = Size{7_rows, 7_cols};
	const auto ch0 = rand_patches(patch_count, patch_size, TestType{});
	const auto ch1 = rand_patches(patch_count, patch_size, TestType{});
	const auto ch2 = rand_patches(patch_count, patch_size, TestType{});

	const auto patches_rgb = [&] {
		auto data = thrust::device_vector<vec3<TestType>>(ch0.total());
		const auto begin = thrust::counting_iterator<size_t>{0};
		const auto end = thrust::counting_iterator<size_t>{data.size()};
		const auto ch0_ptr = ch0.data().get();
		const auto ch1_ptr = ch1.data().get();
		const auto ch2_ptr = ch2.data().get();
		thrust::transform(begin, end, data.begin(), make_vec<TestType>{ch0_ptr, ch1_ptr, ch2_ptr});
		return device_patches<vec3<TestType>>{data, patch_count, patch_size};
	}();
	const auto patches_rgb_split = split(patches_rgb);

	const auto eps = 0.0;
	const auto margin = 0.0;
	is_equal(std::get<0>(patches_rgb_split), ch0, eps, margin);
	is_equal(std::get<1>(patches_rgb_split), ch1, eps, margin);
	is_equal(std::get<2>(patches_rgb_split), ch2, eps, margin);
}

TEMPLATE_TEST_CASE("Join color channels", "[utils]", float, double)
{
	const auto patch_count = 10_patches;
	const auto patch_size = Size{7_rows, 7_cols};
	const auto ch0 = rand_patches(patch_count, patch_size, TestType{});
	const auto ch1 = rand_patches(patch_count, patch_size, TestType{});
	const auto ch2 = rand_patches(patch_count, patch_size, TestType{});

	const auto patches_rgb = [&] {
		auto data = thrust::device_vector<vec3<TestType>>(ch0.total());
		const auto begin = thrust::counting_iterator<size_t>{0};
		const auto end = thrust::counting_iterator<size_t>{data.size()};
		const auto ch0_ptr = ch0.data().get();
		const auto ch1_ptr = ch1.data().get();
		const auto ch2_ptr = ch2.data().get();
		thrust::transform(begin, end, data.begin(), make_vec<TestType>{ch0_ptr, ch1_ptr, ch2_ptr});
		return device_patches<vec3<TestType>>{data, patch_count, patch_size};
	}();
	const auto patches_joined = join(ch0, ch1, ch2);

	const auto eps = 0.0;
	const auto margin = 0.0;
	is_equal(patches_joined, patches_rgb, eps, margin);
}

TEMPLATE_TEST_CASE("Transpose matrix", "[utils]", float, double, vec3<float>, vec3<double>)
{
	// non-quadratic image
	const auto img = rand_matrix(Size{256_rows, 128_cols}, TestType{});

	const auto eps = 0.0;
	const auto margin = 0.0;
	is_equal(to_col_maj(img), img, eps, margin);
	not_equal(to_row_maj(img), img, eps, margin);
	is_equal(to_col_maj(to_row_maj(img)), img, eps, margin);
}

TEMPLATE_TEST_CASE("Transpose patches", "[utils]", float, double, vec3<float>, vec3<double>)
{
	using T = TestType;

	const auto patches_col_maj = [] {
		const auto data = std::vector<T>{
			T{0.0}, T{1.0},	 T{2.0}, // patch 0
			T{3.0}, T{4.0},	 T{5.0}, //
			T{6.0}, T{7.0},	 T{8.0}, // patch 1
			T{9.0}, T{10.0}, T{11.0}, //
		};
		return device_patches<T>{data, 2_patches, 3_rows, 2_cols};
	}();
	const auto patches_row_maj = [] {
		const auto data = std::vector<T>{
			T{0.0}, T{3.0}, // patch 0
			T{1.0}, T{4.0}, //
			T{2.0}, T{5.0}, //
			T{6.0}, T{9.0}, // patch 1
			T{7.0}, T{10.0}, //
			T{8.0}, T{11.0}, //
		};
		const auto row_maj = false;
		return device_patches<T>{data, 2_patches, 3_rows, 2_cols, row_maj};
	}();

	const auto eps = 0.0;
	const auto margin = 0.0;
	is_equal(to_col_maj(patches_col_maj), patches_col_maj, eps, margin);
	is_equal(to_col_maj(patches_row_maj), patches_col_maj, eps, margin);
	is_equal(to_row_maj(patches_row_maj), patches_row_maj, eps, margin);
	is_equal(to_row_maj(patches_col_maj), patches_row_maj, eps, margin);
}

TEST_CASE("Transpose benchmark", "[utils][!benchmark]")
{
	const auto img = rand_matrix(IMG_SIZE_BENCHMARK, float{});
	const auto transpose = true;

	BENCHMARK("Transpose image")
	{
		return impl::transpose_memory(img, transpose);
	};

	const auto patches = rand_patches(PATCH_COUNT_BENCHMARK, PATCH_SIZE_BENCHMARK, float{});

	BENCHMARK("Transpose patches")
	{
		return impl::transpose_memory(patches, transpose);
	};
}

TEST_CASE("Embed patches with offset")
{
	using point = thrust::pair<int, int>; // (x,y)

	const auto patches_data = std::vector<double>{
		0.0, 1.0, 2.0, 3.0, // patch 0
		4.0, 5.0, 6.0, 7.0, // patch 1
		4.0, 5.0, 6.0, 7.0, // patch 2
	};
	const auto patches = device_patches<double>{patches_data, 3_patches, Size{2_rows, 2_cols}};

	const auto offsets_data = std::vector<point>{point{0, 0}, point{1, -1}, point{10, 10}};
	const auto offsets = device_matrix<point>{offsets_data, Size{3_rows, 1_cols}};

	const auto solution_data = std::vector<double>{
		-1.0, -1.0, -1.0, -1.0, // patch 0
		-1.0, 0.0,	1.0,  -1.0, //
		-1.0, 2.0,	3.0,  -1.0, //
		-1.0, -1.0, -1.0, -1.0, //
		-1.0, -1.0, -1.0, -1.0, // patch 1
		-1.0, -1.0, -1.0, -1.0, //
		4.0,  5.0,	-1.0, -1.0, //
		6.0,  7.0,	-1.0, -1.0, //
		-1.0, -1.0, -1.0, -1.0, // patch 2
		-1.0, -1.0, -1.0, -1.0, //
		-1.0, -1.0, -1.0, -1.0, //
		-1.0, -1.0, -1.0, -1.0, //
	};
	const auto emb_size = Size{4_rows, 4_cols};
	const auto solution = device_patches<double>{solution_data, 3_patches, emb_size};

	const auto background = -1.0;
	const auto embedded = embed(patches, offsets, emb_size, background);

	const auto eps = 0.0;
	const auto margin = 0.0;
	is_equal(embedded, solution, eps, margin);
}

TEST_CASE("Crop device_matrix")
{
	const auto img_data = std::vector<double>{
		0.0, 0.0, 0.0, 0.0, 0.0,  0.0,	0.0,  0.0, // col 0
		0.0, 1.0, 2.0, 3.0, 4.0,  5.0,	6.0,  0.0, // col 1
		0.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 0.0, // col 2
		0.0, 0.0, 0.0, 0.0, 0.0,  0.0,	0.0,  0.0, // col 3
	};
	const auto img_size = Size{8_rows, 4_cols};
	const auto img = device_matrix<double>{img_data, img_size};

	const auto solution_data = std::vector<double>{
		1.0, 2.0, 3.0, 4.0,	 5.0,  6.0, // col 0
		7.0, 8.0, 9.0, 10.0, 11.0, 12.0, // col 1
	};
	const auto crop_size = Size{6_rows, 2_cols};
	const auto solution = device_matrix<double>{solution_data, crop_size};

	const auto cropped = crop(img, crop_size);

	const auto eps = 0.0;
	const auto margin = 0.0;
	is_equal(cropped, solution, eps, margin);
}