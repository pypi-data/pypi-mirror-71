#pragma once

#include "vec3.h"

#ifdef __CUDACC__
#define CUDA_HOSTDEV __host__ __device__
#else
#define CUDA_HOSTDEV
#endif

//! Class that implements the Euclidean metric.
struct euclidean_metric final
{
	//! A static member that computes the Euclidean distance between two sets of points.
	/*!
	 * \param lhs First set of points.
	 * \param rhs Second set of points.
	 * \param i_length Number of input elements of lhs and rhs.
	 * \return The euclidean distance for the two input sets.
	 */
	CUDA_HOSTDEV static float compute(const float* lhs, const float* rhs,
									  unsigned int i_length) noexcept
	{
		auto result = float{};
		for(unsigned int i = 0; i < i_length; i++)
		{
			const auto x = lhs[i] - rhs[i];
			result += x * x;
		}

		return sqrtf(result);
	}

	/*!
	 * \overload
	 */
	CUDA_HOSTDEV static double compute(const double* lhs, const double* rhs,
									   unsigned int i_length) noexcept
	{
		auto result = double{};
		for(unsigned int i = 0; i < i_length; i++)
		{
			const auto x = lhs[i] - rhs[i];
			result += x * x;
		}

		return sqrt(result);
	}

	/*!
	 * \overload
	 */
	CUDA_HOSTDEV static float compute(const vec3<float>* lhs, const vec3<float>* rhs,
									  unsigned int i_length) noexcept
	{
		auto result = float{};
		for(unsigned int i = 0; i < i_length; i++)
		{
			const auto lhs_val = lhs[i];
			const auto rhs_val = rhs[i];

			const auto x = lhs_val._1 - rhs_val._1;
			const auto y = lhs_val._2 - rhs_val._2;
			const auto z = lhs_val._3 - rhs_val._3;

			result += x * x + y * y + z * z;
		}

		return sqrtf(result);
	}

	/*!
	 * \overload
	 */
	CUDA_HOSTDEV static double compute(const vec3<double>* lhs, const vec3<double>* rhs,
									   unsigned int i_length) noexcept
	{
		auto result = double{};
		for(unsigned int i = 0; i < i_length; i++)
		{
			const auto lhs_val = lhs[i];
			const auto rhs_val = rhs[i];

			const auto x = lhs_val._1 - rhs_val._1;
			const auto y = lhs_val._2 - rhs_val._2;
			const auto z = lhs_val._3 - rhs_val._3;

			result += x * x + y * y + z * z;
		}

		return sqrt(result);
	}
};