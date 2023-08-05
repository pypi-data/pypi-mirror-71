/*! \file quickselect.h
	\brief Quickselect algorithm for computing the median.
	\sa partition_NA.h
*/

#pragma once

#include "partition_NA.h"
#include "vec3.h"

#include <type_traits>

#ifdef __CUDACC__
#include <thrust/swap.h>
#define CUDA_HOSTDEV __host__ __device__
#else
#include <utility>
#define CUDA_HOSTDEV
#endif

/*!
 * \def CUDA_HOSTDEV
 * \__host__ \__device__ specifier if CUDA is present.
 */

//! Implemenation details.
namespace impl
{
//! Channel 1 of an array.
using ch1 = std::integral_constant<size_t, 1>;
//! Channel 2 of an array.
using ch2 = std::integral_constant<size_t, 2>;
//! Channel 3 of an array.
using ch3 = std::integral_constant<size_t, 3>;

//! Returns the selected channel of an array, i.e., the input.
template<typename C>
constexpr CUDA_HOSTDEV float& get_ch(float& val) noexcept
{
	return val;
};

//! Returns the selected channel of an array, i.e., the input.
template<typename C>
constexpr CUDA_HOSTDEV double& get_ch(double& val) noexcept
{
	return val;
};

//! Returns the selected channel of an array. Default is the first one.
template<typename C>
constexpr CUDA_HOSTDEV float& get_ch(vec3<float>& val) noexcept
{
	return val._1;
};

//! Returns the selected channel of an array, i.e., the first one.
template<>
constexpr CUDA_HOSTDEV float& get_ch<ch1>(vec3<float>& val) noexcept
{
	return val._1;
};

//! Returns the selected channel of an array, i.e., the second one.
template<>
constexpr CUDA_HOSTDEV float& get_ch<ch2>(vec3<float>& val) noexcept
{
	return val._2;
};

//! Returns the selected channel of an array, i.e., the third one.
template<>
constexpr CUDA_HOSTDEV float& get_ch<ch3>(vec3<float>& val) noexcept
{
	return val._3;
};

//! Returns the selected channel of an array.
template<typename C>
constexpr CUDA_HOSTDEV double& get_ch(vec3<double>& val) noexcept
{
	return val._1;
};

//! Returns the selected channel of an array, i.e., the first one.
template<>
constexpr CUDA_HOSTDEV double& get_ch<ch1>(vec3<double>& val) noexcept
{
	return val._1;
};

//! Returns the selected channel of an array, i.e., the second one.
template<>
constexpr CUDA_HOSTDEV double& get_ch<ch2>(vec3<double>& val) noexcept
{
	return val._2;
};

//! Returns the selected channel of an array, i.e., the third one.
template<>
constexpr CUDA_HOSTDEV double& get_ch<ch3>(vec3<double>& val) noexcept
{
	return val._3;
};

//! Quickselect function that computes the k-th (sorted) element of an unsorted array w/o recursion.
/*!
 * Elements of type NA will not(!) be ignored. Complexity: O(n).
 * \param i_array Unsorted array. It will be used as a buffer and overwritten!
 * \param i_size Number of elements of i_array.
 * \param i_k The k-th element of the sorted array.
 * \return The k-th element of the sorted array.
 * \tparam FloatVec Float or vec3<> of float.
 * \tparam Float Output float type.
 * \tparam C If FloatVec is vec3<>, this selects the channel.
 */
template<typename FloatVec, typename Float = FloatVec, typename C = void>
CUDA_HOSTDEV Float quickselect_impl(FloatVec* i_array, int i_size, int i_k) noexcept
{
#ifdef __CUDACC__
	using namespace thrust;
#else
	using namespace std;
#endif

	if(i_size == 0 || i_size < i_k)
	{
		return Float{details::NA};
	}

	auto from = 0;
	auto to = i_size - 1;

	// If from == to we reached the k-th element.
	while(from < to)
	{
		auto r = from;
		auto w = to;
		const auto mid = get_ch<C>(i_array[(r + w) / 2]);

		// Stop if the reader and writer meets.
		while(r < w)
		{
			if(get_ch<C>(i_array[r]) >= mid)
			{
				// put the large values at the end
				swap(get_ch<C>(i_array[w]), get_ch<C>(i_array[r]));
				w -= 1;
			}
			else
			{
				// the value is smaller than the pivot, skip
				r += 1;
			}
		}

		// If we stepped up (r++), we need to step one down.
		if(get_ch<C>(i_array[r]) > mid)
		{
			r -= 1;
		}

		// The r pointer is at the end of the first k elements.
		if(i_k <= r)
		{
			to = r;
		}
		else
		{
			from = r + 1;
		}
	}

	return get_ch<C>(i_array[i_k]);
}
} // namespace impl

//! Quickselect function that computes the k-th (sorted) element of an unsorted array w/o recursion.
/*!
 * Elements of type NA will not(!) be ignored. Complexity: O(n).
 * \param i_array Unsorted array. It will be used as a buffer and overwritten!
 * \param i_size Number of elements of i_array.
 * \param i_k The k-th element of the sorted array.
 * \return The k-th element of the sorted array.
 */
inline CUDA_HOSTDEV float quickselect(float* i_array, int i_size, int i_k) noexcept
{
	return impl::quickselect_impl(i_array, i_size, i_k);
}

/*!
 * \overload
 */
inline CUDA_HOSTDEV double quickselect(double* i_array, int i_size, int i_k) noexcept
{
	return impl::quickselect_impl(i_array, i_size, i_k);
}

/*!
 * \overload
 */
inline CUDA_HOSTDEV vec3<float> quickselect(vec3<float>* i_array, int i_size, int i_k) noexcept
{
	const auto med1 = impl::quickselect_impl<vec3<float>, float, impl::ch1>(i_array, i_size, i_k);
	const auto med2 = impl::quickselect_impl<vec3<float>, float, impl::ch2>(i_array, i_size, i_k);
	const auto med3 = impl::quickselect_impl<vec3<float>, float, impl::ch3>(i_array, i_size, i_k);

	return vec3<float>{med1, med2, med3};
}

/*!
 * \overload
 */
inline CUDA_HOSTDEV vec3<double> quickselect(vec3<double>* i_array, int i_size, int i_k) noexcept
{
	const auto med1 = impl::quickselect_impl<vec3<double>, double, impl::ch1>(i_array, i_size, i_k);
	const auto med2 = impl::quickselect_impl<vec3<double>, double, impl::ch2>(i_array, i_size, i_k);
	const auto med3 = impl::quickselect_impl<vec3<double>, double, impl::ch3>(i_array, i_size, i_k);

	return vec3<double>{med1, med2, med3};
}