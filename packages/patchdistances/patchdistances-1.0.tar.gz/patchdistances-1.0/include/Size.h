/*! \file Size.h
	\brief A type safe class for a 2-dimensional size
	\sa Rows.h, Cols.h, device_matrix.h, device_patches.h
*/

#pragma once

#include "Cols.h"
#include "Rows.h"

#include <cstddef>

#ifdef __CUDACC__
#define CUDA_HOSTDEV __host__ __device__
#else
#define CUDA_HOSTDEV
#endif

/*!
 * \def CUDA_HOSTDEV
 * \__host__ \__device__ specifier if CUDA is present.
 */

//! A type safe class for a 2-dimensional size.
class Size final
{
  public:
	//! Default onstructor.
	Size() = default;

	//! Constructor.
	explicit Size(Rows i_rows, Cols i_cols) noexcept
		: m_rows{i_rows.value()}, m_cols{i_cols.value()}
	{
	}

	//! Returns row value.
	CUDA_HOSTDEV std::size_t rows() const noexcept
	{
		return m_rows;
	}

	//! Returns row value reference.
	CUDA_HOSTDEV std::size_t& rows() noexcept
	{
		return m_rows;
	}

	//! Returns column value.
	CUDA_HOSTDEV std::size_t cols() const noexcept
	{
		return m_cols;
	}

	//! Returns column value reference.
	CUDA_HOSTDEV std::size_t& cols() noexcept
	{
		return m_cols;
	}

	//! Returns total number of elements; rows*columns.
	CUDA_HOSTDEV std::size_t total() const noexcept
	{
		return m_rows * m_cols;
	}

  private:
	std::size_t m_rows{};
	std::size_t m_cols{};
};

//! Equal operator for Size class.
/*!
 * \return True if both rows and columns are equal, otherwise false.
 */
inline bool operator==(const Size& lhs, const Size& rhs)
{
	return lhs.cols() == rhs.cols() && lhs.rows() == rhs.rows();
}

//! "Not Equal" operator for Size class.
/*!
 * \return True if either rows or columns are different, otherwise false.
 */
inline bool operator!=(const Size& lhs, const Size& rhs)
{
	return !(lhs == rhs);
}