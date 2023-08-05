/*! \file determinant.h
    \brief Utilities to compute the determinant used in the affine invariant distance.
    \sa affine_inv_dist
*/

#pragma once

#include <thrust/device_vector.h>

template<typename T>
class device_patches;

//! Templated function to compute the determinant of an affine transformation from patch moments.
/*!
 * \param i_Tf A set of image moment matrices T.
 * \param i_Tg A set of image moment matrices T.
 * \return Determinants of the affine transformation associated to the pair of moments i_Tf[i],
 * i_Tg[i].
 */
thrust::device_vector<float> determinant(const device_patches<float>& i_Tf,
										 const device_patches<float>& i_Tg);

/*!
 * \overload
 */
thrust::device_vector<double> determinant(const device_patches<double>& i_Tf,
										  const device_patches<double>& i_Tg);