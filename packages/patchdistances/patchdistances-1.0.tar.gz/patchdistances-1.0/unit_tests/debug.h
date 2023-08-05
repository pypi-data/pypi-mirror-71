#pragma once

#include "../include/device_matrix.h"
#include "../include/vec3.h"

#include <cuComplex.h>
#include <thrust/complex.h>
#include <thrust/device_vector.h>

#include <iostream>
#include <sstream>
#include <vector>

// Functions to print matrices and patches.
inline void push_back(std::ostringstream& str, float val)
{
	str << std::fixed << val;
}

inline void push_back(std::ostringstream& str, double val)
{
	str << std::fixed << val;
}

inline void push_back(std::ostringstream& str, std::size_t val)
{
	str << val;
}

inline void push_back(std::ostringstream& str, const cuComplex& val)
{
	str << std::fixed << "(" << cuCrealf(val) << "," << cuCimagf(val) << ")";
}

inline void push_back(std::ostringstream& str, const cuDoubleComplex& val)
{
	str << std::fixed << "(" << cuCreal(val) << "," << cuCimag(val) << ")";
}

inline void push_back(std::ostringstream& str, const thrust::complex<float>& val)
{
	str << std::fixed << "(" << val.real() << "," << val.imag() << ")";
}

inline void push_back(std::ostringstream& str, const thrust::complex<double>& val)
{
	str << std::fixed << "(" << val.real() << "," << val.imag() << ")";
}

inline void push_back(std::ostringstream& str, const vec3<float>& val)
{
	str << std::fixed << "(" << val._1 << "," << val._2 << "," << val._3 << ")";
}

inline void push_back(std::ostringstream& str, const vec3<double>& val)
{
	str << std::fixed << "(" << val._1 << "," << val._2 << "," << val._3 << ")";
}

inline void push_back(std::ostringstream& str, const vec3<cuComplex>& val)
{
	str << std::fixed << "{(" << val._1.x << "," << val._1.y << "),(" << val._2.x << "," << val._2.y
		<< "),(" << val._3.x << "," << val._3.y << ")}";
}

inline void push_back(std::ostringstream& str, const vec3<cuDoubleComplex>& val)
{
	str << std::fixed << "{(" << val._1.x << "," << val._1.y << "),(" << val._2.x << "," << val._2.y
		<< "),(" << val._3.x << "," << val._3.y << ")}";
}

inline void push_back(std::ostringstream& str, const vec3<thrust::complex<float>>& val)
{
	str << std::fixed << "{(" << val._1.real() << "," << val._1.imag() << "),(" << val._2.real()
		<< "," << val._2.imag() << "),(" << val._3.real() << "," << val._3.imag() << ")}";
}

inline void push_back(std::ostringstream& str, const vec3<thrust::complex<double>>& val)
{
	str << std::fixed << "{(" << val._1.real() << "," << val._1.imag() << "),(" << val._2.real()
		<< "," << val._2.imag() << "),(" << val._3.real() << "," << val._3.imag() << ")}";
}

template<typename T>
void print(const thrust::device_vector<T>& vec, std::streamsize prec = 3)
{
	std::ostringstream str;
	str.precision(prec);

	for(const auto& val : vec)
	{
		str << std::fixed << val << " ";
	}
	std::cerr << str.str() << "\n";
}

template<typename T>
void print(const std::vector<T>& vec, std::streamsize prec = 3)
{
	std::ostringstream str;
	str.precision(prec);

	for(const auto& val : vec)
	{
		str << std::fixed << val << " ";
	}
	std::cerr << str.str() << "\n";
}

template<typename T>
void print(const device_matrix<T>& mat, std::streamsize prec = 3)
{
	std::ostringstream str;
	str.precision(prec);

	for(std::size_t row = 0; row < mat.rows(); row++)
	{
		for(std::size_t col = 0; col < mat.cols(); col++)
		{
			const auto rows = mat.rows();
			push_back(str, mat.at(Rows{row}, Cols{col}));
			str << " ";
		}
		str << "\n";
	}
	std::cerr << str.str() << "\n";
}

template<typename T>
void print(const device_patches<T>& patches, patch_index no, std::streamsize prec = 3)
{
	std::ostringstream str;
	str.precision(prec);

	str << "patch: " << no.value() << "\n";
	for(std::size_t row = 0; row < patches.rows_patches(); row++)
	{
		for(std::size_t col = 0; col < patches.cols_patches(); col++)
		{
			const auto rows = patches.rows_patches();
			push_back(str, patches.at(no, Rows{row}, Cols{col}));
			str << " ";
		}
		str << "\n";
	}
	std::cerr << str.str() << "\n";
}

template<typename T>
void print(const device_patches<T>& patches, std::streamsize prec = 3)
{
	for(size_t i = 0; i < patches.patch_count(); i++)
	{
		print(patches, patch_index{i}, prec);
	}
}