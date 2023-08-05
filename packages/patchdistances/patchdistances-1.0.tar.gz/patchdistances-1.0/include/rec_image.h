/*! \file rec_image.h
	\brief Reconstructing images using patches.
	\sa rec_t
*/

#pragma once

template<typename T>
class device_matrix;

template<typename T>
class device_patches;

template<typename T>
class vec3;

class Size;

enum class rec_t;

//! A function that reconstructs an image based on patches assigned to each pixel.
//! It is assumed that patches with full support are used!
/*!
 * \param i_labels_idx The assigned label for each pixel.
 * \param i_labels The prototypical labels.
 * \param i_type Method to reconstruct a pixel value from a set of projected values.
 * \return Reconstructed image of original size (i_labels_idx + size of labels - 1).
 */
device_matrix<float> rec_image(const device_matrix<size_t>& i_labels_idx,
							   const device_patches<float>& i_labels, rec_t i_type);

/*!
 * \overload
 */
device_matrix<double> rec_image(const device_matrix<size_t>& i_labels_idx,
								const device_patches<double>& i_labels, rec_t i_type);

/*!
 * \overload
 */
device_matrix<vec3<float>> rec_image(const device_matrix<size_t>& i_labels_idx,
									 const device_patches<vec3<float>>& i_labels, rec_t i_type);

/*!
 * \overload
 */
device_matrix<vec3<double>> rec_image(const device_matrix<size_t>& i_labels_idx,
									  const device_patches<vec3<double>>& i_labels, rec_t i_type);

//! A function that reconstructs an image based on patches (with full support) for each pixel.
/*!
 * This function is intended for internal use.
 * \param i_labels The extracted patches with full support.
 * \param i_img_size Size of the original image.
 * \param i_type Method to reconstruct a pixel value from a set of projected values.
 * \return Reconstructed image.
 */
device_matrix<float> rec_image(const device_patches<float>& i_labels, const Size& i_img_size,
							   rec_t i_type);

/*!
 * \overload
 */
device_matrix<double> rec_image(const device_patches<double>& i_labels, const Size& i_img_size,
								rec_t i_type);

/*!
 * \overload
 */
device_matrix<vec3<float>> rec_image(const device_patches<vec3<float>>& i_labels,
									 const Size& i_img_size, rec_t i_type);

/*!
 * \overload
 */
device_matrix<vec3<double>> rec_image(const device_patches<vec3<double>>& i_labels,
									  const Size& i_img_size, rec_t i_type);