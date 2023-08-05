/*! \file device_patches.h
	\brief Class for sets of patches in CUDA
	\sa device_matrix.h
*/

#pragma once

#include "Cols.h"
#include "Rows.h"
#include "Size.h"
#include "device_matrix.h"
#include "patch_index.h"

#include "../extern/gsl/gsl_assert"
#include "../extern/gsl/gsl_util"

#include <cuda_runtime.h>
#include <thrust/device_vector.h>

#include <cstddef>

//! A template class for sets of patches stored in a matrix in gpu memory.
template<typename T>
class device_patches : private device_matrix<T>
{
  public:
	//! Pointer type of device_matrix.
	using typename device_matrix<T>::pointer;
	//! Const pointer type of device_matrix.
	using typename device_matrix<T>::const_pointer;
	//! Iterator type of device_matrix.
	using typename device_matrix<T>::iterator;
	//! Const iterator type of device_matrix.
	using typename device_matrix<T>::const_iterator;
	//! Difference type of device_matrix iterator.
	using typename device_matrix<T>::difference_type;
	//! Reference type of device_matrix.
	using typename device_matrix<T>::reference;
	//! Const reference type of device_matrix.
	using typename device_matrix<T>::const_reference;

	//! Constructor.
	/*!
	 * The matrix is always stored in row major format so that patches are contiguous in memory.
	 * \param i_patches The number of patches.
	 * \param i_rows_patches The number of rows of each patch.
	 * \param i_cols_patches The number of columns of each patch.
	 * \param i_col_maj_patches If true the matrix is stored in column major format else in row
	 * major format.
	 */
	constexpr explicit device_patches(patch_index i_patches, Rows i_rows_patches,
									  Cols i_cols_patches, bool i_col_maj_patches)
		: device_patches{i_patches, i_rows_patches, i_cols_patches, T{}, i_col_maj_patches}
	{
	}

	//! Constructor.
	/*!
	 * Patches are stored row-wise in the underlying matrix.
	 * The matrix is always stored in row major format so that patches are contiguous in memory.
	 * \param i_patches The number of patches or equivalently the number of rows of the underlying
	 * matrix.
	 * \param i_rows_patches The number of rows of each patch.
	 * \param i_cols_patches The number of columns of each patch.
	 * \param i_init Initial value.
	 * \param i_col_maj_patches If true the patches are stored in column major format else in row
	 * major format.
	 */
	constexpr explicit device_patches(patch_index i_patches = patch_index{},
									  Rows i_rows_patches = Rows{}, Cols i_cols_patches = Cols{},
									  T i_init = T{}, bool i_col_maj_patches = true)
		: device_matrix<T>{Rows{i_patches.value()},
						   Cols{i_rows_patches.value() * i_cols_patches.value()}, i_init, false},
		  m_rows_patches{i_rows_patches.value()}, m_cols_patches{i_cols_patches.value()},
		  m_col_maj_patches{i_col_maj_patches}
	{
		if(m_col_maj_patches)
		{
			m_ld_patches = i_rows_patches.value();
		}
		else
		{
			m_ld_patches = i_cols_patches.value();
		}
	}

	//! Constructor.
	/*!
	 * Patches are stored row-wise in the underlying matrix.
	 * The matrix is always stored in row major format so that patches are contiguous in memory.
	 * \param i_patches The number of patches or equivalently the number of rows of the underlying
	 * matrix.
	 * \param i_size_patches The size of each patch.
	 * \param i_col_maj_patches If true the patches are stored in column major format else in row
	 * major format.
	 */
	constexpr explicit device_patches(patch_index i_patches, const Size& i_size_patches,
									  bool i_col_maj_patches)
		: device_patches{i_patches, Rows{i_size_patches.rows()}, Cols{i_size_patches.cols()}, T{},
						 i_col_maj_patches}
	{
	}

	//! Constructor.
	/*!
	 * Patches are stored row-wise in the underlying matrix.
	 * The matrix is always stored in row major format so that patches are contiguous in memory.
	 * \param i_patches The number of patches or equivalently the number of rows of the underlying
	 * matrix.
	 * \param i_size_patches The size of each patch.
	 * \param i_init Initial value.
	 * \param i_col_maj_patches If true the patches are stored in column major format else in row
	 * major format.
	 */
	constexpr explicit device_patches(patch_index i_patches, const Size& i_size_patches,
									  T i_init = T{}, bool i_col_maj_patches = true)
		: device_patches{i_patches, Rows{i_size_patches.rows()}, Cols{i_size_patches.cols()},
						 i_init, i_col_maj_patches}
	{
	}

