#define CATCH_CONFIG_ENABLE_BENCHMARKING

#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_matrix.h"
#include "../include/imed.h"
#include "../include/utils.h"
#include "utils.h"

#include <thrust/device_vector.h>
#include <vector>

template<typename T>
std::vector<T> tile(const std::vector<T>& in, std::size_t k)
{
	auto out = std::vector<T>{};
	out.reserve(k * in.size());
	for(size_t i = 0; i < k; i++)
	{
		out.insert(out.begin(), in.begin(), in.end());
	}

	return out;
}

TEMPLATE_TEST_CASE("IMED (set of small patches)", "[imed]", float, double, vec3<float>,
				   vec3<double>)
{
	using T = TestType;

	GIVEN("A set of small images")
	{
		const auto count = 50_patches;
		const auto rows = 5_rows;
		const auto cols = 5_cols;
		constexpr auto col_maj = true;

		const auto img_vec = [count] {
			const auto patch = std::vector<T>{
				T{1.0}, T{0.0}, T{1.0}, T{0.0}, T{1.0}, // patch 0
				T{0.0}, T{1.0}, T{0.0}, T{1.0}, T{0.0}, //
				T{1.0}, T{0.0}, T{1.0}, T{0.0}, T{1.0}, //
				T{0.0}, T{1.0}, T{0.0}, T{1.0}, T{0.0}, //
				T{1.0}, T{0.0}, T{1.0}, T{0.0}, T{1.0}, //
				T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, // patch 1
				T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
				T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
				T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
				T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0} //
			};
			return tile(patch, count.value() / 2);
		}();
		const auto img_cft_ref_vec = [count] {
			const auto patch = std::vector<T>{
				T{0.35760425f}, T{0.36290436f}, T{0.40768982f}, T{0.36290436f}, T{0.35760425f}, // 0
				T{0.36290436f}, T{0.49900148f}, T{0.48617374f}, T{0.49900148f}, T{0.36290436f}, //
				T{0.40768982f}, T{0.48617374f}, T{0.50493589f}, T{0.48617374f}, T{0.40768982f}, //
				T{0.36290436f}, T{0.49900148f}, T{0.48617374f}, T{0.49900148f}, T{0.36290436f}, //
				T{0.35760425f}, T{0.36290436f}, T{0.40768982f}, T{0.36290436f}, T{0.35760425f}, //
				T{0.0},			T{0.0},			T{0.0},			T{0.0},			T{0.0}, // 1
				T{0.0},			T{0.0},			T{0.0},			T{0.0},			T{0.0}, //
				T{0.0},			T{0.0},			T{0.0},			T{0.0},			T{0.0}, //
				T{0.0},			T{0.0},			T{0.0},			T{0.0},			T{0.0}, //
				T{0.0},			T{0.0},			T{0.0},			T{0.0},			T{0.0} //
			};
			return tile(patch, count.value() / 2);
		}();

		REQUIRE(img_vec.size() == count.value() * cols.value() * rows.value());
		REQUIRE(img_cft_ref_vec.size() == count.value() * cols.value() * rows.value());

		const auto img =
			device_patches<T>{thrust::device_vector<T>{img_vec}, count, rows, cols, col_maj};
		const auto img_cft_ref = device_patches<T>{thrust::device_vector<T>{img_cft_ref_vec}, count,
												   rows, cols, col_maj};

		WHEN("Convolution Standardized Transform (CFT) is applied (shared memory version)")
		{
			const auto img_cft = imed_cft(img);

			THEN("it equals the known solution.")
			{
				const auto eps = 0.0;
				const auto margin = 0.0001;
				is_equal(img_cft, img_cft_ref, eps, margin);
			}
		}
	}
}

TEST_CASE("IMED (benchmark)", "[imed][!benchmark]")
{
	const auto patches = rand_patches(PATCH_COUNT_BENCHMARK, PATCH_SIZE_BENCHMARK, BENCHMARK_T{});

	BENCHMARK("IMED")
	{
		return imed_cft(patches);
	};
}