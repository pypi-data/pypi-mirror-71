#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/Size.h"
#include "../include/sample.h"
#include "../include/vec3.h"

#include <array>

using namespace impl;

TEST_CASE("Get pixel values", "[sample]")
{
	GIVEN("An 2D (flattened, strided) array")
	{
		constexpr auto img_col_maj =
			std::array<double, 12>{1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0};
		constexpr auto img_row_maj =
			std::array<double, 12>{1.0, 4.0, 7.0, 10.0, 2.0, 5.0, 8.0, 11.0, 3.0, 6.0, 9.0, 12.0};
		constexpr auto rows = 3;
		constexpr auto cols = 4;

		WHEN("array elements are accessed")
		{
			THEN("the correct elements are returned")
			{
				static_assert(1.0 == get_px_col_maj(&img_col_maj[0], 0, 0, rows, cols), "");
				static_assert(2.0 == get_px_col_maj(&img_col_maj[0], 0, 1, rows, cols), "");
				static_assert(3.0 == get_px_col_maj(&img_col_maj[0], 0, 2, rows, cols), "");
				static_assert(4.0 == get_px_col_maj(&img_col_maj[0], 1, 0, rows, cols), "");
				static_assert(5.0 == get_px_col_maj(&img_col_maj[0], 1, 1, rows, cols), "");
				static_assert(6.0 == get_px_col_maj(&img_col_maj[0], 1, 2, rows, cols), "");
				static_assert(7.0 == get_px_col_maj(&img_col_maj[0], 2, 0, rows, cols), "");
				static_assert(8.0 == get_px_col_maj(&img_col_maj[0], 2, 1, rows, cols), "");
				static_assert(9.0 == get_px_col_maj(&img_col_maj[0], 2, 2, rows, cols), "");
				static_assert(10.0 == get_px_col_maj(&img_col_maj[0], 3, 0, rows, cols), "");
				static_assert(11.0 == get_px_col_maj(&img_col_maj[0], 3, 1, rows, cols), "");
				static_assert(12.0 == get_px_col_maj(&img_col_maj[0], 3, 2, rows, cols), "");

				static_assert(1.0 == get_px_row_maj(&img_row_maj[0], 0, 0, rows, cols), "");
				static_assert(2.0 == get_px_row_maj(&img_row_maj[0], 0, 1, rows, cols), "");
				static_assert(3.0 == get_px_row_maj(&img_row_maj[0], 0, 2, rows, cols), "");
				static_assert(4.0 == get_px_row_maj(&img_row_maj[0], 1, 0, rows, cols), "");
				static_assert(5.0 == get_px_row_maj(&img_row_maj[0], 1, 1, rows, cols), "");
				static_assert(6.0 == get_px_row_maj(&img_row_maj[0], 1, 2, rows, cols), "");
				static_assert(7.0 == get_px_row_maj(&img_row_maj[0], 2, 0, rows, cols), "");
				static_assert(8.0 == get_px_row_maj(&img_row_maj[0], 2, 1, rows, cols), "");
				static_assert(9.0 == get_px_row_maj(&img_row_maj[0], 2, 2, rows, cols), "");
				static_assert(10.0 == get_px_row_maj(&img_row_maj[0], 3, 0, rows, cols), "");
				static_assert(11.0 == get_px_row_maj(&img_row_maj[0], 3, 1, rows, cols), "");
				static_assert(12.0 == get_px_row_maj(&img_row_maj[0], 3, 2, rows, cols), "");

				CHECK(true); // Such that the tests do not issue an empty test case warning.
			}
		}

		WHEN("elements bordering the array are accessed")
		{
			THEN("the correct interpolated elements are returned (according to bicubic convolution "
				 "conditions)")
			{
				static_assert(-3.0 == get_px_col_maj(&img_col_maj[0], -1, -1, rows, cols), "");
				static_assert(-2.0 == get_px_col_maj(&img_col_maj[0], -1, 0, rows, cols), "");
				static_assert(-1.0 == get_px_col_maj(&img_col_maj[0], -1, 1, rows, cols), "");
				static_assert(0.0 == get_px_col_maj(&img_col_maj[0], -1, 2, rows, cols), "");
				static_assert(1.0 == get_px_col_maj(&img_col_maj[0], -1, 3, rows, cols), "");
				static_assert(16.0 == get_px_col_maj(&img_col_maj[0], 4, 3, rows, cols), "");
				static_assert(15.0 == get_px_col_maj(&img_col_maj[0], 4, 2, rows, cols), "");
				static_assert(14.0 == get_px_col_maj(&img_col_maj[0], 4, 1, rows, cols), "");
				static_assert(13.0 == get_px_col_maj(&img_col_maj[0], 4, 0, rows, cols), "");
				static_assert(12.0 == get_px_col_maj(&img_col_maj[0], 4, -1, rows, cols), "");
				static_assert(0.0 == get_px_col_maj(&img_col_maj[0], 0, -1, rows, cols), "");
				static_assert(3.0 == get_px_col_maj(&img_col_maj[0], 1, -1, rows, cols), "");
				static_assert(6.0 == get_px_col_maj(&img_col_maj[0], 2, -1, rows, cols), "");
				static_assert(9.0 == get_px_col_maj(&img_col_maj[0], 3, -1, rows, cols), "");
				static_assert(3.0 == get_px_col_maj(&img_col_maj[0], 0, 2, rows, cols), "");
				static_assert(6.0 == get_px_col_maj(&img_col_maj[0], 1, 2, rows, cols), "");
				static_assert(9.0 == get_px_col_maj(&img_col_maj[0], 2, 2, rows, cols), "");
				static_assert(12.0 == get_px_col_maj(&img_col_maj[0], 3, 2, rows, cols), "");

				static_assert(-3.0 == get_px_row_maj(&img_row_maj[0], -1, -1, rows, cols), "");
				static_assert(-2.0 == get_px_row_maj(&img_row_maj[0], -1, 0, rows, cols), "");
				static_assert(-1.0 == get_px_row_maj(&img_row_maj[0], -1, 1, rows, cols), "");
				static_assert(0.0 == get_px_row_maj(&img_row_maj[0], -1, 2, rows, cols), "");
				static_assert(1.0 == get_px_row_maj(&img_row_maj[0], -1, 3, rows, cols), "");
				static_assert(16.0 == get_px_row_maj(&img_row_maj[0], 4, 3, rows, cols), "");
				static_assert(15.0 == get_px_row_maj(&img_row_maj[0], 4, 2, rows, cols), "");
				static_assert(14.0 == get_px_row_maj(&img_row_maj[0], 4, 1, rows, cols), "");
				static_assert(13.0 == get_px_row_maj(&img_row_maj[0], 4, 0, rows, cols), "");
				static_assert(12.0 == get_px_row_maj(&img_row_maj[0], 4, -1, rows, cols), "");
				static_assert(0.0 == get_px_row_maj(&img_row_maj[0], 0, -1, rows, cols), "");
				static_assert(3.0 == get_px_row_maj(&img_row_maj[0], 1, -1, rows, cols), "");
				static_assert(6.0 == get_px_row_maj(&img_row_maj[0], 2, -1, rows, cols), "");
				static_assert(9.0 == get_px_row_maj(&img_row_maj[0], 3, -1, rows, cols), "");
				static_assert(3.0 == get_px_row_maj(&img_row_maj[0], 0, 2, rows, cols), "");
				static_assert(6.0 == get_px_row_maj(&img_row_maj[0], 1, 2, rows, cols), "");
				static_assert(9.0 == get_px_row_maj(&img_row_maj[0], 2, 2, rows, cols), "");
				static_assert(12.0 == get_px_row_maj(&img_row_maj[0], 3, 2, rows, cols), "");

				CHECK(true); // Such that the tests do not issue an empty test case warning.
			}
		}

		WHEN("array elements are accessed out of bounds")
		{
			THEN("zero is returned")
			{
				static_assert(0.0 == get_px_col_maj(&img_col_maj[0], 5, 0, rows, cols), "");
				static_assert(0.0 == get_px_col_maj(&img_col_maj[0], 0, 4, rows, cols), "");
				static_assert(0.0 == get_px_col_maj(&img_col_maj[0], 5, 4, rows, cols), "");
				static_assert(0.0 == get_px_col_maj(&img_col_maj[0], -2, 0, rows, cols), "");
				static_assert(0.0 == get_px_col_maj(&img_col_maj[0], 0, -2, rows, cols), "");
				static_assert(0.0 == get_px_col_maj(&img_col_maj[0], -2, -2, rows, cols), "");

				static_assert(0.0 == get_px_row_maj(&img_row_maj[0], 5, 0, rows, cols), "");
				static_assert(0.0 == get_px_row_maj(&img_row_maj[0], 0, 4, rows, cols), "");
				static_assert(0.0 == get_px_row_maj(&img_row_maj[0], 5, 4, rows, cols), "");
				static_assert(0.0 == get_px_row_maj(&img_row_maj[0], -2, 0, rows, cols), "");
				static_assert(0.0 == get_px_row_maj(&img_row_maj[0], 0, -2, rows, cols), "");
				static_assert(0.0 == get_px_row_maj(&img_row_maj[0], -2, -2, rows, cols), "");

				CHECK(true); // Such that the tests do not issue an empty test case warning.
			}
		}
	}
}

