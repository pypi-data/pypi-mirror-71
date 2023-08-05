/*! \file greedy_k_center.h
	\brief Greedy k-center clustering for patches.
*/

#pragma once

#include "device_matrix.h"
#include "metric.h"

#include "../extern/gsl/gsl_assert"

#include <thrust/device_ptr.h>
#include <thrust/distance.h>
#include <thrust/extrema.h>
#include <thrust/for_each.h>
#include <thrust/iterator/counting_iterator.h>
#include <thrust/iterator/zip_iterator.h>

#include <cuda_runtime.h> // CUDA C++ API
#include <device_launch_parameters.h>

//! Implementation of the GreedyK_Center algorithm for patches.
//! For an explanation see also "Geometric Approximation Algorithms" by Sariel Har-Peled.
/*!
 * \param i_data_patches The input set of patches to cluster.
 * \param i_K The number of clusters.
 * \param i_first The index of the first patch.
 * \return The cluster centers.
 * \tparam T Value type of the patches.
 * \tparam Metric Patch distance. Needs to implement
 * static __device__ T compute(const T* lhs, const T* rhs, unsigned int i_length).
 * \sa metric
 */
template<typename Metric, typename T>
device_patches<T> greedy_k_center_impl(const device_patches<T>& i_data_patches, std::size_t i_K,
									   std::size_t i_first = std::size_t{0})
{
	Expects(i_data_patches.col_maj_patches());
	Expects(i_K > 1);
	Expects(i_first < i_data_patches.patch_count());

	// Output centers and temporary distances between patches.
	auto o_centers = device_patches<T>(patch_index{i_K}, i_data_patches.size_patches());
	auto distances = thrust::device_vector<float>(i_data_patches.rows());

	// Get raw pointers and variables needed in the device function because lambda device functions
	// have to catch by value.
	const auto stride_data = 1;
	const auto stride_centers = 1;
	const auto patch_size = i_data_patches.total_per_patch();
	const auto patch_ptr = i_data_patches.data().get();
	auto center_ptr = o_centers.data().get();
	auto distance_ptr = distances.data().get();

	const auto random_patch = i_data_patches.row_range(i_first);
	auto first_center = o_centers.row_range(0);
	thrust::copy(random_patch.begin(), random_patch.end(), first_center.begin());

	// Compute the distance between the patches and the first center.
	const auto first_pixel = thrust::counting_iterator<std::size_t>{0};
	const auto last_pixel = thrust::counting_iterator<std::size_t>{i_data_patches.patch_count()};

	thrust::for_each(first_pixel, last_pixel, [=] __device__(std::size_t val) {
		distance_ptr[val] = Metric::compute(patch_size, patch_ptr + val * patch_size, stride_data,
											center_ptr, stride_centers);
	});

	// Get the patch with the maximum distance to the first center.
	// Add this patch as the next center.
	const auto max = thrust::max_element(distances.cbegin(), distances.cend());
	const auto max_patch_index = thrust::distance(distances.cbegin(), max);

	// Copy the found patch to the output.
	const auto max_patch = i_data_patches.row_range(max_patch_index);
	auto second_center = o_centers.row_range(1);
	thrust::copy(max_patch.begin(), max_patch.end(), second_center.begin());

	// Iterate over the number of remaining centers.
	for(int i = 2; i < i_K; i++)
	{
		// Compute the distance between the patches and the last center.
		// Then take the minimum of this value and the last center.
		thrust::for_each(first_pixel, last_pixel, [=] __device__(std::size_t val) {
			const auto distance =
				Metric<T>::compute(patch_size, patch_ptr + val * patch_size, stride_data,
								   center_ptr + (i - 1) * patch_size, stride_centers);

			distance_ptr[val] = min(distance, distance_ptr[val]);
		});

		// Get the patch with the maximum distance to the last center.
		const auto max = thrust::max_element(distances.cbegin(), distances.cend());
		const auto max_patch_index = thrust::distance(distances.cbegin(), max);

		// Copy the found patch to the output.
		const auto max_patch = i_data_patches.row_range(max_patch_index);
		auto i_center = o_centers.row_range(i);
		thrust::copy(max_patch.begin(), max_patch.end(), i_center.begin());
	}

	return o_centers;
}

//! A member choosing k patches by applying the greedy-k-center algorithm.
/*!
 * \param i_patches Set of patches.
 * \param i_k The number of patches to pick.
 * \param i_func Function that computes a distance matrix (device_matrix) from two
 * set of patches (device_patches).
 * \param i_first The index of the first patch.
 * \return Indices of k patches.
 */
template<typename T, typename DistMatFunction>
std::vector<size_t> greedy_k_center_impl(const device_patches<T>& i_patches, size_t i_k,
										 DistMatFunction i_func, size_t i_first = size_t{0})
{
	Expects(i_k > 1);
	Expects(i_first < i_patches.patch_count());

	auto ind = std::vector<size_t>(i_k);
	ind.at(0) = i_first;

	for(size_t i = 1; i < i_k; i++)
	{
		const auto patch = copy(i_patches, std::vector<size_t>{ind.at(i - 1)});
		auto dist_mat = i_func(i_patches, patch);
		const auto max = thrust::max_element(dist_mat.cbegin(), dist_mat.cend());
		ind.at(i) = thrust::distance(dist_mat.cbegin(), max);
	}

	return ind;
}