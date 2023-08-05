#define CATCH_CONFIG_ENABLE_BENCHMARKING

#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_patches.h"
#include "../include/enums.h"
#include "../include/procrustes_solver.h"
#include "../include/unique_cublas_handle.h"
#include "../src/affine_inv_dist_impl.h"
#include "data_orthogonal.h"
#include "utils.h"

TEMPLATE_TEST_CASE("Solve image moments with procrustes", "[procrustes_solver]", float, double)
{
	using T = TestType;

	GIVEN("matrices of (first order) moments T0 and T1")
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
			const unique_cublas_handle cublas{};
			const auto As = procrustes_solver(T0, T1, lhs.size_patches(), cublas.get());

			THEN("it equals the known solution")
			{
				REQUIRE(As.patch_count() == T0.patch_count());
				const auto solution = data_orthogonal::perspective_matrices(T{});

				constexpr auto eps = 0.0;
				constexpr auto margin = 0.000001;
				is_equal(As, solution, eps, margin);
			}
		}
	}
}

__host__ __device__ void mat_mul_2x2(const float u[4], const float v[4], float* uv);
__host__ __device__ void mat_mul_2x2(const double u[4], const double v[4], double* uv);

TEMPLATE_TEST_CASE("2x2 matrix multiplication", "[procrustes_solver]", float, double)
{
	const TestType u[4] = {1.0f, 2.0f, 3.0f, 4.0f};
	const TestType v[4] = {5.0f, 6.0f, 7.0f, 8.0f};
	const TestType solution[4] = {23.0f, 34.0f, 31.0f, 46.0f};
	TestType uv[4];
	mat_mul_2x2(u, v, uv);

	CHECK(uv[0] == solution[0]);
	CHECK(uv[1] == solution[1]);
	CHECK(uv[2] == solution[2]);
	CHECK(uv[3] == solution[3]);
}

__host__ __device__ void svd_2x2(const float* a, float u[4], float v[4]);
__host__ __device__ void svd_2x2(const double* a, double u[4], double v[4]);

TEMPLATE_TEST_CASE("2x2 singular value decomposition", "[procrustes_solver]", float, double)
{
	const TestType A[4] = {1.0f, 2.0f, 3.0f, 4.0f};
	const TestType u_solution[4] = {-0.576f, -0.8174f, -0.8174f, 0.576f};
	const TestType v_solution[4] = {-0.4046f, 0.9145f, -0.9145f, -0.4046f};
	TestType u[4];
	TestType v[4];
	svd_2x2(&A[0], u, v);

	CHECK(u[0] == Approx(u_solution[0]).margin(0.001));
	CHECK(u[1] == Approx(u_solution[1]).margin(0.001));
	CHECK(u[2] == Approx(u_solution[2]).margin(0.001));
	CHECK(u[3] == Approx(u_solution[3]).margin(0.001));

	CHECK(v[0] == Approx(v_solution[0]).margin(0.001));
	CHECK(v[1] == Approx(v_solution[1]).margin(0.001));
	CHECK(v[2] == Approx(v_solution[2]).margin(0.001));
	CHECK(v[3] == Approx(v_solution[3]).margin(0.001));
}

TEST_CASE("Procrustes solver", "[!benchmark]")
{
	const auto T0 = rand_patches(PATCH_COUNT_BENCHMARK, T_SIZE_BENCHMARK, float{});
	const auto T1 = rand_patches(PATCH_COUNT_BENCHMARK, T_SIZE_BENCHMARK, float{});
	const unique_cublas_handle h{};

	BENCHMARK("Procrustes")
	{
		return procrustes_solver(T0, T1, PATCH_SIZE_BENCHMARK, h.get());
	};
}