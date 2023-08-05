#include "../include/device_matrix.h"
#include "../include/device_patches.h"
#include "../include/enums.h"
#include "../include/vec3.h"
#include "core_py.h"
#include "utils.h"

py::array identity(const py::array& arr)
{
	if(is_matrix(arr))
	{
		if(is_grey(arr))
		{
			return download(upload_matrix(arr, float{}));
		}
		else if(is_rgb(arr))
		{
			return download(upload_matrix(arr, vec3<float>{}));
		}
		else
		{
			throw std::runtime_error{"Error in identity. Input matrix has to be grey-scale or rgb "
									 "(rgba is not supported)."};
		}
	}
	else if(is_patches(arr))
	{
		if(is_grey(arr))
		{
			return download(upload_patches(arr, float{}));
		}
		else if(is_rgb(arr))
		{
			return download(upload_patches(arr, vec3<float>{}));
		}
		else
		{
			throw std::runtime_error{"Error in identity. Input patches has to be grey-scale or rgb "
									 "(rgba is not supported)."};
		}
	}
	else
	{
		throw std::runtime_error{"Error in identity. Input has to be grey-scale or rgb "
								 " matrix or patches (rgba is not supported)."};
	}
}