	//! Constructor.
	/*!
	 * The matrix is always stored in row major format so that patches are contiguous in memory.
	 * \param i_data The patch data of size i_patches * i_rows_patches * i_cols_patches.
	 * \param i_patches The number of patches.
	 * \param i_rows_patches The number of rows of each patch.
	 * \param i_cols_patches The number of columns of each patch.
	 * \param i_col_maj_patches If true the matrix is stored in column major format else in row
	 * major format.
	 */
	explicit device_patches(thrust::device_vector<T> i_data, patch_index i_patches,
							Rows i_rows_patches, Cols i_cols_patches, bool i_col_maj_patches = true)
		: device_matrix<T>{std::move(i_data), Rows{i_patches.value()},
						   Cols{i_rows_patches.value() * i_cols_patches.value()}, false},
		  m_rows_patches{i_rows_patches.value()}, m_cols_patches{i_cols_patches.value()},
		  m_col_maj_patches{i_col_maj_patches}
	{
		if(m_col_maj_patches)
		{
			m_ld_patches = i_rows_patches.value();
		}
		else
		{
			m_ld_patches = i_cols_patches.value();
		}
	}

	//! Constructor.
	/*!
	 * Patches are stored row-wise in the underlying matrix.
	 * The matrix is always stored in row major format so that patches are contiguous in memory.
	 * \param i_data The patch data of size i_patches * i_size_patches.
	 * \param i_patches The number of patches or equivalently the number of rows of the underlying
	 * matrix.
	 * \param i_size_patches The size of each patch.
	 * \param i_col_maj_patches If true the patches are stored in column major format else in row
	 * major format.
	 */
	explicit device_patches(thrust::device_vector<T> i_data, patch_index i_patches,
							const Size& i_size_patches, bool i_col_maj_patches = true)
		: device_patches{std::move(i_data), i_patches, Rows{i_size_patches.rows()},
						 Cols{i_size_patches.cols()}, i_col_maj_patches}
	{
	}

	//! Constructor.
	/*!
	 * Constructs one patch from a matrix.
	 * Patches are stored row-wise in the underlying matrix.
	 * The matrix is always stored in row major format so that patches are contiguous in memory.
	 * \param i_matrix Matrix to copy.
	 */
	constexpr explicit device_patches(const device_matrix<T>& i_matrix)
		: device_patches{i_matrix.container(), patch_index{1}, Rows{i_matrix.rows()},
						 Cols{i_matrix.cols()}, i_matrix.col_maj()}
	{
	}

	//! Constructor.
	/*!
	 * Constructs one patch from a matrix.
	 * Patches are stored row-wise in the underlying matrix.
	 * The matrix is always stored in row major format so that patches are contiguous in memory.
	 * \param i_matrix Matrix to copy.
	 */
	constexpr explicit device_patches(device_matrix<T>&& i_matrix)
		: device_patches{std::move(i_matrix).container(), patch_index{1}, Rows{i_matrix.rows()},
						 Cols{i_matrix.cols()}, i_matrix.col_maj()}
	{
	}

	//! Returns the number of patches.
	std::size_t patch_count() const noexcept
	{
		return device_matrix<T>::rows();
	}

	//! Returns the number of rows per patch.
	std::size_t rows_patches() const noexcept
	{
		return m_rows_patches;
	}

	//! Returns the number of columns per patch.
	std::size_t cols_patches() const noexcept
	{
		return m_cols_patches;
	}

	//! Returns the size of a patch.
	Size size_patches() const noexcept
	{
		return Size{Rows{m_rows_patches}, Cols{m_cols_patches}};
	}

	//! Returns the total number of elements; patch_count * rows_patches * cols_patches.
	std::size_t total() const noexcept
	{
		return device_matrix<T>::total();
	}

	//! Returns the total number of elements per patch; rows_patches * cols_patches.
	std::size_t total_per_patch() const noexcept
	{
		return m_rows_patches * m_cols_patches;
	}

	//! Returns the leading dimension of a patch.
	constexpr std::size_t ld_patches() const noexcept
	{
		return m_ld_patches;
	}

	//! Returns the stride between patches; in elements not bytes.
	constexpr std::size_t ld() const noexcept
	{
		return device_matrix<T>::ld();
	}

	//! Returns true if the memory layout of a patch(!) is column-major, otherwise false.
	bool col_maj_patches() const noexcept
	{
		return m_col_maj_patches;
	}

	using device_matrix<T>::begin;
	using device_matrix<T>::cbegin;
	using device_matrix<T>::end;
	using device_matrix<T>::cend;

