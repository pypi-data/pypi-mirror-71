/*! \file least_squares_solver.h
	\brief Solving image moments of the affine_invariant_distance with least squares.
   \sa affine_inv_dist, warp_perspective.h
*/

#pragma once

class Size;

template<typename T>
class device_patches;

struct cublasContext;
typedef struct cublasContext* cublasHandle_t;
/**< Forward declaration of cublasHandle_t. */

//! Least squares for image moments.
/*!
 * \param lhs Image moments.
 * \param rhs Image moments.
 * \param patch_size Patch size associated to the affine transformations.
 * \param handle Initialized cublas handle.
 * \return Affine transformations associated to the image moments but in the more general format of
 * perspective transformations.
 */
device_patches<float> least_squares_solver(const device_patches<float>& lhs,
										   const device_patches<float>& rhs, const Size& patch_size,
										   cublasHandle_t handle);

/*!
 * \overload
 */
device_patches<float> least_squares_solver(const device_patches<double>& lhs,
										   const device_patches<double>& rhs,
										   const Size& patch_size, cublasHandle_t handle);