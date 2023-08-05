/*! \file procrustes_solver.h
	\brief Solving image moments of the affine_invariant_distance for the rotation group (instead of
   affine group). \sa affine_inv_dist, warp_perspective.h
*/

#pragma once

template<typename T>
class device_patches;

class Size;

struct cublasContext;
typedef struct cublasContext* cublasHandle_t;
/**< Forward declaration of cublasHandle_t. */

//! A function computing the affine transformations of image patches, based on the image moments.
/*!
 * \param lhs Image moments.
 * \param rhs Image moments.
 * \param patch_size Size of the images corresponding to the moments.
 * \param cublas_h Initialized cublas handle.
 * \return Rotations associated to the image moments but in the more general format of
 * perspective transformations.
 */
device_patches<float> procrustes_solver(const device_patches<float>& lhs,
										const device_patches<float>& rhs, const Size& patch_size,
										cublasHandle_t cublas_h);

/*!
 * \overload
 */
device_patches<float> procrustes_solver(const device_patches<double>& lhs,
										const device_patches<double>& rhs, const Size& patch_size,
										cublasHandle_t cublas_h);