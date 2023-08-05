/*! \file log_polar_transform.h
	\brief Log polar transform and its inverse for patches.
*/

#pragma once

template<typename T>
class device_patches;

template<typename T>
struct vec3;

class Size;
class Cols;
class Rows;

//! Computes the log-polar transform of a set of patch with bi-cubic interpolation.
/*!
 * \param i_patches One patch per row.
 * \param i_M Number of rows of the interpolated patches.
 * \param i_N Number of columns of the interpolated patches.
 * \param i_embed If true the patches are embedded in a black background first.
 * \param i_transpose If true the output will be transposed.
 * Otherwise, the largest disk contained in the patches is interpolated.
 */
device_patches<float> log_polar_transform(const device_patches<float>& i_patches, Rows i_M,
										  Cols i_N, bool i_embed, bool i_transpose);

/*!
 * \overload
 */
device_patches<double> log_polar_transform(const device_patches<double>& i_patches, Rows i_M,
										   Cols i_N, bool i_embed, bool i_transpose);

/*!
 * \overload
 */
device_patches<vec3<float>> log_polar_transform(const device_patches<vec3<float>>& i_patches,
												Rows i_M, Cols i_N, bool i_embed, bool i_transpose);

/*!
 * \overload
 */
device_patches<vec3<double>> log_polar_transform(const device_patches<vec3<double>>& i_patches,
												 Rows i_M, Cols i_N, bool i_embed,
												 bool i_transpose);

//! Computes the log-polar inverse transform of a set of patch with bi-cubic interpolation.
/*!
 * \param i_patches One patch per row.
 * \param i_Y Number of rows of the interpolated patches.
 * \param i_X Number of columns of the interpolated patches.
 * \param i_embed If true the patches are embedded in a black background first.
 * \param i_transposed If true the input is transposed.
 * Otherwise, the largest disk contained in the patches is interpolated.
 */
device_patches<float> log_polar_inv_transform(const device_patches<float>& i_patches, Rows i_Y,
											  Cols i_X, bool i_embed, bool i_transposed);

/*!
 * \overload
 */
device_patches<double> log_polar_inv_transform(const device_patches<double>& i_patches, Rows i_Y,
											   Cols i_X, bool i_embed, bool i_transposed);
/*!
 * \overload
 */
device_patches<vec3<float>> log_polar_inv_transform(const device_patches<vec3<float>>& i_patches,
													Rows i_Y, Cols i_X, bool i_embed,
													bool i_transposed);
/*!
 * \overload
 */
device_patches<vec3<double>> log_polar_inv_transform(const device_patches<vec3<double>>& i_patches,
													 Rows i_Y, Cols i_X, bool i_embed,
													 bool i_transposed);