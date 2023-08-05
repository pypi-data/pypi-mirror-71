/*! \file strided_range.h
	\brief Iterator calls for a strided range
	\sa device_matrix.h, device_patches.h
*/

#pragma once

#include <thrust/functional.h>
#include <thrust/iterator/counting_iterator.h>
#include <thrust/iterator/permutation_iterator.h>
#include <thrust/iterator/transform_iterator.h>

//! Iterator class for a strided range.
template<typename Iterator>
class strided_range
{
  public:
	//! Difference type of Iterator template type.
	using difference_type = typename thrust::iterator_difference<Iterator>::type;

	//! Class computing the stride of an index.
	struct stride_functor : public thrust::unary_function<difference_type, difference_type>
	{
		//! Stride between elements.
		difference_type stride;

		//! Constructor.
		stride_functor(difference_type stride) : stride(stride) {}

		//! Strided index of input index.
		__host__ __device__ difference_type operator()(const difference_type& i) const noexcept
		{
			return stride * i;
		}
	};

	//! Thrust counting iterator type of difference_type.
	using CountingIterator = thrust::counting_iterator<difference_type>;
	//! Thrust transform iterator type of stride_functor and CountingIterator.
	using TransformIterator = thrust::transform_iterator<stride_functor, CountingIterator>;
	//! Thrust permutation iterator type of Iterator template type and TransformIterator.
	using PermutationIterator = thrust::permutation_iterator<Iterator, TransformIterator>;
	//! Shorthand for PermutationIterator.
	using iterator = PermutationIterator;

	//! Construct strided_range for the range [first,last).
	/*!
	 * \param first Range begin.
	 * \param last Range end.
	 * \param stride Stride between consecutive elements.
	 */
	explicit strided_range(Iterator first, Iterator last, difference_type stride) noexcept
		: first(first), last(last), stride(stride)
	{
	}

	//! Iterator to the first element.
	/*!
	 * \return Iterator to the first element.
	 */
	iterator begin() const noexcept
	{
		return PermutationIterator(first,
								   TransformIterator(CountingIterator(0), stride_functor(stride)));
	}

	//! Iterator to the last element.
	/*!
	 * \return Iterator to the last element.
	 */
	iterator end() const noexcept
	{
		return begin() + ((last - first) + (stride - 1)) / stride;
	}

  protected:
	Iterator first; /**< Iterator to first element of the range. */
	Iterator last; /**< Iterator to last element of the range. */
	difference_type stride; /**< Stride between elements in the range. */
};