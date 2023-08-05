/*! \file unique_cufft_plan.h
	\brief RAII for cufftHandle
*/

#pragma once

#include "cufft.h"
#include "utils.h"
#include <exception>

//! Throws an exception if status is not CUFFT_SUCCESS.
inline void check_cufft(cufftResult_t status) noexcept(false)
{
	switch(status)
	{
		case CUFFT_SUCCESS:
			break;
		case CUFFT_INVALID_PLAN:
			throw std::runtime_error{"CUFFT_INVALID_PLAN"};
		case CUFFT_ALLOC_FAILED:
			throw std::runtime_error{"CUFFT_ALLOC_FAILED"};
		case CUFFT_INVALID_TYPE:
			throw std::runtime_error{"CUFFT_INVALID_TYPE"};
		case CUFFT_INVALID_VALUE:
			throw std::runtime_error{"CUFFT_INVALID_VALUE"};
		case CUFFT_INTERNAL_ERROR:
			throw std::runtime_error{"CUFFT_INTERNAL_ERROR"};
		case CUFFT_EXEC_FAILED:
			throw std::runtime_error{"CUFFT_EXEC_FAILED"};
		case CUFFT_SETUP_FAILED:
			throw std::runtime_error{"CUFFT_SETUP_FAILED"};
		case CUFFT_INVALID_SIZE:
			throw std::runtime_error{"CUFFT_INVALID_SIZE"};
		case CUFFT_UNALIGNED_DATA:
			throw std::runtime_error{"CUFFT_UNALIGNED_DATA"};
		case CUFFT_INCOMPLETE_PARAMETER_LIST:
			throw std::runtime_error{"CUFFT_INCOMPLETE_PARAMETER_LIST"};
		case CUFFT_INVALID_DEVICE:
			throw std::runtime_error{"CUFFT_INVALID_DEVICE"};
		case CUFFT_PARSE_ERROR:
			throw std::runtime_error{"CUFFT_PARSE_ERROR"};
		case CUFFT_NO_WORKSPACE:
			throw std::runtime_error{"CUFFT_NO_WORKSPACE"};
		case CUFFT_NOT_IMPLEMENTED:
			throw std::runtime_error{"CUFFT_NOT_IMPLEMENTED"};
		case CUFFT_LICENSE_ERROR:
			throw std::runtime_error{"CUFFT_LICENSE_ERROR"};
		case CUFFT_NOT_SUPPORTED:
			throw std::runtime_error{"CUFFT_NOT_SUPPORTED"};
		default:
			throw std::runtime_error{"Unknown cufft error."};
	}
}

//! RAII for cufftHandle.
class unique_cufft_plan final
{
  public:
	unique_cufft_plan() noexcept(false)
	{
		check(cufftCreate(&m_handle), CUFFT_SUCCESS);
	}
	unique_cufft_plan(const unique_cufft_plan& other) = delete;
	unique_cufft_plan& operator=(const unique_cufft_plan& other) = delete;
	~unique_cufft_plan() noexcept
	{
		cufftDestroy(m_handle);
	}

	//! Return cufftHandle.
	cufftHandle get() const noexcept
	{
		return m_handle;
	}

	//! Resets handle before creating a new plan.
	void reset() noexcept(false)
	{
		check(cufftDestroy(m_handle), CUFFT_SUCCESS);
		check(cufftCreate(&m_handle), CUFFT_SUCCESS);
	}

  private:
	cufftHandle m_handle{};
};