#define CATCH_CONFIG_ENABLE_BENCHMARKING

#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_matrix.h"
#include "../include/nearest_neighbor.h"
#include "../include/utils.h"
#include "utils.h"

#include <vector>

TEST_CASE("Nearest neighbor labeling", "[nearest_neighbour]")
{
	GIVEN("A distance matrix")
	{
		const auto vec = std::vector<double>{
			1.0, 4.0, 3.0, 2.0, //
			2.0, 1.1, 4.1, 3.0, //
			3.0, 2.0, 1.2, 4.2, //
			4.3, 3.0, 2.0, 1.3, //
		};
		const auto rows = 4_rows;
		const auto cols = 4_cols;
		const auto col_maj = true;

		const auto solution_min = std::vector<size_t>{0, 1, 2, 3};
		const auto solution_max = std::vector<size_t>{3, 0, 1, 2};

		const auto solution_dist_min = std::vector<double>{1.0, 1.1, 1.2, 1.3};
		const auto solution_dist_max = std::vector<double>{4.3, 4.0, 4.1, 4.2};

		const auto size_nn = Size{2_rows, 2_cols};

		const auto mat = device_matrix<double>{vec, rows, cols, col_maj};

		WHEN("the nearest neighbors are computed")
		{
			constexpr auto min = true;
			const auto neigh_dist_min = nearest_neighbor_w_distances(mat, size_nn, min);
			const auto neigh_dist_max = nearest_neighbor_w_distances(mat, size_nn, !min);

			const auto neigh_min = std::get<0>(neigh_dist_min);
			const auto dist_min = std::get<1>(neigh_dist_min);
			const auto neigh_max = std::get<0>(neigh_dist_max);
			const auto dist_max = std::get<1>(neigh_dist_max);

			THEN("they equal the solution")
			{
				CHECK(neigh_min.size() == size_nn);
				CHECK(neigh_max.size() == size_nn);

				CHECK(get_host_vector(neigh_min) == solution_min);
				CHECK(get_host_vector(neigh_max) == solution_max);

				CHECK(dist_min.size() == size_nn);
				CHECK(dist_max.size() == size_nn);

				CHECK(get_host_vector(dist_min) == solution_dist_min);
				CHECK(get_host_vector(dist_max) == solution_dist_max);
			}
		}
	}
}

TEST_CASE("Nearest neighbor labeling (benchmark)", "[nearest_neighbor][!benchmark]")
{
	const auto rows = Rows{PATCH_COUNT_BENCHMARK.value()};
	const auto cols = Cols{LABEL_COUNT_BENCHMARK.value()};
	const auto matrix = rand_matrix(Size{rows, cols}, double{});
	constexpr auto min = true;

	BENCHMARK("Nearest neighbor")
	{
		return nearest_neighbor(matrix, PATCH_COUNT_SIZE_BENCHMARK, min);
	};
}