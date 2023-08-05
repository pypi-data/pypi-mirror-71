/*! \file nearest_neighbor.h
	\brief Nearest neighbor for distance matrices.
*/

#pragma once

#include <utility>

template<typename T>
class device_matrix;

template<typename T>
class vec3;

class Size;

//! Function that computes the nearest neighbors from a distance matrix.
/*!
 * \param i_dist_mat The nearest neighbor (minimum or maximum) of each row will be computed. Expects
 * column-major layout.
 * \param i_image_size The size of the output matrix. Rows * columns = rows of i_dist_matrix.
 * \param i_min If true the nearest neighbor is defined as the minimum value. Otherwise as the
 * maximum.
 * \return Matrix of indices of the nearest neighbors.
 */
device_matrix<size_t> nearest_neighbor(const device_matrix<double>& i_dist_mat,
									   const Size& i_image_size, bool i_min = true);

//! Function that computes the nearest neighbors from a distance matrix and also returns the
//! realising distances.
/*!
 * \param i_dist_mat The nearest neighbor (minimum or maximum) of each row will be computed. Expects
 * column-major layout.
 * \param i_image_size The size of the output matrix. Rows * columns = rows of i_dist_matrix.
 * * \param i_min If true the nearest neighbor is defined as the minimum value. Otherwise as the
 * maximum.
 * \return Matrix of indices of the nearest neighbors and the realising distances.
 */
std::pair<device_matrix<size_t>, device_matrix<double>>
	nearest_neighbor_w_distances(const device_matrix<double>& i_dist_mat, const Size& i_image_size,
								 bool i_min = true);