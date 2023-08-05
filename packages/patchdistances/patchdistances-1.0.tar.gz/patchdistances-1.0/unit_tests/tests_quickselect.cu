#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/partition_NA.h"
#include "../include/quickselect.h"

#include <vector>

TEMPLATE_TEST_CASE("Quickselect (Median) (grey)", "[quickselect]", float, double)
{
	GIVEN("A vector with elements (including NA/undefined values)")
	{
		constexpr auto NA = details::NA;
		auto vec_uneven = std::vector<TestType>{NA, 1.0, 0.5, 0.25, NA, NA, 0.2, NA, 0.1};
		auto vec_even = std::vector<TestType>{NA, 1.0, 0.5, 0.3, NA, NA, 0.2, NA, 0.1, 0.1};
		constexpr auto median = 0.25;

		WHEN("the median is computed")
		{
			const auto uneven_size =
				partition_NA(vec_uneven.data(), gsl::narrow_cast<int>(vec_uneven.size()));
			const auto median_uneven = quickselect(vec_uneven.data(), uneven_size, uneven_size / 2);

			const auto even_size =
				partition_NA(vec_even.data(), gsl::narrow_cast<int>(vec_even.size()));
			const auto median_even =
				0.5f * (quickselect(vec_even.data(), even_size, even_size / 2 - 1) +
						quickselect(vec_even.data(), even_size, even_size / 2));

			THEN("it equals the known solution")
			{
				CHECK(median == median_uneven);
				CHECK(median == median_even);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Quickselect (Median) (rgb)", "[quickselect]", float, double)
{
	using T = vec3<double>;
	GIVEN("A vector with elements (including NA/undefined values)")
	{
		constexpr auto NA = details::NA;
		auto vec_uneven = std::vector<T>{T{NA},
										 T{1.0, 2.0, 3.0},
										 T{0.5, 1.0, 1.5},
										 T{0.25, 0.5, 0.75},
										 T{NA},
										 T{NA},
										 T{0.2, 0.4, 0.6},
										 T{NA},
										 T{0.1, 0.2, 0.3}};
		auto vec_even = std::vector<T>{T{NA},
									   T{1.0, 2.0, 3.0},
									   T{0.5, 1.0, 1.5},
									   T{0.3, 0.6, 0.9},
									   T{NA},
									   T{NA},
									   T{0.2, 0.4, 0.6},
									   T{NA},
									   T{0.1, 0.2, 0.3},
									   T{0.1, 0.2, 0.3}};
		const auto median = T{0.25, 0.5, 0.75};

		WHEN("the median is computed")
		{
			const auto uneven_size =
				partition_NA(vec_uneven.data(), gsl::narrow_cast<int>(vec_uneven.size()));
			const auto median_uneven = quickselect(vec_uneven.data(), uneven_size, uneven_size / 2);

			const auto even_size =
				partition_NA(vec_even.data(), gsl::narrow_cast<int>(vec_even.size()));
			const auto median_even =
				0.5f * (quickselect(vec_even.data(), even_size, even_size / 2 - 1) +
						quickselect(vec_even.data(), even_size, even_size / 2));

			THEN("it equals the known solution")
			{
				CHECK(median == median_uneven);
				CHECK(median == median_even);
			}
		}
	}
}