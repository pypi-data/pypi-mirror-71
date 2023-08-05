/*! \file enums.h
	\brief Global enum declarations.
	\sa affine_inv_dist, sim_inv_dist, rec_image.h, warp_perspective.h
*/

#pragma once

#include "Cols.h"
#include "Rows.h"

#include <cstddef>

//! Interpolation methods.
/*!
 * \sa warp_perspective.h
 */
enum class interpolation_t
{
	nn, /*!<nearest neighbor*/
	bicubic, /*!<bicubic*/
};

//! Methods for image reconstructing, meaning the averaging method of overlapping pixels.
/*!
 * \sa rec_image.h
 */
enum class rec_t
{
	median, /*!<Median*/
	mean /*!<Mean*/
};

//! Methods solving overdetermined linear systems.
/*!
 * \sa affine_inv_dist, least_squares_solver.h, procrustes_solver.h, identity_solver.h
 */
enum class solver_t
{
	least_squares, /*!<Ordinary least squares solver.*/
	procrustes, /*!<Least squares with restriction to orthogonal matrices.*/
	identity /*!<The result is always the identity. Reference.*/
};

//! Families of linearly independent functions.
/*!
 * \sa affine_inv_dist
 */
enum class func_family_t
{
	superlevelsets, /*!<Super level sets*/
	clip /*!<Clipping functions*/
};

//! Parameters for the affine invariant distance.
/*!
 * \sa affine_inv_dist
 */
struct aid_params
{
	solver_t solver = solver_t::least_squares; /*!<Method solving overdetermined linear systems.*/
	func_family_t func_family = func_family_t::clip; /*!<Type of the function family.*/
	size_t levels = 10; /*!<Size of the function family.*/
	bool higher_order_moments =
		false; /*!<If true, use higher order moments, otherwise first ones.*/
	bool imed = false; /*!<If true, use Image euclidean distance, otherwise euclidean distance.*/
	interpolation_t interpolation = interpolation_t::bicubic; /*!< Image interpolation method.*/
};

//! Parameters for the similarity invariant distance.
/*!
 * \sa sim_inv_dist
 */
struct sid_params
{
	size_t log_polar_size = 16; /*!< Rows/ Columns for log polar interpolation.*/
	Rows descriptors_rows = 4_rows; /*!< Row dimension of the descriptors. 2K+1 <= log_polar_size.*/
	Cols descriptors_cols = 4_cols; /*!< Col dimension of the descriptors. 2V+1 <= log_polar_size*/
	float sigma = 0.5f; /*!< Fourier-Mellin-Coefficient.*/
};