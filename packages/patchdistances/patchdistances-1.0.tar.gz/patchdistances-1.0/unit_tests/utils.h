#pragma once

#include "../include/Size.h"
#include "../include/patch_index.h"
#include "../include/utils.h"

#include <Catch2/single_include/catch2/catch.hpp>

#include <ostream>
#include <string>

template<typename>
class device_matrix;

template<typename>
class device_patches;

template<typename T>
struct vec3;

struct float2;
using cuComplex = float2;

struct double2;
using cuDoubleComplex = double2;

/*
** Default parameters for benchmarking.
*/

const auto IMG_SIZE_BENCHMARK = Size{525_rows, 525_cols};
const auto PATCH_SIZE_BENCHMARK = Size{11_rows, 11_cols};
const auto LABEL_COUNT_BENCHMARK = 20_patches;
const auto PATCH_COUNT_SIZE_BENCHMARK = patch_count_size(IMG_SIZE_BENCHMARK, PATCH_SIZE_BENCHMARK);
const auto PATCH_COUNT_BENCHMARK = patch_index{PATCH_COUNT_SIZE_BENCHMARK.total()};
const auto T_SIZE_BENCHMARK = Size{20_rows, 3_cols};
using BENCHMARK_T = vec3<float>;

/*
** Functions that return random matrices and patches using uniform distribution with values in
** [0,1).
*/

device_matrix<float> rand_matrix(Size s, float tag);
device_matrix<double> rand_matrix(Size s, double tag);
device_matrix<vec3<float>> rand_matrix(Size s, vec3<float> tag);
device_matrix<vec3<double>> rand_matrix(Size s, vec3<double> tag);

device_patches<float> rand_patches(patch_index p, Size s, float tag);
device_patches<double> rand_patches(patch_index p, Size s, double tag);
device_patches<vec3<float>> rand_patches(patch_index p, Size s, vec3<float> tag);
device_patches<vec3<double>> rand_patches(patch_index p, Size s, vec3<double> tag);

/*
** Catch2 checks, which compare matrices and patches. Eps is the expected L2 error (for each patch/
** matrix) and margin its error margin.
*/

void is_equal(const device_patches<float>& lhs, const device_patches<float>& rhs, double eps,
			  double margin);
void is_equal(const device_patches<double>& lhs, const device_patches<double>& rhs, double eps,
			  double margin);
void is_equal(const device_patches<vec3<float>>& lhs, const device_patches<vec3<float>>& rhs,
			  double eps, double margin);
void is_equal(const device_patches<vec3<double>>& lhs, const device_patches<vec3<double>>& rhs,
			  double eps, double margin);

void is_equal(const device_patches<cuComplex>& lhs, const device_patches<cuComplex>& rhs,
			  double eps, double margin);
void is_equal(const device_patches<cuDoubleComplex>& lhs,
			  const device_patches<cuDoubleComplex>& rhs, double eps, double margin);
void is_equal(const device_patches<vec3<cuComplex>>& lhs,
			  const device_patches<vec3<cuComplex>>& rhs, double eps, double margin);
void is_equal(const device_patches<vec3<cuDoubleComplex>>& lhs,
			  const device_patches<vec3<cuDoubleComplex>>& rhs, double eps, double margin);

void is_equal(const device_matrix<size_t>& lhs, const device_matrix<size_t>& rhs, double eps,
			  double margin);
void is_equal(const device_matrix<float>& lhs, const device_matrix<float>& rhs, double eps,
			  double margin);
void is_equal(const device_matrix<double>& lhs, const device_matrix<double>& rhs, double eps,
			  double margin);
void is_equal(const device_matrix<vec3<float>>& lhs, const device_matrix<vec3<float>>& rhs,
			  double eps, double margin);
void is_equal(const device_matrix<vec3<double>>& lhs, const device_matrix<vec3<double>>& rhs,
			  double eps, double margin);

void not_equal(const device_matrix<float>& lhs, const device_matrix<float>& rhs, double eps,
			   double margin);
void not_equal(const device_matrix<double>& lhs, const device_matrix<double>& rhs, double eps,
			   double margin);
void not_equal(const device_matrix<vec3<float>>& lhs, const device_matrix<vec3<float>>& rhs,
			   double eps, double margin);
void not_equal(const device_matrix<vec3<double>>& lhs, const device_matrix<vec3<double>>& rhs,
			   double eps, double margin);

//! A template function that appends device_patches.
/*!
 * \param i_patches1 Left hand side patches.
 * \param i_patches2 Right hand side patches with the same memory layout.
 * \return Appended device_patches.
 */
template<typename T>
device_patches<T> append(const device_patches<T>& i_patches1, const device_patches<T>& i_patches2)
{
	Expects(i_patches1.patch_count() > 0);
	Expects(i_patches2.patch_count() > 0);
	Expects(i_patches1.size_patches() == i_patches2.size_patches());
	Expects(i_patches1.col_maj_patches() == i_patches2.col_maj_patches());

	const auto count = patch_index{i_patches1.patch_count() + i_patches2.patch_count()};
	auto out = device_patches<T>{count, i_patches1.size_patches(), i_patches1.col_maj_patches()};

	const auto count1 = patch_index{i_patches1.patch_count()};
	thrust::copy(i_patches1.cbegin(), i_patches1.cend(), out.begin());
	thrust::copy(i_patches2.cbegin(), i_patches2.cend(), out.begin(count1));

	return out;
}

//! A template function that appends device_patches.
/*!
 * \param i_patches1 Left hand side patches.
 * \param i_patches2 Right hand side patches with the same memory layout.
 * \return Appended device_patches.
 */
template<typename T>
device_patches<T> append(device_patches<T>& i_patches1, const device_patches<T>& i_patches2)
{
	Expects(i_patches1.patch_count() > 0);
	Expects(i_patches2.patch_count() > 0);
	Expects(i_patches1.size_patches() == i_patches2.size_patches());
	Expects(i_patches1.col_maj_patches() == i_patches2.col_maj_patches());

	auto data = std::move(i_patches1).container();
	data.insert(data.end(), i_patches2.container().cbegin(), i_patches2.container().cend());
	const auto count = patch_index{i_patches1.patch_count() + i_patches2.patch_count()};
	const auto size = i_patches1.size_patches();
	const auto col_maj = i_patches1.col_maj_patches();

	return device_patches<T>{std::move(data), count, size, col_maj};
}

//! A template function that appends device_patches.
/*!
 * \param i_patches1 Left hand side patches.
 * \param i_patches2 Right hand side patches with the same memory layout.
 * \param args List of patches to append to [i_patches1, i_patches2].
 * \return Appended device_patches.
 */
template<typename T, typename... Args>
device_patches<T> append(const device_patches<T>& i_patches1, const device_patches<T>& i_patches2,
						 Args... args)
{
	return append(append(i_patches1, i_patches2), std::forward<Args>(args)...);
}