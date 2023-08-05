/*! \file warp_perspective.h
	\brief Perspective transformation for patches.
*/

#include "Size.h"

enum class interpolation_t;

template<typename T>
class device_matrix;

template<typename T>
class device_patches;

//! Takes an affine transformation and returns the perspective transformation, which can be
//! used with warp_perspective(). This includes scaling to a given image dimension. The projective
//! matrix will be rounded to 2 decimal places to avoid transformation artifacts. If this results is
//! the 0 matrix, the identity will be used instead.
/*!
 * \param a11 A_11
 * \param a12 A_12
 * \param b1  A_13 = b1; Offset in x-direction.
 * \param a21 A_21
 * \param a22 A_22
 * \param b2 A_23 = b2; Offset in y-direction.
 * \param img_size Image size needed for scaling the transformation.
 * \param mat Row major output array of size 3x3.
 */
inline __host__ __device__ void perspective_matrix(float a11, float a12, float b1, float a21,
												   float a22, float b2, const Size& img_size,
												   float* mat)
{
	constexpr auto prec = 100;
	const auto rows = static_cast<float>(img_size.rows());
	const auto cols = static_cast<float>(img_size.cols());

	const auto a11_ = rintf(a11 * prec) / prec;
	const auto a12_ = rintf(a12 * prec) / prec;
	const auto a21_ = rintf(a21 * prec) / prec;
	const auto a22_ = rintf(a22 * prec) / prec;
	const auto b1_ = rintf(0.5f * (cols - 1) * (b1 + 1 - a11_ - a12_) * prec) / prec;
	const auto b2_ = rintf(0.5f * (rows - 1) * (b2 + 1 - a21_ - a22_) * prec) / prec;

	if(a11_ * a22_ - a12_ * a21_ != 0)
	{
		mat[0] = a11_;
		mat[1] = a12_;
		mat[2] = b1_;
		mat[3] = a21_;
		mat[4] = a22_;
		mat[5] = b2_;
		mat[6] = 0.0f;
		mat[7] = 0.0f;
		mat[8] = 1.0f;
	}
	else // identity
	{
		mat[0] = 1.0f;
		mat[1] = 0.0f;
		mat[2] = 0.0f;
		mat[3] = 0.0f;
		mat[4] = 1.0f;
		mat[5] = 0.0f;
		mat[6] = 0.0f;
		mat[7] = 0.0f;
		mat[8] = 1.0f;
	}
}

//! Perspective transformation for patches ("pull"/ "backward" resampling).
/*!
 * \param i_patches Patches.
 * \param i_transforms Perspective transformations of size 3x3 with row major memory layout. Since
 * this function performs pull resampling, inverse transformations need to be suplied.
 * \param i_type Interpolation type.
 * \return Perspective transformation of i_patches[i] and i_transforms[i], for each patch i.
 */
device_patches<float> warp_perspective(const device_patches<float>& i_patches,
									   const device_patches<float>& i_transforms,
									   interpolation_t i_type);

/*!
 * \overload
 */
device_patches<double> warp_perspective(const device_patches<double>& i_patches,
										const device_patches<float>& i_transforms,
										interpolation_t i_type);

/*!
 * \overload
 */
device_patches<vec3<float>> warp_perspective(const device_patches<vec3<float>>& i_patches,
											 const device_patches<float>& i_transforms,
											 interpolation_t i_type);

/*!
 * \overload
 */
device_patches<vec3<double>> warp_perspective(const device_patches<vec3<double>>& i_patches,
											  const device_patches<float>& i_transforms,
											  interpolation_t i_type);

//! Perspective transformation for patches ("pull"/ "backward" resampling).
/*!
 * \param i_matrix Matrix.
 * \param i_transforms Perspective transformations of size 3x3 with row major memory layout. Since
 * this function performs pull resampling, inverse transformations need to be suplied.
 * \param i_type Interpolation type.
 * \return Perspective transformation of i_matrix and i_transforms[i], for each patch i.
 */
device_patches<float> warp_perspective(const device_matrix<float>& i_matrix,
									   const device_patches<float>& i_transforms,
									   interpolation_t i_type);

/*!
 * \overload
 */
device_patches<double> warp_perspective(const device_matrix<double>& i_matrix,
										const device_patches<float>& i_transforms,
										interpolation_t i_type);

/*!
 * \overload
 */
device_patches<vec3<float>> warp_perspective(const device_matrix<vec3<float>>& i_patches,
											 const device_patches<float>& i_transforms,
											 interpolation_t i_type);

/*!
 * \overload
 */
device_patches<vec3<double>> warp_perspective(const device_matrix<vec3<double>>& i_patches,
											  const device_patches<float>& i_transforms,
											  interpolation_t i_type);