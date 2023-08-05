/*! \file Rows.h
	\brief A type safe class for rows
	\sa device_matrix.h, device_patches.h
*/

#pragma once

#include "../extern/gsl/gsl_util"

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

//! A type safe class for rows.
class Rows final
{
  public:
	//! Default onstructor.
	Rows() = default;

	//! Constructor.
	explicit Rows(unsigned long i_rows) noexcept : m_rows{i_rows} {}
	//! Constructor.
	explicit Rows(unsigned int i_rows) noexcept : m_rows{i_rows} {}
	//! Constructor.
	explicit Rows(unsigned long long i_rows) : m_rows{gsl::narrow<std::size_t>(i_rows)} {}
	//! Constructor.
	explicit Rows(int i_rows) : m_rows{gsl::narrow<std::size_t>(i_rows)} {}

	//! Returns row value.
	CUDA_HOSTDEV std::size_t value() const noexcept
	{
		return m_rows;
	}

	//! Returns row value reference.
	CUDA_HOSTDEV std::size_t& value() noexcept
	{
		return m_rows;
	}

  private:
	std::size_t m_rows{};
};

//! Literal operator for Rows class.
inline Rows operator"" _rows(unsigned long long n)
{
	return Rows{n};
}