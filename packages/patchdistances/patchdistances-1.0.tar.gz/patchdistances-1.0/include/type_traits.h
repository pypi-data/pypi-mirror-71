/*! \file Cols.h
	\brief Type traits for CUDA
*/

#pragma once

#include "vec3.h"

#include <cuComplex.h>
#include <thrust/complex.h>
#include <type_traits>

using namespace thrust;
using t_complex = complex<float>;
using t_complex_dbl = complex<double>;

/*
 **
 *** make_thrust_type
 **
 */

inline __host__ __device__ t_complex make_thrust_type(const cuComplex& val) noexcept
{
	return t_complex{val.x, val.y};
}

inline __host__ __device__ t_complex_dbl make_thrust_type(const cuDoubleComplex& val) noexcept
{
	return t_complex_dbl{val.x, val.y};
}

inline __host__ __device__ vec3<t_complex> make_thrust_type(const vec3<cuComplex>& val) noexcept
{
	return vec3<t_complex>{make_thrust_type(val._1), make_thrust_type(val._2),
						   make_thrust_type(val._3)};
}

inline __host__ __device__ vec3<t_complex_dbl>
	make_thrust_type(const vec3<cuDoubleComplex>& val) noexcept
{
	return vec3<t_complex_dbl>{make_thrust_type(val._1), make_thrust_type(val._2),
							   make_thrust_type(val._3)};
}

/*
 **
 *** make_complex
 **
 */

inline __host__ __device__ t_complex make_complex(float real, float img)
{
	return t_complex{real, img};
}

inline __host__ __device__ t_complex_dbl make_complex(double real, double img)
{
	return t_complex_dbl{real, img};
}

inline __host__ __device__ t_complex make_complex(float real, double img)
{
	return t_complex_dbl{real, img};
}

inline __host__ __device__ t_complex_dbl make_complex(double real, float img)
{
	return t_complex_dbl{real, img};
}

/*
 **
 *** remove_vec3
 **
 */

template<typename T>
struct remove_vec3
{
	using type = std::false_type;
};

template<>
struct remove_vec3<float>
{
	using type = float;
};

template<>
struct remove_vec3<double>
{
	using type = double;
};

template<>
struct remove_vec3<vec3<float>>
{
	using type = float;
};

template<>
struct remove_vec3<vec3<double>>
{
	using type = double;
};

template<>
struct remove_vec3<t_complex>
{
	using type = t_complex;
};

template<>
struct remove_vec3<t_complex_dbl>
{
	using type = t_complex_dbl;
};

template<>
struct remove_vec3<vec3<t_complex>>
{
	using type = t_complex;
};

template<>
struct remove_vec3<vec3<t_complex_dbl>>
{
	using type = t_complex_dbl;
};

template<typename T>
using remove_vec3_t = typename remove_vec3<T>::type;

/*
 **
 *** to_cu_type
 **
 */

template<typename Float>
struct to_cu_type
{
	using type = std::false_type;
};

template<>
struct to_cu_type<float>
{
	using type = cuComplex;
};

template<>
struct to_cu_type<double>
{
	using type = cuDoubleComplex;
};

template<typename Float>
using to_cu_type_t = typename to_cu_type<Float>::type;

/*
 **
 *** to_thrust_type
 **
 */

template<typename T>
struct to_thrust_type
{
	using type = std::false_type;
};

template<>
struct to_thrust_type<float>
{
	using type = t_complex;
};

template<>
struct to_thrust_type<double>
{
	using type = t_complex_dbl;
};

template<>
struct to_thrust_type<vec3<float>>
{
	using type = vec3<t_complex>;
};

template<>
struct to_thrust_type<vec3<double>>
{
	using type = vec3<t_complex_dbl>;
};

template<>
struct to_thrust_type<cuComplex>
{
	using type = t_complex;
};

template<>
struct to_thrust_type<cuDoubleComplex>
{
	using type = t_complex_dbl;
};

template<>
struct to_thrust_type<vec3<cuComplex>>
{
	using type = vec3<t_complex>;
};

template<>
struct to_thrust_type<vec3<cuDoubleComplex>>
{
	using type = vec3<t_complex_dbl>;
};

template<typename T>
using to_thrust_type_t = typename to_thrust_type<T>::type;

/*
 **
 *** to_real_type
 **
 */

template<typename FloatVec>
struct to_real_type
{
	using type = std::false_type;
};

template<>
struct to_real_type<t_complex>
{
	using type = float;
};

template<>
struct to_real_type<t_complex_dbl>
{
	using type = double;
};

template<>
struct to_real_type<vec3<t_complex>>
{
	using type = vec3<float>;
};

template<>
struct to_real_type<vec3<t_complex_dbl>>
{
	using type = vec3<double>;
};

template<typename FloatVec>
using to_real_type_t = typename to_real_type<FloatVec>::type;