/*! \file unique_cublas_handle.h
	\brief RAII for cublasHandle_t
*/

#pragma once

#include "utils.h"
#include <cublas_v2.h>
#include <exception>

//! Throws an exception if status is not CUBLAS_STATUS_SUCCESS.
inline void check_cublas(cublasStatus_t status) noexcept(false)
{
	switch(status)
	{
		case CUBLAS_STATUS_SUCCESS:
			break;
		case CUBLAS_STATUS_NOT_INITIALIZED:
			throw std::runtime_error{"CUBLAS_STATUS_NOT_INITIALIZED"};
		case CUBLAS_STATUS_ALLOC_FAILED:
			throw std::runtime_error{"CUBLAS_STATUS_ALLOC_FAILED"};
		case CUBLAS_STATUS_INVALID_VALUE:
			throw std::runtime_error{"CUBLAS_STATUS_INVALID_VALUE"};
		case CUBLAS_STATUS_ARCH_MISMATCH:
			throw std::runtime_error{"CUBLAS_STATUS_ARCH_MISMATCH"};
		case CUBLAS_STATUS_MAPPING_ERROR:
			throw std::runtime_error{"CUBLAS_STATUS_MAPPING_ERROR"};
		case CUBLAS_STATUS_EXECUTION_FAILED:
			throw std::runtime_error{"CUBLAS_STATUS_EXECUTION_FAILED"};
		case CUBLAS_STATUS_INTERNAL_ERROR:
			throw std::runtime_error{"CUBLAS_STATUS_INTERNAL_ERROR"};
		case CUBLAS_STATUS_NOT_SUPPORTED:
			throw std::runtime_error{"CUBLAS_STATUS_NOT_SUPPORTED"};
		case CUBLAS_STATUS_LICENSE_ERROR:
			throw std::runtime_error{"CUBLAS_STATUS_LICENSE_ERROR"};
		default:
			throw std::runtime_error{"Unknown cublas error."};
	}
}

//! RAII for cublasHandle_t
class unique_cublas_handle final
{
  public:
	unique_cublas_handle() noexcept(false)
	{
		check_cublas(cublasCreate_v2(&m_handle));
	}
	unique_cublas_handle(const unique_cublas_handle& other) = delete;
	unique_cublas_handle& operator=(const unique_cublas_handle& other) = delete;
	~unique_cublas_handle() noexcept
	{
		cublasDestroy_v2(m_handle);
	}

	//! Returns cublasHandle_t.
	cublasHandle_t get() const noexcept
	{
		return m_handle;
	}

  private:
	cublasHandle_t m_handle{};
};