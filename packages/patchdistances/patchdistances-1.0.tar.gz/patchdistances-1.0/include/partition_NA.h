/*! \file partition_NA.h
	\brief Partitioning of NA values.
*/

#pragma once

#ifdef __CUDACC__
#define CUDA_HOSTDEV __host__ __device__
#else
#define CUDA_HOSTDEV
#endif

//! Implementation details.
namespace details
{
//! NA value use in partition_NA.
constexpr auto NA = -1.0f;
} // namespace details

//! A function that arranges all NA elements to the end of the array.
/*!
 * \param i_array Unsorted array. The first partition is a stable sort of the non NA elements. For
 * the second partition is unspecified.
 * \param i_size Number of elements of i_array.
 * \return Number of non-NA elements.
 */
template<typename Float>
CUDA_HOSTDEV int partition_NA(Float* i_array, int i_size) noexcept
{
	// Sort all NA values to the end of the array.
	auto nas = 0;
	for(int i = 0; i < i_size; i++)
	{
		if(i_array[i] == Float{details::NA})
		{
			nas += 1;
		}
		else
		{
			i_array[i - nas] = i_array[i];
		}
	}

	return i_size - nas;
}