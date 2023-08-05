/*! \file Cols.h
	\brief A type safe class for columns
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

//! A type safe class for columns.
class Cols final
{
  public:
	//! Default onstructor.
	Cols() = default;

	//! Constructor.
	explicit Cols(unsigned long i_cols) noexcept : m_cols{i_cols} {}
	//! Constructor.
	explicit Cols(unsigned int i_cols) noexcept : m_cols{i_cols} {}
	//! Constructor.
	explicit Cols(unsigned long long i_cols) : m_cols{gsl::narrow<std::size_t>(i_cols)} {}
	//! Constructor.
	explicit Cols(int i_cols) : m_cols{gsl::narrow<std::size_t>(i_cols)} {}

	//! Returns column value.
	CUDA_HOSTDEV std::size_t value() const noexcept
	{
		return m_cols;
	}

	//! Returns column value reference.
	CUDA_HOSTDEV std::size_t& value() noexcept
	{
		return m_cols;
	}

  private:
	std::size_t m_cols{};
};

//! Literal operator for Col class.
inline Cols operator"" _cols(unsigned long long n)
{
	return Cols{n};
}