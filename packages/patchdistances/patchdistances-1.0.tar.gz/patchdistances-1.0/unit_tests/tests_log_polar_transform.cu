#define CATCH_CONFIG_ENABLE_BENCHMARKING

#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_matrix.h"
#include "../include/extract_patches.h"
#include "../include/log_polar_transform.h"
#include "../include/utils.h"
#include "data_similar.h"
#include "utils.h"

#include <cstddef>

TEMPLATE_TEST_CASE("Log-polar transform (w/o embedding)", "[log_polar_transform][template]", float,
				   double, vec3<float>, vec3<double>)
{
	GIVEN("Patches (embedded in a black background)")
	{
		const auto patches_col_maj = data_similar::patches_rhs(TestType{});
		const auto patches_row_maj = to_row_maj(patches_col_maj);
		const auto solution = data_similar::patches_rhs_log_polar(TestType{});
		const auto solution_t = transpose(solution);

		const auto lp_rows = Rows{solution.rows_patches()};
		const auto lp_cols = Cols{solution.cols_patches()};
		const auto already_embedded = false;
		const auto transposed = true;

		WHEN("applying log-polar transformation")
		{
			const auto log_polar_col_maj = log_polar_transform(patches_col_maj, lp_rows, lp_cols,
															   already_embedded, !transposed);
			const auto log_polar_col_maj_t = log_polar_transform(patches_col_maj, lp_rows, lp_cols,
																 already_embedded, transposed);

			const auto log_polar_row_maj = log_polar_transform(patches_row_maj, lp_rows, lp_cols,
															   already_embedded, !transposed);
			const auto log_polar_row_maj_t = log_polar_transform(patches_row_maj, lp_rows, lp_cols,
																 already_embedded, transposed);

			THEN("the interpolation equals the known solution")
			{
				const auto eps = 0.0;
				const auto margin = 0.01;
				is_equal(log_polar_col_maj, solution, eps, margin);
				is_equal(log_polar_col_maj_t, solution_t, eps, margin);
				is_equal(log_polar_row_maj, to_row_maj(solution), eps, margin);
				is_equal(log_polar_row_maj_t, to_row_maj(solution_t), eps, margin);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Log-polar inverse transform (w/o embedding)", "[log_polar_transform][template]",
				   float, double, vec3<float>, vec3<double>)
{
	GIVEN("Log polar transformed patches (embedded in a black background)")
	{
		const auto already_embedded = false;
		const auto transposed = true;

		const auto original = data_similar::patches_rhs(TestType{});
		const auto patches_col_maj =
			log_polar_transform(original, 80_rows, 100_cols, already_embedded, !transposed);
		const auto patches_row_maj = to_row_maj(patches_col_maj);
		const auto patches_col_maj_t = transpose(patches_col_maj);
		const auto patches_row_maj_t = transpose(patches_row_maj);

		const auto solution = data_similar::patches_rhs(TestType{});

		const auto rows = Rows{solution.rows_patches()};
		const auto cols = Cols{solution.cols_patches()};

		WHEN("applying inverse log-polar transformation")
		{
			const auto log_polar_inv_col_maj =
				log_polar_inv_transform(patches_col_maj, rows, cols, already_embedded, !transposed);
			const auto log_polar_inv_col_maj_t = log_polar_inv_transform(
				patches_col_maj_t, rows, cols, already_embedded, transposed);

			const auto log_polar_inv_row_maj =
				log_polar_inv_transform(patches_row_maj, rows, cols, already_embedded, !transposed);
			const auto log_polar_inv_row_maj_t = log_polar_inv_transform(
				patches_row_maj_t, rows, cols, already_embedded, transposed);

			THEN("the result equals the original patches")
			{
				const auto eps = 0.0;
				const auto margin = 0.01;
				is_equal(log_polar_inv_col_maj, solution, eps, margin);
				is_equal(log_polar_inv_col_maj_t, solution, eps, margin);
				is_equal(log_polar_inv_row_maj, to_row_maj(solution), eps, margin);
				is_equal(log_polar_inv_row_maj_t, to_row_maj(solution), eps, margin);
			}
		}
	}
}

// TODO: Maybe add a test with embedded log-polar transform. Though, the function implementation is
// the same as w/o embedding, just with a different interpolation radius.

TEST_CASE("Log polar transform (benchmark)", "[log_polar_transform_benchmark][!benchmark]")
{
	const auto patches = rand_patches(PATCH_COUNT_BENCHMARK, PATCH_SIZE_BENCHMARK, BENCHMARK_T{});
	const auto embed = true;
	const auto transpose = true;

	BENCHMARK("Log-polar transform")
	{
		return log_polar_transform(patches, 16_rows, 16_cols, embed, transpose);
	};
}