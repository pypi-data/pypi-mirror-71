#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_patches.h"
#include "../include/identity_solver.h"
#include "utils.h"

#include <vector>

TEST_CASE("Identity solver")
{
	const auto id = std::vector<float>{1.0f, 0.0f, 0.0f, //
									   0.0f, 1.0f, 0.0f, //
									   0.0f, 0.0f, 1.0f};
	const auto data = [&id] {
		auto tmp = id;
		tmp.insert(tmp.end(), id.cbegin(), id.cend());
		tmp.insert(tmp.end(), id.cbegin(), id.cend());
		return tmp;
	}();
	const auto row_maj = false;
	const auto solution = device_patches<float>{data, 3_patches, 3_rows, 3_cols, row_maj};

	const auto result = identity_solver(3);

	constexpr auto eps = 0.0;
	constexpr auto margin = 0.0;
	is_equal(result, solution, eps, margin);
}