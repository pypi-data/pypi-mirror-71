#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/partition_NA.h"

#include <array>

TEST_CASE("Partition NA", "[nearest_neighbour]")
{
	constexpr auto NA = details::NA;
	auto data = std::array<double, 10>{0.1, 0.2, NA, NA, 1.0, NA, 0.0, 2.0, -10.0, NA};

	const auto non_NA_count = partition_NA(data.data(), data.size());

	CHECK(non_NA_count == 6);
	CHECK(data[0] == 0.1);
	CHECK(data[1] == 0.2);
	CHECK(data[2] == 1.0);
	CHECK(data[3] == 0.0);
	CHECK(data[4] == 2.0);
	CHECK(data[5] == -10.0);
	// The second partition is unspecified.
}