TEST_CASE("Sample grey pixel", "[sample]")
{
	constexpr auto img_col_maj =
		std::array<double, 12>{1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0};
	constexpr auto img_row_maj =
		std::array<double, 12>{1.0, 4.0, 7.0, 10.0, 2.0, 5.0, 8.0, 11.0, 3.0, 6.0, 9.0, 12.0};
	constexpr auto rows = 3;
	constexpr auto cols = 4;

	CHECK(5.0f == sample_nn_col_maj(&img_col_maj[0], 1.0f, 1.0f, rows, cols));
	CHECK(5.0f == sample_nn_row_maj(&img_row_maj[0], 1.0f, 1.0f, rows, cols));
	CHECK(5.0f == sample_nn_col_maj(&img_col_maj[0], 1.2f, 1.2f, rows, cols));
	CHECK(5.0f == sample_nn_row_maj(&img_row_maj[0], 1.2f, 1.2f, rows, cols));
	CHECK(9.0f == sample_nn_col_maj(&img_col_maj[0], 1.7f, 1.7f, rows, cols));
	CHECK(9.0f == sample_nn_row_maj(&img_row_maj[0], 1.7f, 1.7f, rows, cols));

	static_assert(5.0f == sample_bicubic_col_maj(&img_col_maj[0], 1.0f, 1.0f, rows, cols), "");
	static_assert(5.0f == sample_bicubic_row_maj(&img_row_maj[0], 1.0f, 1.0f, rows, cols), "");
	static_assert(7.0f == sample_bicubic_col_maj(&img_col_maj[0], 1.5f, 1.5f, rows, cols), "");
	static_assert(7.0f == sample_bicubic_row_maj(&img_row_maj[0], 1.5f, 1.5f, rows, cols), "");
}