	//! Returns the iterator to the element at the given index.
	/*!
	 * \param ind Index of the patch.
	 * \param i_row Index of the patch row.
	 * \param i_col Index of the patch column.
	 */
	iterator begin(patch_index ind, Rows i_row = 0_rows, Cols i_col = 0_cols) noexcept
	{
		Expects(ind.value() < patch_count());
		Expects(i_row.value() < m_rows_patches);
		Expects(i_col.value() < m_cols_patches);

		if(m_col_maj_patches)
		{
			return begin() + ind.value() * ld() + i_col.value() * m_ld_patches + i_row.value();
		}
		else
		{
			return begin() + ind.value() * ld() + i_row.value() * m_ld_patches + i_col.value();
		}
	}

	//! Returns the const iterator to the element at the given index.
	/*!
	 * \param ind Index of the patch.
	 * \param i_row Index of the patch row.
	 * \param i_col Index of the patch column.
	 */
	const_iterator begin(patch_index ind, Rows i_row = 0_rows, Cols i_col = 0_cols) const noexcept
	{
		Expects(ind.value() < patch_count());
		Expects(i_row.value() < m_rows_patches);
		Expects(i_col.value() < m_cols_patches);

		if(m_col_maj_patches)
		{
			return cbegin() + ind.value() * ld() + i_col.value() * m_ld_patches + i_row.value();
		}
		else
		{
			return cbegin() + ind.value() * ld() + i_row.value() * m_ld_patches + i_col.value();
		}
	}

	//! Returns the const iterator to the element at the given index.
	/*!
	 * \param ind Index of the patch.
	 * \param i_row Index of the patch row.
	 * \param i_col Index of the patch column.
	 */
	const_iterator cbegin(patch_index ind, Rows i_row = 0_rows, Cols i_col = 0_cols) const noexcept
	{
		return begin(ind, i_row, i_col);
	}

	//! A member returning an iterator to the element following the last element in
	//! the matrix.
	iterator end(patch_index ind) noexcept
	{
		return begin(ind) + ld();
	}

	//! A member returning an iterator to the element following the last element in
	//! the matrix.
	const_iterator end(patch_index ind) const noexcept
	{
		return cbegin(ind) + ld();
	}

	//! A member returning a const iterator to the element following the last element
	//! in the matrix.
	const_iterator cend(patch_index ind) const noexcept
	{
		return cbegin(ind) + ld();
	}

	using device_matrix<T>::data;

	//! Returns a pointer to the first element of a given patch.
	pointer data(patch_index ind)
	{
		Expects(ind.value() < patch_count());

		return device_matrix<T>::data() + gsl::narrow<difference_type>(ind.value() * ld());
	}

	//! Returns a const pointer to the first element of a given patch.
	const_pointer data(patch_index ind) const
	{
		Expects(ind.value() < patch_count());

		return device_matrix<T>::data() + gsl::narrow<difference_type>(ind.value() * ld());
	}

	//! Bound checked element access.
	reference at(patch_index idx, Rows i_row, Cols i_col) & noexcept
	{
		Expects(idx.value() <= patch_count());
		Expects(i_row.value() < m_rows_patches);
		Expects(i_col.value() < m_cols_patches);

		if(m_col_maj_patches)
		{
			return device_matrix<T>::at(Rows{idx.value()},
										Cols{i_col.value() * m_ld_patches + i_row.value()});
		}
		else
		{
			return device_matrix<T>::at(Rows{idx.value()},
										Cols{i_row.value() * m_ld_patches + i_col.value()});
		}
	}

	//! Bound checked element access.
	const_reference at(patch_index idx, Rows i_row, Cols i_col) const& noexcept
	{
		Expects(idx.value() <= patch_count());
		Expects(i_row.value() < m_rows_patches);
		Expects(i_col.value() < m_cols_patches);

		if(m_col_maj_patches)
		{
			return device_matrix<T>::at(Rows{idx.value()},
										Cols{i_col.value() * m_ld_patches + i_row.value()});
		}
		else
		{
			return device_matrix<T>::at(Rows{idx.value()},
										Cols{i_row.value() * m_ld_patches + i_col.value()});
		}
	}

	//! Returns a given patch as a matrix; deep copy.
	device_matrix<T> clone(patch_index i_patch) const
	{
		const auto first = data(i_patch);
		const auto last = first + total_per_patch();
		auto out = device_matrix<T>{Rows{m_rows_patches}, Cols{m_cols_patches}, m_col_maj_patches};
		thrust::copy(first, last, out.data());

		return out;
	}

	//! A member returning the underlying container.
	constexpr thrust::device_vector<T> container() const&
	{
		return device_matrix<T>::container();
	}

	//! A member extracting the underlying container if called on a rvalue reference.
	//! The device_patches are valid, but undefined afterwards.
	constexpr thrust::device_vector<T>&& container() &&
	{
		return std::forward<thrust::device_vector<T>>(device_matrix<T>::container());
	}

  private:
	std::size_t m_rows_patches;
	std::size_t m_cols_patches;
	bool m_col_maj_patches;
	std::size_t m_ld_patches;
};