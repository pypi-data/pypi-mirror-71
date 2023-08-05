/*! \file extract_patches.h
	\brief Utilities to extract patches from an image.
*/

#pragma once

template<typename T>
class device_matrix;

template<typename T>
class device_patches;

template<typename T>
class vec3;

class Rows;
class Cols;

//! A function that extracts all patches from an image.
/*
 * \param i_image The input image.
 * \param i_patch_rows Row count of the extracted patches.
 * \param i_patch_cols Column count of the extracted patches.
 * \return Matrix with one patch per row. Patches are are stored in column-major format.
 */
device_patches<float> extract_patches(const device_matrix<float>& i_image, Rows i_patch_rows,
									  Cols i_patch_cols);

/*!
 * \overload
 */
device_patches<float> extract_patches(const device_matrix<float>& i_image,
									  const Size& i_patch_size);

/*!
 * \overload
 */
device_patches<double> extract_patches(const device_matrix<double>& i_image, Rows i_patch_rows,
									   Cols i_patch_cols);

/*!
 * \overload
 */
device_patches<double> extract_patches(const device_matrix<double>& i_image,
									   const Size& i_patch_size);

/*!
 * \overload
 */
device_patches<vec3<float>> extract_patches(const device_matrix<vec3<float>>& i_image,
											Rows i_patch_rows, Cols i_patch_cols);

/*!
 * \overload
 */
device_patches<vec3<float>> extract_patches(const device_matrix<vec3<float>>& i_image,
											const Size& i_patch_size);

/*!
 * \overload
 */
device_patches<vec3<double>> extract_patches(const device_matrix<vec3<double>>& i_image,
											 Rows i_patch_rows, Cols i_patch_cols);

/*!
 * \overload
 */
device_patches<vec3<double>> extract_patches(const device_matrix<vec3<double>>& i_image,
											 const Size& i_patch_size);