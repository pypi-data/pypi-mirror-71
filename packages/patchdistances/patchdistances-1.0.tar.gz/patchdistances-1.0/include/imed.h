/*! \file imed.h
	\brief Utilities to compute the Image Euclidean distance for patches.
*/

template<typename T>
class device_patches;

template<typename T>
struct vec3;

//! Function that computes the Convolution Standardized Transform (CFT) of patches.
/*!
 * \param i_patches Patches that will be convolved.
 * \return Convolved patches.
 */
device_patches<float> imed_cft(const device_patches<float>& i_patches);

/*!
 * \overload
 */
device_patches<double> imed_cft(const device_patches<double>& i_patches);

/*!
 * \overload
 */
device_patches<vec3<float>> imed_cft(const device_patches<vec3<float>>& i_patches);

/*!
 * \overload
 */
device_patches<vec3<double>> imed_cft(const device_patches<vec3<double>>& i_patches);