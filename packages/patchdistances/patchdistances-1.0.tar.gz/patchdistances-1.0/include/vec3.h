/*! \file vec3.h
	\brief Vector class of size 3
*/

#pragma once

#include "../extern/gsl/gsl_assert"
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

//! A template struct for a vector of size 3 with "element-wise" multiplication and division.
template<typename T>
struct alignas(alignof(T)) vec3 final
{
	//! Default onstructor.
	explicit CUDA_HOSTDEV vec3() noexcept
	{
		// An array of vec3<T> can be safely cast to an array of T.
		static_assert(sizeof(vec3<T>) == 3 * sizeof(T), "The struct has unexpected padding.");
	}

	//! Constructor.
	explicit CUDA_HOSTDEV vec3(T val) noexcept : _1{val}, _2{val}, _3{val}
	{
		// An array of vec3<T> can be safely cast to an array of T.
		static_assert(sizeof(vec3<T>) == 3 * sizeof(T), "The struct has unexpected padding.");
	}

	//! Constructor.
	explicit CUDA_HOSTDEV vec3(T i_1, T i_2, T i_3) noexcept
		: _1{std::move(i_1)}, _2{std::move(i_2)}, _3{std::move(i_3)}
	{
		// An array of vec3<T> can be safely cast to an array of T.
		static_assert(sizeof(vec3<T>) == 3 * sizeof(T), "The struct has unexpected padding.");
	}

	T _1{}; /**< First element. */
	T _2{}; /**< Second element. */
	T _3{}; /**< Third element. */

	//! Equality comparison; True if all elements are equal.
	friend CUDA_HOSTDEV bool operator==(const vec3<T>& lhs, const vec3<T>& rhs) noexcept
	{
		return lhs._1 == rhs._1 && lhs._2 == rhs._2 && lhs._3 == rhs._3;
	}

	//! Inequality comparison; True if one element is different.
	friend CUDA_HOSTDEV bool operator!=(const vec3<T>& lhs, const vec3<T>& rhs) noexcept
	{
		return !(lhs == rhs);
	}

	//! Element-wise addition.
	CUDA_HOSTDEV vec3<T>& operator+=(const vec3<T>& n) noexcept
	{
		_1 += n._1;
		_2 += n._2;
		_3 += n._3;

		return *this;
	}

	//! Element-wise subtraction.
	CUDA_HOSTDEV vec3<T>& operator-=(const vec3<T>& n) noexcept
	{
		_1 -= n._1;
		_2 -= n._2;
		_3 -= n._3;

		return *this;
	}

	//! Element-wise multiplication with a constant.
	CUDA_HOSTDEV vec3<T>& operator*=(T n) noexcept
	{
		_1 *= n;
		_2 *= n;
		_3 *= n;

		return *this;
	}

	//! Element-wise multiplication.
	CUDA_HOSTDEV vec3<T>& operator*=(const vec3<T>& n) noexcept
	{
		_1 *= n._1;
		_2 *= n._2;
		_3 *= n._3;

		return *this;
	}

	//! Element-wise division by a constant.
	CUDA_HOSTDEV vec3<T>& operator/=(T n) noexcept
	{
		_1 /= n;
		_2 /= n;
		_3 /= n;

		return *this;
	}

	//! Element-wise division.
	CUDA_HOSTDEV vec3<T>& operator/=(const vec3<T>& n) noexcept
	{
		_1 /= n._1;
		_2 /= n._2;
		_3 /= n._3;

		return *this;
	}

	//! Element-wise subtraction.
	CUDA_HOSTDEV vec3<T>& operator-() noexcept
	{
		_1 = -_1;
		_2 = -_2;
		_3 = -_3;

		return *this;
	}

	//! Element-wise addition.
	friend CUDA_HOSTDEV vec3<T> operator+(vec3<T> lhs, const vec3<T>& rhs) noexcept
	{
		lhs += rhs;
		return lhs;
	}

	//! Element-wise subtraction.
	friend CUDA_HOSTDEV vec3<T> operator-(vec3<T> lhs, const vec3<T>& rhs) noexcept
	{
		lhs -= rhs;
		return lhs;
	}

	//! Element-wise multiplication with a constant.
	friend CUDA_HOSTDEV vec3<T> operator*(vec3<T> lhs, T rhs) noexcept
	{
		lhs *= rhs;
		return lhs;
	}

	//! Element-wise multiplication with a constant.
	friend CUDA_HOSTDEV vec3<T> operator*(T lhs, vec3<T> rhs) noexcept
	{
		rhs *= lhs;
		return rhs;
	}

	//! Element-wise multiplication.
	friend CUDA_HOSTDEV vec3<T> operator*(vec3<T> lhs, const vec3<T>& rhs) noexcept
	{
		lhs *= rhs;
		return lhs;
	}

	//! Element-wise division by a constant.
	friend CUDA_HOSTDEV vec3<T> operator/(vec3<T> lhs, T rhs) noexcept
	{
		lhs /= rhs;
		return lhs;
	}

	//! Element-wise division by a constant.
	friend CUDA_HOSTDEV vec3<T> operator/(vec3<T> lhs, const vec3<T>& rhs) noexcept
	{
		lhs /= rhs;
		return lhs;
	}
};