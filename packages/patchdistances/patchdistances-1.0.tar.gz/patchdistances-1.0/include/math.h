#pragma once

#include "vec3.h"

#ifdef __CUDACC__
#define CUDA_HOSTDEV __host__ __device__
#else
#define CUDA_HOSTDEV
#endif

#ifdef __CUDACC__
#include <thrust/complex.h>

using namespace thrust;
using t_complex = complex<float>;
using t_complex_dbl = complex<double>;

/*
 **
 *** Absolute square
 **
 */

inline CUDA_HOSTDEV float abs_square(const t_complex& val) noexcept
{
	return abs(val) * abs(val);
}

inline CUDA_HOSTDEV double abs_square(const t_complex_dbl& val) noexcept
{
	return abs(val) * abs(val);
}

inline CUDA_HOSTDEV float abs_square(const vec3<t_complex>& val) noexcept
{
	const auto val1 = abs(val._1);
	const auto val2 = abs(val._2);
	const auto val3 = abs(val._3);

	return val1 * val1 + val2 * val2 + val2 * val3;
}

inline CUDA_HOSTDEV double abs_square(const vec3<t_complex_dbl>& val) noexcept
{
	const auto val1 = abs(val._1);
	const auto val2 = abs(val._2);
	const auto val3 = abs(val._3);

	return val1 * val1 + val2 * val2 + val2 * val3;
}

/*
 **
 *** Mean
 **
 */

inline CUDA_HOSTDEV t_complex mean(const t_complex& val)
{
	return val;
}

inline CUDA_HOSTDEV t_complex_dbl mean(const t_complex_dbl& val)
{
	return val;
}

inline CUDA_HOSTDEV t_complex mean(vec3<t_complex> val)
{
	return (val._1 + val._2 + val._3) / 3;
}

inline CUDA_HOSTDEV t_complex_dbl mean(vec3<t_complex_dbl> val)
{
	return (val._1 + val._2 + val._3) / 3;
}
#endif // __CUDACC__

/*
 **
 *** Squared norm
 **
 */

//! Squared norm.
template<typename Float>
struct squared_norm final
{
	CUDA_HOSTDEV Float operator()(const Float& lhs, const Float& rhs) const
	{
		return lhs * lhs - rhs * rhs;
	}
};

/*
 **
 *** Multiplication
 **
 */

//! Multiplication with a scalar.
template<typename Float>
struct mul final
{
	explicit mul(Float scalar) : m_scalar{std::move(scalar)} {}

	CUDA_HOSTDEV Float operator()(const Float& val) const
	{
		return m_scalar * val;
	}

  private:
	Float m_scalar;
};

/*
 **
 *** Division
 **
 */

//! Division.
template<typename FloatVec>
struct divi final
{
	explicit divi(FloatVec val) noexcept : m{val} {}
	CUDA_HOSTDEV void operator()(FloatVec& in) const noexcept
	{
		in = in / m;
	}

  private:
	FloatVec m;
};

/*
 **
 *** Function families
 **
 */

/*
 **
 *** Superlevel sets
 **
 */

//! Superlevel sets.
struct superlevelsets final
{
	/*! A static member computing if a value lies in a superlevelset.
	 * \param x Input value in [0,1].
	 * \param i Index of the level.
	 * \param max Number of levels.
	 * \return 1 if x is in the superlevelset, 0 otherwise.
	 */
	template<typename T>
	CUDA_HOSTDEV static T compute(const T& x, unsigned int i, unsigned int max)
	{
		const auto level = static_cast<T>(i) / static_cast<T>(max);
		return x > level ? 1.0f : 0.0f;
	}

	/*!
	 * \overload
	 */
	template<typename T>
	CUDA_HOSTDEV static vec3<T> compute(const vec3<T>& x, unsigned int i, unsigned int max)
	{
		const auto level = static_cast<T>(i) / static_cast<T>(max);
		const auto val1 = x._1 > level ? 1.0f : 0.0f;
		const auto val2 = x._2 > level ? 1.0f : 0.0f;
		const auto val3 = x._3 > level ? 1.0f : 0.0f;

		return vec3<T>{val1, val2, val3};
	}
};

/*
 **
 *** Clip function
 **
 */

//! Clipping to [min,max].
struct clip final
{
	/*! A static member clipping a value.
	 * \param x Input value in [0,1].
	 * \param i Current iteration.
	 * \param max Total number of iterations.
	 * \return min(x, i/max).
	 */
	template<typename T>
	CUDA_HOSTDEV static T compute(T x, unsigned int i, unsigned int max)
	{
		const auto upper = static_cast<T>(i + 1) / static_cast<T>(max);

		return min(x, upper);
	}

	/*!
	 * \overload
	 */
	template<typename T>
	CUDA_HOSTDEV static vec3<T> compute(const vec3<T>& x, unsigned int i, unsigned int max)
	{
		const auto upper = static_cast<T>(i + 1) / static_cast<T>(max);
		const auto val1 = min(x._1, upper);
		const auto val2 = min(x._2, upper);
		const auto val3 = min(x._3, upper);

		return vec3<T>{val1, val2, val3};
	}
};