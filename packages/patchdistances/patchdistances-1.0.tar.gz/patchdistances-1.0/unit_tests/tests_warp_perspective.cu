#define CATCH_CONFIG_ENABLE_BENCHMARKING

#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_patches.h"
#include "../include/enums.h"
#include "../include/utils.h"
#include "../include/vec3.h"
#include "../include/warp_perspective.h"
#include "utils.h"

#include "../extern/gsl/gsl_util"

#include <vector>

constexpr auto nn = interpolation_t::nn;
constexpr auto bicubic = interpolation_t::bicubic;

TEMPLATE_TEST_CASE("Warp perspective matrix: Different image memory layouts", "[warp_perspective]",
				   float, double, vec3<float>, vec3<double>)
{
	using T = TestType;

	GIVEN("an image in row and column major format")
	{
		// Non quadratic image.
		const auto col_maj = true;
		const auto size = Size{6_rows, 5_cols};
		const auto img_vec = std::vector<T>{
			T{1.0}, T{1.0}, T{0.0}, T{3.0}, T{3.0}, //
			T{1.0}, T{1.0}, T{0.0}, T{3.0}, T{3.0}, //
			T{0.0}, T{0.0}, T{1.0}, T{0.0}, T{0.0}, //
			T{4.0}, T{4.0}, T{0.0}, T{2.0}, T{2.0}, //
			T{4.0}, T{4.0}, T{0.0}, T{2.0}, T{2.0}, //
			T{4.0}, T{4.0}, T{0.0}, T{2.0}, T{2.0}, //
		};
		const auto img_c = device_matrix<T>{img_vec, size, col_maj};
		const auto img_r = to_row_maj(img_c);
		const auto rows_r = gsl::narrow_cast<float>(img_r.rows());
		const auto cols_r = gsl::narrow_cast<float>(img_r.cols());

		// Since warp_perspective uses the pull transformation, we need to use the inverse matrix.
		const auto A_1_vec = std::vector<float>{
			-1.0, 0.0,	cols_r - 1.0f, // -pi rotation + projection
			0.0,  -1.0, rows_r - 1.0f, //
			0.5,  2.0,	1.0, //
			-1.0, 0.0,	cols_r - 1.0f, // -pi rotation + projection
			0.0,  -1.0, rows_r - 1.0f, //
			2.0,  0.5,	1.0, //
		};
		const auto row_maj = false;
		const auto A_1 = device_patches<float>{A_1_vec, 2_patches, 3_rows, 3_cols, row_maj};

		WHEN("both are affinely transformed")
		{
			const auto img_c_warp = warp_perspective(img_c, A_1, bicubic);
			const auto img_r_warp = to_col_maj(warp_perspective(img_r, A_1, bicubic));

			THEN("they are equal")
			{
				REQUIRE(img_c_warp.patch_count() == 2);
				REQUIRE(img_r_warp.patch_count() == 2);

				constexpr auto eps = 0.0;
				constexpr auto margin = 0.0;
				is_equal(img_c_warp, img_r_warp, eps, margin);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Warp perspective patches: Different image memory layouts", "[warp_perspective]",
				   float, double, vec3<float>, vec3<double>)
{
	using T = TestType;

	GIVEN("patches in row and column major format")
	{
		// Non quadratic image.
		const auto col_maj = true;
		const auto size = Size{6_rows, 5_cols};
		const auto img_vec = std::vector<T>{
			T{1.0}, T{1.0}, T{0.0}, T{3.0}, T{3.0}, //
			T{1.0}, T{1.0}, T{0.0}, T{3.0}, T{3.0}, //
			T{0.0}, T{0.0}, T{1.0}, T{0.0}, T{0.0}, //
			T{4.0}, T{4.0}, T{0.0}, T{2.0}, T{2.0}, //
			T{4.0}, T{4.0}, T{0.0}, T{2.0}, T{2.0}, //
			T{4.0}, T{4.0}, T{0.0}, T{2.0}, T{2.0}, //
		};
		const auto patches = [&img_vec] {
			auto tmp = img_vec;
			tmp.insert(tmp.end(), img_vec.cbegin(), img_vec.cend());
			return tmp;
		}();
		const auto img_c = device_patches<T>{patches, patch_index{2}, size, col_maj};
		const auto img_r = to_row_maj(img_c);
		const auto rows_r = gsl::narrow_cast<float>(img_r.rows_patches());
		const auto cols_r = gsl::narrow_cast<float>(img_r.cols_patches());

		// Since warp_perspective uses the pull transformation, we need to use the inverse
		// matrix.
		const auto A_1_vec = std::vector<float>{
			-1.0, 0.0,	cols_r - 1.0f, // -pi rotation + projection
			0.0,  -1.0, rows_r - 1.0f, //
			0.5,  2.0,	1.0, //
			-1.0, 0.0,	cols_r - 1.0f, // -pi rotation + projection
			0.0,  -1.0, rows_r - 1.0f, //
			2.0,  0.5,	1.0, //
		};
		const auto row_maj = false;
		const auto A_1 = device_patches<float>{A_1_vec, 2_patches, 3_rows, 3_cols, row_maj};

		WHEN("both sets are affinely transformed")
		{
			const auto img_c_warp = warp_perspective(img_c, A_1, bicubic);
			const auto img_r_warp = to_col_maj(warp_perspective(img_r, A_1, bicubic));

			THEN("they are equal")
			{
				REQUIRE(img_c_warp.patch_count() == 2);
				REQUIRE(img_r_warp.patch_count() == 2);

				constexpr auto eps = 0.0;
				constexpr auto margin = 0.0;
				is_equal(img_c_warp, img_r_warp, eps, margin);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Warp affine matrix (nearest neighbor interpolation)", "[warp_perspective]",
				   float, double)
{
	GIVEN("A set of patches")
	{
		const auto row_maj = false;
		const auto size = Size{5_rows, 5_cols};
		const auto img_vec = std::vector<TestType>{
			1.0, 1.0, 0.0, 0.0, 0.0, //
			1.0, 1.0, 0.0, 0.0, 0.0, //
			0.0, 0.0, 0.0, 0.0, 0.0, //
			0.0, 0.0, 0.0, 0.0, 0.0, //
			0.0, 0.0, 0.0, 0.0, 0.0, //
		};

		// Solutions for bicubic interpolation (not exact).
		const auto sol0_vec = std::vector<TestType>{
			1.0, 1.0, 1.0, 0.0, 0.0, //
			1.0, 1.0, 1.0, 0.0, 0.0, //
			1.0, 1.0, 1.0, 0.0, 0.0, //
			0.0, 0.0, 0.0, 0.0, 0.0, //
			0.0, 0.0, 0.0, 0.0, 0.0, //
		};

		const auto sol1_vec = std::vector<TestType>{
			0.0, 0.0, 0.0, 0.0, 0.0, //
			0.0, 0.0, 0.0, 0.0, 0.0, //
			0.0, 0.0, 0.0, 0.0, 0.0, //
			1.0, 1.0, 0.0, 0.0, 0.0, //
			1.0, 1.0, 0.0, 0.0, 0.0, //
		};

		const auto sol2_vec = std::vector<TestType>{
			0.0, 0.0, 0.0, 0.0, 0.0, //
			0.0, 0.0, 0.0, 0.0, 0.0, //
			0.0, 0.0, 0.0, 0.0, 0.0, //
			0.0, 0.0, 0.0, 1.0, 1.0, //
			0.0, 0.0, 0.0, 1.0, 1.0, //
		};
		REQUIRE(img_vec.size() == size.total());
		REQUIRE(sol0_vec.size() == size.total());
		REQUIRE(sol1_vec.size() == size.total());

		const auto img = device_matrix<TestType>{img_vec, size, row_maj};
		const auto sol0 = device_matrix<TestType>{sol0_vec, size, row_maj};
		const auto sol1 = device_matrix<TestType>{sol1_vec, size, row_maj};
		const auto sol2 = device_matrix<TestType>{sol2_vec, size, row_maj};

		const auto A = [&] {
			auto tmp = std::vector<float>(3 * 9);
			perspective_matrix(0.5f, 0.0f, -0.4f, // offset by one row/ column
							   0.0f, 0.5f, -0.4f, //
							   size, tmp.data());
			perspective_matrix(0.0f, -1.0f, 0.0f, // -pi/2 rotation
							   1.0f, 0.0f, 0.0f, //
							   size, tmp.data() + 9);
			perspective_matrix(-1.0f, 0.0f, 0.0f, // -pi rotation
							   0.0f, -1.0f, 0.0f, //
							   size, tmp.data() + 18);

			return device_patches<float>{tmp, 3_patches, 3_rows, 3_cols, row_maj};
		}();

		WHEN("the patches are warped")
		{
			const auto img_warped = warp_perspective(img, A, nn);

			THEN("they equal the known solution")
			{
				REQUIRE(img_warped.patch_count() == 3);
				REQUIRE(img_warped.size_patches() == size);

				constexpr auto eps = 0.0;
				constexpr auto margin = 0.0;
				is_equal(copy(img_warped, 0), sol0, eps, margin); // identity
				is_equal(copy(img_warped, 1), sol1, eps, margin); // pi/2 rotation
				is_equal(copy(img_warped, 2), sol2, eps, margin); // pi rotation
			}
		}
	}
}

TEST_CASE("Warp perspective patches", "[warp_perspective][!benchmark]")
{
	const auto patches = rand_patches(PATCH_COUNT_BENCHMARK, PATCH_SIZE_BENCHMARK, BENCHMARK_T{});
	const auto A_vec = [] {
		const auto transform = std::vector<float>{
			0.0f, -1.0f, 6.0f, // pi/2 rotation
			1.0f, 0.0f,	 0.0f, //
			0.0f, 0.0f,	 1.0f, //
		};
		auto out = std::vector<float>{};
		for(size_t i = 0; i < PATCH_COUNT_BENCHMARK.value(); i++)
		{
			out.insert(out.end(), transform.cbegin(), transform.cend());
		}
		return out;
	}();
	const auto row_maj = false;
	const auto A = device_patches<float>{A_vec, PATCH_COUNT_BENCHMARK, 3_rows, 3_cols, row_maj};

	BENCHMARK("Warp perspective patches (bicubic)")
	{
		return warp_perspective(patches, A, bicubic);
	};

	BENCHMARK("Warp perspective patches (nearest neighbor)")
	{
		return warp_perspective(patches, A, nn);
	};
}

TEST_CASE("Warp perspective matrix", "[warp_perspective][!benchmark]")
{
	const auto patch = rand_matrix(PATCH_SIZE_BENCHMARK, BENCHMARK_T{});
	const auto A_vec = [] {
		const auto transform = std::vector<float>{
			0.0f, -1.0f, 6.0f, // pi/2 rotation
			1.0f, 0.0f,	 0.0f, //
			0.0f, 0.0f,	 1.0f, //
		};
		auto out = std::vector<float>{};
		for(size_t i = 0; i < PATCH_COUNT_BENCHMARK.value(); i++)
		{
			out.insert(out.end(), transform.cbegin(), transform.cend());
		}
		return out;
	}();
	const auto row_maj = false;
	const auto A = device_patches<float>{A_vec, PATCH_COUNT_BENCHMARK, 3_rows, 3_cols, row_maj};

	BENCHMARK("Warp perspective matrix (bicubic)")
	{
		return warp_perspective(patch, A, bicubic);
	};

	BENCHMARK("Warp perspective matrix (nearest neighbor)")
	{
		return warp_perspective(patch, A, nn);
	};
}