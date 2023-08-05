#include "utils.h"

#include "../extern/gsl/gsl_util"
#include "../include/device_matrix.h"
#include "../include/utils.h"

#include <thrust/copy.h>
#include <thrust/device_ptr.h>
#include <thrust/device_vector.h>
#include <thrust/for_each.h>
#include <thrust/host_vector.h>
#include <thrust/iterator/counting_iterator.h>

#include <vector>

bool is_grey(const py::array& array)
{
	// limitation: Patches of size 3x3 or smaller are not properly handled.
	if(array.ndim() == 2 || (array.ndim() == 3 && array.shape()[2] > 3))
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool is_rgb(const py::array& array)
{
	if((array.ndim() == 3 && array.shape()[2] == 3) || (array.ndim() == 4 && array.shape()[3] == 3))
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool is_matrix(const py::array& array)
{
	// limitation: Patches of size 3x3 or smaller are not properly handled.
	if(array.ndim() == 2 || (array.ndim() == 3 && array.shape()[2] == 3))
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool is_patches(const py::array& array)
{
	if((array.ndim() == 3 && array.shape()[2] > 3) || (array.ndim() == 4 && array.shape()[3] == 3))
	{
		return true;
	}
	else
	{
		return false;
	}
}

template<typename T>
device_matrix<T> upload_grey_matrix_impl(const py_array_col_maj<T>& i_matrix, T /*tag*/)
{
	Expects(i_matrix.ndim() == 2);

	const auto col_maj = true;
	const auto rows = gsl::narrow<size_t>(i_matrix.shape()[0]);
	const auto cols = gsl::narrow<size_t>(i_matrix.shape()[1]);

	return device_matrix<T>{
		thrust::device_vector<T>(i_matrix.data(), i_matrix.data() + i_matrix.size()), Rows{rows},
		Cols{cols}, col_maj};
}

device_matrix<size_t> upload_matrix(const py_array_col_maj<size_t>& i_matrix, size_t tag)
{
	return upload_grey_matrix_impl(i_matrix, tag);
}

device_matrix<double> upload_matrix(const py_array_col_maj<double>& i_matrix, double tag)
{
	return upload_grey_matrix_impl(i_matrix, tag);
}

device_matrix<float> upload_matrix(const py_array_col_maj<float>& i_matrix, float tag)
{
	return upload_grey_matrix_impl(i_matrix, tag);
}

device_patches<float> upload_patches(const py_array_row_maj<float>& i_patches, float /*tag*/)
{
	Expects(i_patches.ndim() == 3);

	const auto row_maj = false;
	const auto patches = gsl::narrow<size_t>(i_patches.shape()[0]);
	const auto rows = gsl::narrow<size_t>(i_patches.shape()[1]);
	const auto cols = gsl::narrow<size_t>(i_patches.shape()[2]);
	const auto out = device_patches<float>{
		thrust::device_vector<float>(i_patches.data(), i_patches.data() + i_patches.size()),
		patch_index{patches}, Rows{rows}, Cols{cols}, row_maj};

	return to_col_maj(out);
}

thrust::device_vector<vec3<float>> vectorize(const float* data, ssize_t size)
{
	Expects(size % 3 == 0);

	const auto begin = thrust::counting_iterator<ssize_t>(0);
	const auto end = begin + (size / 3);
	const auto float_vec = thrust::device_vector<float>(data, data + size);
	const auto float_ptr = float_vec.data().get();
	auto float3_vec = thrust::device_vector<vec3<float>>(size / 3);
	auto float3_ptr = float3_vec.data().get();

	thrust::for_each(begin, end, [=] __device__(ssize_t idx) {
		float3_ptr[idx] =
			vec3<float>{float_ptr[3 * idx], float_ptr[3 * idx + 1], float_ptr[3 * idx + 2]};
	});

	return float3_vec;
}

device_matrix<vec3<float>> upload_matrix(const py_array_row_maj<float>& i_matrix,
										 vec3<float> /*tag*/)
{
	Expects(i_matrix.ndim() == 3);
	Expects(i_matrix.shape()[2] == 3);

	const auto row_maj = false;
	const auto rows = gsl::narrow<size_t>(i_matrix.shape()[0]);
	const auto cols = gsl::narrow<size_t>(i_matrix.shape()[1]);
	const auto out = device_matrix<vec3<float>>{vectorize(i_matrix.data(), i_matrix.size()),
												Rows{rows}, Cols{cols}, row_maj};

	return to_col_maj(out);
}

device_patches<vec3<float>> upload_patches(const py_array_row_maj<float>& i_patches,
										   vec3<float> /*tag*/)
{
	Expects(i_patches.ndim() == 4);
	Expects(i_patches.shape()[3] == 3);

	const auto row_maj = false;
	const auto patches = gsl::narrow<size_t>(i_patches.shape()[0]);
	const auto rows = gsl::narrow<size_t>(i_patches.shape()[1]);
	const auto cols = gsl::narrow<size_t>(i_patches.shape()[2]);
	const auto out =
		device_patches<vec3<float>>{vectorize(i_patches.data(), i_patches.size()),
									patch_index{patches}, Rows{rows}, Cols{cols}, row_maj};

	return to_col_maj(out);
}

template<typename T, std::enable_if_t<std::is_arithmetic<T>::value, int> = 0>
py_array_col_maj<T> download_grey_matrix_impl(const device_matrix<T>& i_matrix)
{
	const auto mem_layout = [&]() {
		// safe, matrix dimensions are small
		const auto rows_mem = gsl::narrow<ssize_t>(sizeof(T) * i_matrix.rows());
		const auto cols_mem = gsl::narrow<ssize_t>(sizeof(T) * i_matrix.cols());
		using ret_t = std::vector<ssize_t>;
		return i_matrix.col_maj() ? ret_t{sizeof(T), rows_mem} : ret_t{cols_mem, sizeof(T)};
	}();

	const auto rows = gsl::narrow<ssize_t>(i_matrix.rows());
	const auto cols = gsl::narrow<ssize_t>(i_matrix.cols());

	auto host_vec = std::vector<T>(i_matrix.cbegin(), i_matrix.cend());
	const auto matrix_ptr = new std::vector<T>(std::move(host_vec));
	auto capsule = py::capsule(
		matrix_ptr, [](void* p) noexcept { delete gsl::narrow<decltype(matrix_ptr)>(p); });

	return py::array{{rows, cols}, mem_layout, matrix_ptr->data(), std::move(capsule)};
}

py_array_col_maj<size_t> download(const device_matrix<size_t>& i_matrix)
{
	return download_grey_matrix_impl(i_matrix);
}

py_array_col_maj<float> download(const device_matrix<float>& i_matrix)
{
	return download_grey_matrix_impl(i_matrix);
}

py_array_col_maj<double> download(const device_matrix<double>& i_matrix)
{
	return download_grey_matrix_impl(i_matrix);
}

py_array_row_maj<float> download(const device_patches<float>& i_patches)
{
	const auto mem_layout = [&]() {
		// safe, matrix dimensions are small
		const auto ld_mem = gsl::narrow<ssize_t>(sizeof(float) * i_patches.ld());
		const auto rows_mem = gsl::narrow<ssize_t>(sizeof(float) * i_patches.rows_patches());
		const auto cols_mem = gsl::narrow<ssize_t>(sizeof(float) * i_patches.cols_patches());
		using ret_t = std::vector<ssize_t>;
		return i_patches.col_maj_patches() ? ret_t{ld_mem, sizeof(float), rows_mem}
										   : ret_t{ld_mem, cols_mem, sizeof(float)};
	}();

	const auto count = gsl::narrow<ssize_t>(i_patches.patch_count());
	const auto rows = gsl::narrow<ssize_t>(i_patches.rows_patches());
	const auto cols = gsl::narrow<ssize_t>(i_patches.cols_patches());

	auto host_vec = std::vector<float>(i_patches.cbegin(), i_patches.cend());
	const auto matrix_ptr = new std::vector<float>(std::move(host_vec));
	auto capsule = py::capsule(
		matrix_ptr, [](void* p) noexcept { delete gsl::narrow<decltype(matrix_ptr)>(p); });

	return py::array{{count, rows, cols}, mem_layout, matrix_ptr->data(), std::move(capsule)};
}

std::vector<float> devectorize(const thrust::device_ptr<const vec3<float>>& data, ssize_t size)
{
	// reinterpret_cast is well defined, since vec3 has the proper padding and alignment.
	const auto float3_ptr =
		thrust::device_pointer_cast(reinterpret_cast<const float*>(thrust::raw_pointer_cast(data)));
	auto float_vec = std::vector<float>(3 * size);
	thrust::copy(float3_ptr, float3_ptr + 3 * size, float_vec.begin());

	return float_vec;
}

py_array_col_maj<float> download(const device_matrix<vec3<float>>& i_matrix)
{
	const auto mem_layout = [&]() {
		// safe, matrix dimensions are small
		const auto rows_mem = gsl::narrow<ssize_t>(sizeof(vec3<float>) * i_matrix.rows());
		const auto cols_mem = gsl::narrow<ssize_t>(sizeof(vec3<float>) * i_matrix.cols());
		using ret_t = std::vector<ssize_t>;
		return i_matrix.col_maj() ? ret_t{sizeof(vec3<float>), rows_mem, sizeof(float)}
								  : ret_t{cols_mem, sizeof(vec3<float>), sizeof(float)};
	}();

	const auto rows = gsl::narrow<ssize_t>(i_matrix.rows());
	const auto cols = gsl::narrow<ssize_t>(i_matrix.cols());
	const auto ch = ssize_t{3};

	const auto matrix_ptr = new std::vector<float>(devectorize(i_matrix.data(), i_matrix.total()));
	auto capsule = py::capsule(
		matrix_ptr, [](void* p) noexcept { delete gsl::narrow<decltype(matrix_ptr)>(p); });

	return py::array{{rows, cols, ch}, mem_layout, matrix_ptr->data(), std::move(capsule)};
}

py_array_row_maj<float> download(const device_patches<vec3<float>>& i_patches)
{
	const auto mem_layout = [&]() {
		// safe, matrix dimensions are small
		const auto ld_mem = gsl::narrow<ssize_t>(sizeof(vec3<float>) * i_patches.ld());
		const auto rows_mem = gsl::narrow<ssize_t>(sizeof(vec3<float>) * i_patches.rows_patches());
		const auto cols_mem = gsl::narrow<ssize_t>(sizeof(vec3<float>) * i_patches.cols_patches());
		using ret_t = std::vector<ssize_t>;
		return i_patches.col_maj_patches()
				   ? ret_t{ld_mem, sizeof(vec3<float>), rows_mem, sizeof(float)}
				   : ret_t{ld_mem, cols_mem, sizeof(vec3<float>), sizeof(float)};
	}();

	const auto count = gsl::narrow<ssize_t>(i_patches.patch_count());
	const auto rows = gsl::narrow<ssize_t>(i_patches.rows_patches());
	const auto cols = gsl::narrow<ssize_t>(i_patches.cols_patches());
	const auto ch = ssize_t{3};

	const auto matrix_ptr =
		new std::vector<float>(devectorize(i_patches.data(), i_patches.total()));
	auto capsule = py::capsule(
		matrix_ptr, [](void* p) noexcept { delete gsl::narrow<decltype(matrix_ptr)>(p); });

	return py::array{{count, rows, cols, ch}, mem_layout, matrix_ptr->data(), std::move(capsule)};
}