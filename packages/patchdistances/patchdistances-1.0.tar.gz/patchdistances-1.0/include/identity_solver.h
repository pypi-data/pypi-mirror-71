/*! \file identity_solver.h
	\brief Solving image moments of the affine_invariant_distance for the trivial group (instead of
   affine group).
   \sa affine_inv_dist, warp_perspective.h
*/

#pragma once

template<typename T>
class device_patches;

#include <cstddef>

//! A function that returns the identity perspective matrix for a given number of patches. This is
//! intended as the reference for comparing the other solvers.
/*!
 * \param patch_count Number of output transformations.
 * \return Identities but in the more general format of perspective transformations.
 */
device_patches<float> identity_solver(std::size_t patch_count);