/*! \file device_matrix.h
	\brief Matrix class in CUDA
*/

#pragma once

#include "Cols.h"
#include "Rows.h"
#include "Size.h"
#include "strided_range.h"

#include "../extern/gsl/gsl_assert"
#include "../extern/gsl/gsl_util"

#include <thrust/device_vector.h>

#include <cstddef>

// Remark: Data in the following classes is not aligned for 2D (device_matrix) or 3D
// (device_patches) access. Devices of compute capability 2.0 or higher have a negligible
// performance penalty for misaligned but coalesced memory access.

//! A template class for matrices stored in gpu memory.
template<typename T>
class device_matrix
{
  public:
	//! Pointer type of thrust::device_vector.
	using pointer = typename thrust::device_vector<T>::pointer;
	//! Const pointer type of thrust::device_vector.
	using const_pointer = typename thrust::device_vector<T>::const_pointer;
	//! Iterator type of thrust::device_vector.
	using iterator = typename thrust::device_vector<T>::iterator;
	//! Const iterator type of thrust::device_vector.
	using const_iterator = typename thrust::device_vector<T>::const_iterator;
	//! Iterator difference type of thrust::device_vector.
	using difference_type = typename thrust::iterator_difference<iterator>::type;
	//! Reference type of thrust::device_vector.
	using reference = typename thrust::device_vector<T>::reference;
	//! Const reference type of thrust::device_vector.
	using const_reference = typename thrust::device_vector<T>::const_reference;
	//! Strided range for iterator of thrust::device_vector..
	using range_t = strided_range<iterator>;
	//! Strided range for const iterator of thrust::device_vector.
	using const_range_t = strided_range<const_iterator>;

	//! Constructor.
	/*!
	 * \param i_rows The number of rows.
	 * \param i_cols The number of columns.
	 * \param i_col_major If true the matrix is stored in column major format else in row major
	 * format.
	 */
	constexpr explicit device_matrix(Rows i_rows = Rows{}, Cols i_cols = Cols{},
									 bool i_col_major = true)
		: device_matrix{i_rows, i_cols, T{}, i_col_major}

	{
	}

	//! Constructor.
	/*!
	 * \param i_size The matrix size.
	 * \param i_col_major If true the matrix is stored in column major format else in row major
	 * format.
	 */
	constexpr explicit device_matrix(Size i_size, bool i_col_major = true)
		: device_matrix{Rows{i_size.rows()}, Cols{i_size.cols()}, T{}, i_col_major}
	{
	}

	//! Constructor.
	/*!
	 * \param i_rows The number of rows.
	 * \param i_cols The number of columns.
	 * \param i_init Initial value.
	 * \param i_col_major If true the matrix is stored in column major format else in row major
	 * format.
	 */
	constexpr explicit device_matrix(Rows i_rows, Cols i_cols, T i_init, bool i_col_major = true)
		: m_data(i_rows.value() * i_cols.value(), i_init), m_rows{i_rows.value()},
		  m_cols{i_cols.value()}, m_col_major{i_col_major}
	{
		if(m_col_major)
		{
			m_ld = i_rows.value();
		}
		else
		{
			m_ld = i_cols.value();
		}
	}

	//! Constructor.
	/*!
	 * \param i_size The matrix size.
	 * \param i_init Initial value.
	 * \param i_col_major If true the matrix is stored in column major format else in row major
	 * format.
	 */
	constexpr explicit device_matrix(Size i_size, T i_init, bool i_col_major = true)
		: device_matrix{Rows{i_size.rows()}, Cols{i_size.cols()}, i_init, i_col_major}
	{
	}

	//! Constructor.
	/*!
	 * \param i_data The matrix data of size i_rows * i_cols.
	 * \param i_size The matrix size.
	 * \param i_col_major If true the matrix is stored in column major format else in row major
	 * format.
	 */
	explicit device_matrix(thrust::device_vector<T> i_data, Size i_size, bool i_col_major = true)
		: device_matrix{std::move(i_data), Rows{i_size.rows()}, Cols{i_size.cols()}, i_col_major}
	{
	}

