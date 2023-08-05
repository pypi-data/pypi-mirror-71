#define CATCH_CONFIG_ENABLE_BENCHMARKING

#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_patches.h"
#include "../include/least_squares_solver.h"
#include "../include/unique_cublas_handle.h"
#include "../src/affine_inv_dist_impl.h"
#include "data_affine.h"
#include "data_orthogonal.h"
#include "utils.h"

TEMPLATE_TEST_CASE("Solve image moments with least squares", "[least_squares_solver]", float,
				   double)
{
	using T = TestType;

	GIVEN("matrices of first order moments T0 and T1")
	{
		const auto lhs = data_orthogonal::patches_lhs(T{});
		const auto rhs = data_orthogonal::patches_rhs(T{});

		const auto ff = func_family_t::clip;
		const auto levels = 4u;
		const auto first_order_moments = false;
		const auto T0 = image_moments(lhs, ff, levels, first_order_moments);
		const auto T1 = image_moments(rhs, ff, levels, first_order_moments);

		WHEN("(orthogonal) affine transformations are computed")
		{
			const unique_cublas_handle h{};
			const auto A = least_squares_solver(T0, T1, lhs.size_patches(), h.get());

			THEN("they equal the known solution")
			{
				const auto solution = data_orthogonal::perspective_matrices(T{});
				constexpr auto eps = 0.0;
				constexpr auto margin = 0.0;
				is_equal(A, solution, eps, margin);
			}
		}
	}

	// Remark: CUDA implementation is less robust than the python numpy implementation.
	// Some example that work with python do not work with CUDA.
	GIVEN("matrices of first order moments T0 and T1")
	{
		const auto lhs = data_affine::patches_lhs();
		const auto rhs = data_affine::patches_rhs();

		const auto ff = func_family_t::clip;
		const auto levels = 4u;
		const auto first_order_moments = false;
		const auto T0 = image_moments(lhs, ff, levels, first_order_moments);
		const auto T1 = image_moments(rhs, ff, levels, first_order_moments);

		WHEN("(non orthogonal) affine transformations are computed")
		{
			const unique_cublas_handle h{};
			const auto A = least_squares_solver(T0, T1, lhs.size_patches(), h.get());

			THEN("they equal the known solution")
			{
				const auto solution = data_affine::perspective_matrices();

				constexpr auto eps = 0.0;
				constexpr auto margin = 0.05;
				is_equal(A, solution, eps, margin);
			}
		}
	}
}

TEST_CASE("Least squares solver", "[!benchmark]")
{
	const auto T0 = rand_patches(PATCH_COUNT_BENCHMARK, T_SIZE_BENCHMARK, float{});
	const auto T1 = rand_patches(PATCH_COUNT_BENCHMARK, T_SIZE_BENCHMARK, float{});
	const unique_cublas_handle h{};

	BENCHMARK("Least squares")
	{
		return least_squares_solver(T0, T1, PATCH_SIZE_BENCHMARK, h.get());
	};
}