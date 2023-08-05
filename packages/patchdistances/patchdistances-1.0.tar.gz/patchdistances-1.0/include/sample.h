/*! \file sample.h
	\brief Sampling image pixels for interpolation
	\sa warp_perspecitve.h, log_polar_transform.h
*/

#pragma once

#include "Size.h"
#include "enums.h"

#include <algorithm>
#include <cuda_runtime.h>

#include <cstddef>

//! Implementation details.
namespace impl
{
//! Cubic convolution at position 0 <= t <= 1 (with parameter a=-0.5).
/*!
 * \param A (f-1) Used to compute left-hand slope.
 * \param B (f0) If t=0, B is returned.
 * \param C (f1) If t=1, C is returned.
 * \param D (f2) Used to compute right-hand slope.
 * \param t Value that goes from 0 to 1 to interpolate in a C1 continuous way across uniformly
 * sampled data points.
 * \tparam FloatVec Floating point or vec3<> of floating point.
 * \return Interpolated point.
 */
template<typename FloatVec>
constexpr __host__ __device__ FloatVec cubic_conv(FloatVec A, FloatVec B, FloatVec C, FloatVec D,
												  float t)
{
	const auto a = -0.5f * A + 1.5f * B - 1.5f * C + 0.5f * D;
	const auto b = A - 2.5f * B + 2.0f * C - 0.5f * D;
	const auto c = -0.5f * A + 0.5f * C;
	const auto d = B;

	return FloatVec{a * t * t * t + b * t * t + c * t + d};
}

//! Returns pixel value for a given position. For positions 1px outside the grid, an interpolated
//! value is returned, which is based on the cubic interpolation algorithm. Otherwise 0 is returned.
/*!
 * \param data Continuous image data of size rows*cols in column major layout.
 * \param x X position.
 * \param y Y position.
 * \param rows Rows of data.
 * \param cols Columns of data.
 * \tparam FloatVec Floating point or vec3<> of floating point.
 * \return Pixel at position (x,y).
 */
template<typename FloatVec>
constexpr __host__ __device__ FloatVec get_px_col_maj(const FloatVec* data, int x, int y, int rows,
													  int cols)
{
	if(x >= 0 && x < cols)
	{
		if(y >= 0 && y < rows) // standard case
		{
			return data[y + x * rows];
		}
		else if(y == -1)
		{
			const auto i = x * rows;
			return 3 * data[i] - 3 * data[i + 1] + data[i + 2];
		}
		else if(y == rows)
		{
			const auto i = y - 1 + x * rows;
			return 3 * data[i] - 3 * data[i - 1] + data[i - 2];
		}
	}
	else if(x == -1)
	{
		if(y >= 0 && y < rows)
		{
			return 3 * data[y] - 3 * data[y + rows] + data[y + 2 * rows];
		}
		else if(y == -1)
		{
			const auto c0 = 3 * data[0] - 3 * data[1] + data[2];
			const auto c1 = 3 * data[rows] - 3 * data[1 + rows] + data[2 + rows];
			const auto c2 = 3 * data[2 * rows] - 3 * data[1 + 2 * rows] + data[2 + 2 * rows];
			return 3 * c0 - 3 * c1 + c2;
		}
		else if(y == rows)
		{
			const auto c0 = 3 * data[rows - 1] - 3 * data[rows - 2] + data[rows - 3];
			const auto c1 = 3 * data[2 * rows - 1] - 3 * data[2 * rows - 2] + data[2 * rows - 3];
			const auto c2 = 3 * data[3 * rows - 1] - 3 * data[3 * rows - 2] + data[3 * rows - 3];
			return 3 * c0 - 3 * c1 + c2;
		}
	}
	else if(x == cols)
	{
		if(y >= 0 && y < rows)
		{
			const auto i = y + (cols - 1) * rows;
			return 3 * data[i] - 3 * data[i - rows] + data[i - 2 * rows];
		}
		else if(y == -1)
		{
			const auto i = (cols - 1) * rows;
			const auto c0 = 3 * data[i] - 3 * data[i + 1] + data[i + 2];
			const auto c1 = 3 * data[i - rows] - 3 * data[i - rows + 1] + data[i - rows + 2];
			const auto c2 =
				3 * data[i - 2 * rows] - 3 * data[i - 2 * rows + 1] + data[i - 2 * rows + 2];
			return 3 * c0 - 3 * c1 + c2;
		}
		else if(y == rows)
		{
			const auto i = cols * rows - 1;
			const auto c0 = 3 * data[i] - 3 * data[i - 1] + data[i - 2];
			const auto c1 = 3 * data[i - rows] - 3 * data[i - rows - 1] + data[i - rows - 2];
			const auto c2 =
				3 * data[i - 2 * rows] - 3 * data[i - 2 * rows - 1] + data[i - 2 * rows - 2];
			return 3 * c0 - 3 * c1 + c2;
		}
	}

	// The point lies outside the grid and interpolation is not possible.
	return FloatVec{0};
}

//! Returns pixel value for a given position. For positions 1px outside the grid, an interpolated
//! value is returned, which is based on the cubic interpolation algorithm. Otherwise 0 is returned.
/*!
 * \param data Continuous image data of size rows*cols in row major layout.
 * \param x X position.
 * \param y Y position.
 * \param rows Rows of data.
 * \param cols Columns of data.
 * \tparam FloatVec Floating point or vec3<> of floating point.
 * \return Pixel at position (x,y).
 */
template<typename FloatVec>
constexpr __host__ __device__ FloatVec get_px_row_maj(const FloatVec* data, int x, int y, int rows,
													  int cols)
{
	if(x >= 0 && x < cols)
	{
		if(y >= 0 && y < rows) // standard case
		{
			return data[x + y * cols];
		}
		else if(y == -1)
		{
			return 3 * data[x] - 3 * data[x + cols] + data[x + 2 * cols];
		}
		else if(y == rows)
		{
			const auto i = x + (rows - 1) * cols;
			return 3 * data[i] - 3 * data[i - cols] + data[i - 2 * cols];
		}
	}
	else if(x == -1)
	{
		if(y >= 0 && y < rows)
		{
			return 3 * data[y * cols] - 3 * data[y * cols + 1] + data[y * cols + 2];
		}
		else if(y == -1)
		{
			const auto c0 = 3 * data[0] - 3 * data[1] + data[2];
			const auto c1 = 3 * data[cols] - 3 * data[1 + cols] + data[2 + cols];
			const auto c2 = 3 * data[2 * cols] - 3 * data[1 + 2 * cols] + data[2 + 2 * cols];
			return 3 * c0 - 3 * c1 + c2;
		}
		else if(y == rows)
		{
			const auto i = (rows - 1) * cols;
			const auto c0 = 3 * data[i] - 3 * data[i + 1] + data[i + 2];
			const auto c1 = 3 * data[i - cols] - 3 * data[i - cols + 1] + data[i - cols + 2];
			const auto c2 =
				3 * data[i - 2 * cols] - 3 * data[i - 2 * cols + 1] + data[i - 2 * cols + 2];
			return 3 * c0 - 3 * c1 + c2;
		}
	}
	else if(x == cols)
	{
		if(y >= 0 && y < rows)
		{
			const auto i = (y + 1) * cols - 1;
			return 3 * data[i] - 3 * data[i - 1] + data[i - 2];
		}
		else if(y == -1)
		{
			const auto c0 = 3 * data[cols - 1] - 3 * data[cols - 2] + data[cols - 3];
			const auto c1 = 3 * data[2 * cols - 1] - 3 * data[2 * cols - 2] + data[2 * cols - 3];
			const auto c2 = 3 * data[3 * cols - 1] - 3 * data[3 * cols - 2] + data[3 * cols - 3];
			return 3 * c0 - 3 * c1 + c2;
		}
		else if(y == rows)
		{
			const auto i = cols * rows - 1;
			const auto c0 = 3 * data[i] - 3 * data[i - 1] + data[i - 2];
			const auto c1 = 3 * data[i - cols] - 3 * data[i - cols - 1] + data[i - cols - 2];
			const auto c2 =
				3 * data[i - 2 * cols] - 3 * data[i - 2 * cols - 1] + data[i - 2 * cols - 2];
			return 3 * c0 - 3 * c1 + c2;
		}
	}

	// The point lies outside the grid and interpolation is not possible.
	return FloatVec{0};
}

//! Returns bicubic interpolated pixel value for given coordinates using the bicubic convolution
//! algorithm.
/*!
 * \param data Continuous image data of size rows*cols in column major layout.
 * The size has to be at least 3x3.
 * \param x X Coordinate of the sampled point in pixel of the sampled image starting on the left.
 * \param y Y Coordinate of the sampled point in pixel of the sampled image starting at the top.
 * \param rows Rows of data.
 * \param cols Columns of data.
 * \tparam FloatVec Floating point or vec3<> of floating point.
 * \return Bicubic interpolated pixel value.
 */
template<typename FloatVec>
constexpr __host__ __device__ FloatVec sample_bicubic_col_maj(const FloatVec* data, float x,
															  float y, int rows, int cols)
{
	const auto x_ = static_cast<int>(x); // static_cast: rounding down.
	const auto x_frac = x - static_cast<float>(x_);

	const auto y_ = static_cast<int>(y);
	const auto y_frac = y - static_cast<float>(y_);

	// 1st row
	const auto p00 = get_px_col_maj(data, x_ - 1, y_ - 1, rows, cols);
	const auto p10 = get_px_col_maj(data, x_ + 0, y_ - 1, rows, cols);
	const auto p20 = get_px_col_maj(data, x_ + 1, y_ - 1, rows, cols);
	const auto p30 = get_px_col_maj(data, x_ + 2, y_ - 1, rows, cols);

	// 2nd row
	const auto p01 = get_px_col_maj(data, x_ - 1, y_ + 0, rows, cols);
	const auto p11 = get_px_col_maj(data, x_ + 0, y_ + 0, rows, cols);
	const auto p21 = get_px_col_maj(data, x_ + 1, y_ + 0, rows, cols);
	const auto p31 = get_px_col_maj(data, x_ + 2, y_ + 0, rows, cols);

	// 3rd row
	const auto p02 = get_px_col_maj(data, x_ - 1, y_ + 1, rows, cols);
	const auto p12 = get_px_col_maj(data, x_ + 0, y_ + 1, rows, cols);
	const auto p22 = get_px_col_maj(data, x_ + 1, y_ + 1, rows, cols);
	const auto p32 = get_px_col_maj(data, x_ + 2, y_ + 1, rows, cols);

	// 4th row
	const auto p03 = get_px_col_maj(data, x_ - 1, y_ + 2, rows, cols);
	const auto p13 = get_px_col_maj(data, x_ + 0, y_ + 2, rows, cols);
	const auto p23 = get_px_col_maj(data, x_ + 1, y_ + 2, rows, cols);
	const auto p33 = get_px_col_maj(data, x_ + 2, y_ + 2, rows, cols);

	// interpolate bi-cubically
	const auto b_1 = cubic_conv(p00, p10, p20, p30, x_frac);
	const auto b0 = cubic_conv(p01, p11, p21, p31, x_frac);
	const auto b1 = cubic_conv(p02, p12, p22, p32, x_frac);
	const auto b2 = cubic_conv(p03, p13, p23, p33, x_frac);

	return cubic_conv(b_1, b0, b1, b2, y_frac);
}

//! Returns bicubic interpolated pixel value for given coordinates using the bicubic convolution
//! algorithm.
/*!
 * \param data Continuous image data of size rows*cols in row major layout.
 * The size has to be at least 3x3.
 * \param x X Coordinate of the sampled point in pixel of the sampled image starting on the left.
 * \param y Y Coordinate of the sampled point in pixel of the sampled image starting at the top.
 * \param rows Rows of data.
 * \param cols Columns of data.
 * \tparam FloatVec Floating point or vec3<> of floating point.
 * \return Bicubic interpolated pixel value.
 */
template<typename FloatVec>
constexpr __host__ __device__ FloatVec sample_bicubic_row_maj(const FloatVec* data, float x,
															  float y, int rows, int cols)
{
	const auto x_ = static_cast<int>(x); // static_cast: rounding down.
	const auto x_frac = x - static_cast<float>(x_);

	const auto y_ = static_cast<int>(y);
	const auto y_frac = y - static_cast<float>(y_);

	// 1st row
	const auto p00 = get_px_row_maj(data, x_ - 1, y_ - 1, rows, cols);
	const auto p10 = get_px_row_maj(data, x_ + 0, y_ - 1, rows, cols);
	const auto p20 = get_px_row_maj(data, x_ + 1, y_ - 1, rows, cols);
	const auto p30 = get_px_row_maj(data, x_ + 2, y_ - 1, rows, cols);

	// 2nd row
	const auto p01 = get_px_row_maj(data, x_ - 1, y_ + 0, rows, cols);
	const auto p11 = get_px_row_maj(data, x_ + 0, y_ + 0, rows, cols);
	const auto p21 = get_px_row_maj(data, x_ + 1, y_ + 0, rows, cols);
	const auto p31 = get_px_row_maj(data, x_ + 2, y_ + 0, rows, cols);

	// 3rd row
	const auto p02 = get_px_row_maj(data, x_ - 1, y_ + 1, rows, cols);
	const auto p12 = get_px_row_maj(data, x_ + 0, y_ + 1, rows, cols);
	const auto p22 = get_px_row_maj(data, x_ + 1, y_ + 1, rows, cols);
	const auto p32 = get_px_row_maj(data, x_ + 2, y_ + 1, rows, cols);

	// 4th row
	const auto p03 = get_px_row_maj(data, x_ - 1, y_ + 2, rows, cols);
	const auto p13 = get_px_row_maj(data, x_ + 0, y_ + 2, rows, cols);
	const auto p23 = get_px_row_maj(data, x_ + 1, y_ + 2, rows, cols);
	const auto p33 = get_px_row_maj(data, x_ + 2, y_ + 2, rows, cols);

	// interpolate bi-cubically
	const auto b_1 = cubic_conv(p00, p10, p20, p30, x_frac);
	const auto b0 = cubic_conv(p01, p11, p21, p31, x_frac);
	const auto b1 = cubic_conv(p02, p12, p22, p32, x_frac);
	const auto b2 = cubic_conv(p03, p13, p23, p33, x_frac);

	return cubic_conv(b_1, b0, b1, b2, y_frac);
}

//! Returns nearest neighbor interpolated pixel value for given coordinates.
/*!
 * \param data Continuous image data of size rows*cols in column major layout.
 * The size has to be at least 3x3.
 * \param x X Coordinate of the sampled point in pixel of the sampled image starting on the left.
 * \param y Y Coordinate of the sampled point in pixel of the sampled image starting at the top.
 * \param rows Rows of data.
 * \param cols Columns of data.
 * \tparam FloatVec Floating point or vec3<> of floating point.
 * \return Nearest neighbor interpolated pixel value.
 */
template<typename FloatVec>
__host__ __device__ FloatVec sample_nn_col_maj(const FloatVec* data, float x, float y, int rows,
											   int cols)
{
	const auto x_ = lrintf(x);
	const auto y_ = lrintf(y);

	if(x_ >= 0 && x_ < cols && y_ >= 0 && y_ < rows)
	{
		return data[y_ + x_ * rows];
	}
	else
	{
		return FloatVec{0.0};
	}
}

//! Returns nearest neighbor interpolated pixel value for given coordinates.
/*!
 * \param data Continuous image data of size rows*cols in row major layout.
 * The size has to be at least 3x3.
 * \param x X Coordinate of the sampled point in pixel of the sampled image starting on the left.
 * \param y Y Coordinate of the sampled point in pixel of the sampled image starting at the top.
 * \param rows Rows of data.
 * \param cols Columns of data.
 * \tparam FloatVec Floating point or vec3<> of floating point.
 * \return Nearest neighbor interpolated pixel value.
 */
template<typename FloatVec>
__host__ __device__ FloatVec sample_nn_row_maj(const FloatVec* data, float x, float y, int rows,
											   int cols)
{
	const auto x_ = lrintf(x);
	const auto y_ = lrintf(y);

	if(x_ >= 0 && x_ < cols && y_ >= 0 && y_ < rows)
	{
		return data[x_ + y_ * cols];
	}
	else
	{
		return FloatVec{0.0};
	}
}
} // namespace impl

//! Samples a pixel with a given interpolation method.
/*!
 * \param data Continuous image data of size rows*cols in column major layout.
 * For bicubic interpolation, the size has to be at least 3x3.
 * \param x X Coordinate of the sampled point in pixel of the sampled image starting on the left.
 * \param y Y Coordinate of the sampled point in pixel of the sampled image starting at the top.
 * \param rows Rows of data.
 * \param cols Columns of data.
 * \param col_maj If true column-major data layout of data is assumed. Otherwise row-major.
 * \param type Interpolation type.
 * \tparam FloatVec Floating point or vec3<> of floating point.
 * \return Interpolated pixel value.
 */
template<typename FloatVec>
__host__ __device__ FloatVec sample(const FloatVec* data, float x, float y, int rows, int cols,
									bool col_maj, interpolation_t type)
{
	if(type == interpolation_t::bicubic)
	{
		return col_maj ? impl::sample_bicubic_col_maj(data, x, y, rows, cols)
					   : impl::sample_bicubic_row_maj(data, x, y, rows, cols);
	}
	else
	{
		return col_maj ? impl::sample_nn_col_maj(data, x, y, rows, cols)
					   : impl::sample_nn_row_maj(data, x, y, rows, cols);
	}
}