	//! Constructor.
	/*!
	 * \param i_data The matrix data of size i_rows * i_cols.
	 * \param i_rows The number of rows.
	 * \param i_cols The number of columns.
	 * \param i_col_major If true the matrix is stored in column major format else in row major
	 * format.
	 */
	explicit device_matrix(thrust::device_vector<T> i_data, Rows i_rows, Cols i_cols,
						   bool i_col_major = true)
		: m_data{std::move(i_data)}, m_rows{i_rows.value()}, m_cols{i_cols.value()},
		  m_col_major{i_col_major}
	{
		Expects(m_data.size() == m_rows * m_cols);
		if(m_col_major)
		{
			m_ld = i_rows.value();
		}
		else
		{
			m_ld = i_cols.value();
		}
	}

	//! A member returning the number of rows.
	constexpr std::size_t rows() const noexcept
	{
		return m_rows;
	}

	//! A member returning the number of columns.
	constexpr std::size_t cols() const noexcept
	{
		return m_cols;
	}

	//! A member returning the leading dimension.
	constexpr std::size_t ld() const noexcept
	{
		return m_ld;
	}

	//! A member returning the size of the matrix.
	constexpr Size size() const noexcept
	{
		return Size{Rows{m_rows}, Cols{m_cols}};
	}

	//! A member returning the total number of elements.
	constexpr std::size_t total() const noexcept
	{
		return m_rows * m_cols;
	}

	//! A member returning true if the matrix is stored in column-major format.
	constexpr bool col_maj() const noexcept
	{
		return m_col_major;
	}

	//! A member returning a device_ptr to the first element.
	constexpr pointer data() noexcept
	{
		return m_data.data();
	}

	//! A member returning a const device_ptr to the first element.
	constexpr const_pointer data() const noexcept
	{
		return m_data.data();
	}

	//! A member returning a range for iterating over one row.
	constexpr range_t range(Rows i_row)
	{
		Expects(i_row.value() < m_rows);

		if(m_col_major)
		{
			const auto _begin = m_data.begin() + gsl::narrow<difference_type>(i_row.value());
			const auto _end = m_data.end();
			const auto stride = gsl::narrow<difference_type>(m_ld);

			return range_t{_begin, _end, stride};
		}
		else
		{
			const auto _begin =
				m_data.begin() + gsl::narrow<difference_type>(i_row.value() * m_cols);
			const auto _end = _begin + gsl::narrow<difference_type>(m_cols);
			const auto stride = gsl::narrow<difference_type>(1);

			return range_t{_begin, _end, stride};
		}
	}

	//! A member returning a const range for iterating over one row.
	constexpr const_range_t range(Rows i_row) const
	{
		Expects(i_row.value() < m_rows);

		if(m_col_major)
		{
			const auto _cbegin = m_data.cbegin() + gsl::narrow<difference_type>(i_row.value());
			const auto _cend = m_data.cend();
			const auto stride = gsl::narrow<difference_type>(m_ld);

			return const_range_t{_cbegin, _cend, stride};
		}
		else
		{
			const auto _cbegin =
				m_data.cbegin() + gsl::narrow<difference_type>(i_row.value() * m_cols);
			const auto _cend = _cbegin + gsl::narrow<difference_type>(m_cols);
			const auto stride = gsl::narrow<difference_type>(1);

			return const_range_t{_cbegin, _cend, stride};
		}
	}

	//! A member returning a range for iterating over one column.
	constexpr range_t range(Cols i_col)
	{
		Expects(i_col.value() < m_cols);

		if(m_col_major)
		{
			const auto _begin =
				m_data.begin() + gsl::narrow<difference_type>(i_col.value() * m_rows);
			const auto _end = _begin + gsl::narrow<difference_type>(m_rows);
			const auto stride = gsl::narrow<difference_type>(1);

			return range_t{_begin, _end, stride};
		}
		else
		{
			const auto _begin = m_data.begin() + gsl::narrow<difference_type>(i_col.value());
			const auto _end = m_data.end();
			const auto stride = gsl::narrow<difference_type>(m_ld);

			return range_t{_begin, _end, stride};
		}
	}

