/*! \file patch_index.h
	\brief A type safe class indexing patches
	\sa device_patches.h
*/
#pragma once

#include "../extern/gsl/gsl_util"

#include <cstddef>

//! A type safe class for a patch index.
class patch_index final
{
  public:
	//! Default onstructor.
	constexpr patch_index() = default;

	//! Constructor.
	constexpr explicit patch_index(unsigned int i_index) : m_index{i_index} {}
	//! Constructor.
	constexpr explicit patch_index(unsigned long i_index) noexcept : m_index{i_index} {}
	//! Constructor.
	explicit patch_index(int i_index) : m_index{gsl::narrow<std::size_t>(i_index)} {}
	//! Constructor.
	explicit patch_index(std::ptrdiff_t i_index) : m_index{gsl::narrow<std::size_t>(i_index)} {}
	//! Constructor.
	explicit patch_index(unsigned long long i_index) : m_index{gsl::narrow<std::size_t>(i_index)} {}

	//! Returns patch index.
	__host__ __device__ constexpr std::size_t value() const noexcept
	{
		return m_index;
	}

	//! Returns patch index reference.
	__host__ __device__ constexpr std::size_t& value() noexcept
	{
		return m_index;
	}

  private:
	std::size_t m_index{};
};

//! Literal operator for patch_index class.
inline patch_index operator"" _patches(unsigned long long p)
{
	return patch_index{p};
}