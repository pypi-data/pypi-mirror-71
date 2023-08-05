#define CATCH_CONFIG_ENABLE_BENCHMARKING

#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_matrix.h"
#include "../include/extract_patches.h"
#include "../include/utils.h"
#include "utils.h"

#include <vector>

TEMPLATE_TEST_CASE("Extract patches (uneven image, uneven patches)", "[extract_patches]", float,
				   double, vec3<float>, vec3<double>)
{
	using T = TestType;

	GIVEN("An image")
	{
		const auto vec = std::vector<T>{
			T{1.0}, T{1.0}, T{1.0}, T{1.0}, T{1.0}, //
			T{2.0}, T{2.0}, T{2.0}, T{2.0}, T{2.0}, //
			T{3.0}, T{3.0}, T{3.0}, T{3.0}, T{3.0}, //
			T{4.0}, T{4.0}, T{4.0}, T{4.0}, T{4.0}, //
			T{5.0}, T{5.0}, T{5.0}, T{5.0}, T{5.0}, //
		};
		const auto rows = 5_rows;
		const auto cols = 5_cols;
		const auto col_maj = true;
		REQUIRE(vec.size() == cols.value() * rows.value());

		const auto solution = std::vector<T>{
			T{1.0}, T{1.0}, T{1.0}, T{2.0}, T{2.0}, T{2.0}, T{3.0}, T{3.0}, T{3.0}, // patch 0
			T{1.0}, T{1.0}, T{1.0}, T{2.0}, T{2.0}, T{2.0}, T{3.0}, T{3.0}, T{3.0}, //
			T{1.0}, T{1.0}, T{1.0}, T{2.0}, T{2.0}, T{2.0}, T{3.0}, T{3.0}, T{3.0}, //
			T{2.0}, T{2.0}, T{2.0}, T{3.0}, T{3.0}, T{3.0}, T{4.0}, T{4.0}, T{4.0}, //
			T{2.0}, T{2.0}, T{2.0}, T{3.0}, T{3.0}, T{3.0}, T{4.0}, T{4.0}, T{4.0}, //
			T{2.0}, T{2.0}, T{2.0}, T{3.0}, T{3.0}, T{3.0}, T{4.0}, T{4.0}, T{4.0}, //
			T{3.0}, T{3.0}, T{3.0}, T{4.0}, T{4.0}, T{4.0}, T{5.0}, T{5.0}, T{5.0}, //
			T{3.0}, T{3.0}, T{3.0}, T{4.0}, T{4.0}, T{4.0}, T{5.0}, T{5.0}, T{5.0}, //
			T{3.0}, T{3.0}, T{3.0}, T{4.0}, T{4.0}, T{4.0}, T{5.0}, T{5.0}, T{5.0} // patch 8
		};
		const auto p_count = 9_patches;
		const auto p_rows = 3_rows;
		const auto p_cols = 3_cols;
		REQUIRE(solution.size() == p_count.value() * p_cols.value() * p_rows.value());

		const auto img = device_matrix<T>{thrust::device_vector<T>{vec}, rows, cols, col_maj};

		WHEN("patches are extracted")
		{
			const auto patches = extract_patches(img, p_rows, p_cols);

			THEN("the extracted patches equal the known solution")
			{
				CHECK(patches.patch_count() == p_count.value());
				CHECK(patches.rows_patches() == p_rows.value());
				CHECK(patches.cols_patches() == p_cols.value());
				CHECK(get_host_vector(patches) == solution);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Extract patches (uneven image, even patch)", "[extract_patches]", float, double,
				   vec3<float>, vec3<double>)
{
	using T = TestType;

	GIVEN("An image")
	{
		const auto vec = std::vector<T>{
			T{1.0}, T{1.0}, T{1.0}, T{1.0}, T{1.0}, //
			T{2.0}, T{2.0}, T{2.0}, T{2.0}, T{2.0}, //
			T{3.0}, T{3.0}, T{3.0}, T{3.0}, T{3.0}, //
			T{4.0}, T{4.0}, T{4.0}, T{4.0}, T{4.0}, //
			T{5.0}, T{5.0}, T{5.0}, T{5.0}, T{5.0} //
		};
		const auto rows = 5_rows;
		const auto cols = 5_cols;
		const auto col_maj = true;
		REQUIRE(vec.size() == cols.value() * rows.value());

		const auto solution = std::vector<T>{
			T{1.0}, T{1.0}, T{1.0}, T{1.0}, T{2.0}, T{2.0}, T{2.0}, T{2.0},
			T{3.0}, T{3.0}, T{3.0}, T{3.0}, T{4.0}, T{4.0}, T{4.0}, T{4.0}, // patch 0
			T{1.0}, T{1.0}, T{1.0}, T{1.0}, T{2.0}, T{2.0}, T{2.0}, T{2.0},
			T{3.0}, T{3.0}, T{3.0}, T{3.0}, T{4.0}, T{4.0}, T{4.0}, T{4.0}, //
			T{2.0}, T{2.0}, T{2.0}, T{2.0}, T{3.0}, T{3.0}, T{3.0}, T{3.0},
			T{4.0}, T{4.0}, T{4.0}, T{4.0}, T{5.0}, T{5.0}, T{5.0}, T{5.0}, //
			T{2.0}, T{2.0}, T{2.0}, T{2.0}, T{3.0}, T{3.0}, T{3.0}, T{3.0},
			T{4.0}, T{4.0}, T{4.0}, T{4.0}, T{5.0}, T{5.0}, T{5.0}, T{5.0} // patch 3
		};
		const auto p_count = 4_patches;
		const auto p_rows = 4_rows;
		const auto p_cols = 4_cols;
		REQUIRE(solution.size() == p_count.value() * p_cols.value() * p_rows.value());

		const auto img = device_matrix<T>{thrust::device_vector<T>{vec}, rows, cols, col_maj};

		WHEN("patches are extracted")
		{
			const auto patches = extract_patches(img, p_rows, p_cols);

			THEN("the extracted patches equal the known solution")
			{
				CHECK(patches.patch_count() == p_count.value());
				CHECK(patches.rows_patches() == p_rows.value());
				CHECK(patches.cols_patches() == p_cols.value());
				CHECK(::get_host_vector(patches) == solution);
			}
		}
	}
}

TEST_CASE("Extract patches (benchmark)", "[extract_patches_benchmark][!benchmark]")
{
	const auto img = rand_matrix(IMG_SIZE_BENCHMARK, BENCHMARK_T{});
	BENCHMARK("Extract patches")
	{
		return extract_patches(img, PATCH_SIZE_BENCHMARK);
	};
}