	//! A member returning a const range for iterating over one column.
	constexpr const_range_t range(Cols i_col) const
	{
		Expects(i_col.value() < m_cols);

		if(m_col_major)
		{
			const auto _cbegin =
				m_data.cbegin() + gsl::narrow<difference_type>(i_col.value() * m_rows);
			const auto _cend = _cbegin + gsl::narrow<difference_type>(m_rows);
			const auto stride = gsl::narrow<difference_type>(1);

			return const_range_t{_cbegin, _cend, stride};
		}
		else
		{
			const auto _cbegin = m_data.cbegin() + gsl::narrow<difference_type>(i_col.value());
			const auto _cend = m_data.cend();
			const auto stride = gsl::narrow<difference_type>(m_ld);

			return const_range_t{_cbegin, _cend, stride};
		}
	}

	//! A member returning an iterator over all elements.
	/*!
	 * The iteration order can be determined with the member function
	 * col_maj(). The default is iterating over the columns.
	 * \sa isColumnMajor
	 * \return Iterator.
	 */
	constexpr iterator begin() noexcept
	{
		return m_data.begin();
	}

	//! A member returning an iterator over all elements.
	/*!
	 * The iteration order can be determined with the member function
	 * col_maj(). The default is iterating over the columns.
	 * \sa isColumnMajor
	 * \return Iterator.
	 */
	constexpr const_iterator begin() const noexcept
	{
		return m_data.begin();
	}

	//! A member returning a const iterator over all elements.
	/*!
	 * The iteration order can be determined with the member function
	 * col_maj(). The default is iterating over the columns.
	 * \sa isCoulmnMajor
	 * \return Const iterator.
	 */
	constexpr const_iterator cbegin() const noexcept
	{
		return m_data.cbegin();
	}

	//! A member returning an iterator to element following the last element in
	//! the matrix.
	constexpr iterator end() noexcept
	{
		return m_data.end();
	}

	//! A member returning an iterator to element following the last element in
	//! the matrix.
	constexpr const_iterator end() const noexcept
	{
		return m_data.end();
	}

	//! A member returning a const iterator to element following the last element
	//! in the matrix.
	constexpr const_iterator cend() const noexcept
	{
		return m_data.cend();
	}

	//! Subscript operator. Out of bound accesses are undefined.
	reference operator[](std::size_t i_pos) & noexcept
	{
		return m_data[i_pos];
	}

	//! Subscript operator. Out of bound accesses are undefined.
	constexpr const_reference operator[](std::size_t i_pos) const& noexcept
	{
		return m_data[i_pos];
	}

	//! Bound checked element access.
	constexpr reference at(Rows i_row, Cols i_col) & noexcept
	{
		Expects(i_row.value() < m_rows);
		Expects(i_col.value() < m_cols);

		if(m_col_major)
		{
			return m_data[i_col.value() * m_ld + i_row.value()];
		}
		else
		{
			return m_data[i_row.value() * m_ld + i_col.value()];
		}
	}

	//! Bound checked element access.
	constexpr const_reference at(Rows i_row, Cols i_col) const& noexcept
	{
		Expects(i_row.value() < m_rows);
		Expects(i_col.value() < m_cols);

		if(m_col_major)
		{
			return m_data[i_col.value() * m_ld + i_row.value()];
		}
		else
		{
			return m_data[i_row.value() * m_ld + i_col.value()];
		}
	}

	//! A member returning the underlying container.
	constexpr thrust::device_vector<T> container() const&
	{
		return m_data;
	}

	//! A member extracting the underlying container if called on a rvalue reference.
	//! The device_matrix is valid, but undefined afterwards.
	constexpr thrust::device_vector<T>&& container() &&
	{
		return std::move(m_data);
	}

  private:
	thrust::device_vector<T> m_data;

	std::size_t m_rows{};
	std::size_t m_cols{};
	std::size_t m_ld{};
	bool m_col_major{true};
};