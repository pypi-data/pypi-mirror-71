#include "../include/Size.h"
#include "../include/device_patches.h"
#include "../include/identity_solver.h"
#include "../include/patch_index.h"

#include <thrust/for_each.h>
#include <thrust/iterator/counting_iterator.h>

device_patches<float> identity_solver(std::size_t patch_count)
{
	const auto fill_val = 0.0f;
	const auto row_maj = false;
	auto transformations =
		device_patches<float>{patch_index{patch_count}, 3_rows, 3_cols, fill_val, row_maj};
	auto ptr = transformations.data().get();

	const auto begin = thrust::counting_iterator<std::size_t>{0};
	const auto end = thrust::counting_iterator<std::size_t>{patch_count};
	thrust::for_each(begin, end, [=] __device__(std::size_t patch) {
		auto p_ptr = ptr + 3 * 3 * patch;
		p_ptr[0] = 1.0f;
		p_ptr[4] = 1.0f;
		p_ptr[8] = 1.0f;
	});

	return transformations;
}