TEST_CASE("Sample rgb pixel", "[sample]")
{
	using T = vec3<float>;
	const auto rows = 3;
	const auto cols = 4;
	const auto img = std::array<T, 12>{
		// column major
		T{1.0, 2.0, 3.0},	 T{2.0, 3.0, 4.0},	  T{3.0, 4.0, 5.0}, //
		T{4.0, 5.0, 6.0},	 T{5.0, 6.0, 7.0},	  T{6.0, 7.0, 8.0}, //
		T{7.0, 8.0, 9.0},	 T{8.0, 9.0, 10.0},	  T{9.0, 10.0, 11.0}, //
		T{10.0, 11.0, 12.0}, T{11.0, 12.0, 13.0}, T{12.0, 13.0, 14.0}, //
	};

	CHECK(vec3<float>{5.0f, 6.0f, 7.0f} == sample_nn_col_maj(&img[0], 1.0f, 1.0f, rows, cols));
	CHECK(vec3<float>{5.0f, 6.0f, 7.0f} == sample_nn_col_maj(&img[0], 1.2f, 1.2f, rows, cols));
	CHECK(vec3<float>{9.0f, 10.0f, 11.0f} == sample_nn_col_maj(&img[0], 1.7f, 1.7f, rows, cols));

	CHECK(vec3<float>{5.0f, 6.0f, 7.0f} == sample_bicubic_col_maj(&img[0], 1.0f, 1.0f, rows, cols));
	CHECK(vec3<float>{7.0f, 8.0f, 9.0f} == sample_bicubic_col_maj(&img[0], 1.5f, 1.5f, rows, cols));
}