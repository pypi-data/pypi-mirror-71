#include "utils.h"

#include "../include/device_matrix.h"
#include "../include/device_patches.h"
#include "../include/enums.h"
#include "../include/utils.h"

#include "../extern/gsl/gsl_util"

#include <thrust/device_vector.h>
#include <thrust/functional.h>
#include <thrust/inner_product.h>
#include <thrust/iterator/counting_iterator.h>
#include <thrust/random.h>
#include <thrust/transform.h>

#include <cuComplex.h>

#include <string>
#include <vector>

/*
**
*** Functions that return random matrices and patches using uniform distribution with values in
*** [0,1).
**
*/

template<typename Float>
struct rand_op
{
	rand_op(size_t off) : m{off} {}

	// Returns unique random numbers for unique n.
	__device__ Float operator()(size_t n)
	{
		auto rng = thrust::default_random_engine{};
		auto dist = thrust::uniform_real_distribution<Float>(0, 1);
		rng.discard(m + n);
		return dist(rng);
	}

  private:
	size_t m;
};

//! Returns a device_vector of random floats sampled from [0,1).
template<typename Float, typename = std::enable_if_t<std::is_floating_point<Float>::value>>
thrust::device_vector<Float> rand_vector(size_t size, Float /*tag*/)
{
	static auto offset = size_t{0}; // Ensures different output on each function call.
	auto rand_vec = thrust::device_vector<Float>(size);

	const auto begin = thrust::counting_iterator<size_t>{0};
	const auto end = thrust::counting_iterator<size_t>{size};
	thrust::transform(begin, end, rand_vec.begin(), rand_op<Float>{offset});

	offset += size;

	return rand_vec;
}

template<typename Float>
thrust::device_vector<vec3<Float>> rand_vector(size_t size, vec3<Float> /*tag*/)
{
	const auto ch0 = rand_vector(size, Float{});
	const auto ch1 = rand_vector(size, Float{});
	const auto ch2 = rand_vector(size, Float{});

	const auto ch0_ptr = ch0.data().get();
	const auto ch1_ptr = ch1.data().get();
	const auto ch2_ptr = ch2.data().get();

	auto data = thrust::device_vector<vec3<Float>>(ch0.size());
	const auto begin = thrust::counting_iterator<size_t>{0};
	const auto end = thrust::counting_iterator<size_t>{data.size()};
	thrust::transform(begin, end, data.begin(), [ch0_ptr, ch1_ptr, ch2_ptr] __device__(size_t i) {
		return vec3<Float>{ch0_ptr[i], ch1_ptr[i], ch2_ptr[i]};
	});

	return data;
}

device_matrix<float> rand_matrix(Size s, float tag)
{
	return device_matrix<float>{rand_vector(s.total(), tag), s};
}

device_matrix<double> rand_matrix(Size s, double tag)
{
	return device_matrix<double>{rand_vector(s.total(), tag), s};
}

device_matrix<vec3<float>> rand_matrix(Size s, vec3<float> tag)
{
	return device_matrix<vec3<float>>{rand_vector(s.total(), tag), s};
}

device_matrix<vec3<double>> rand_matrix(Size s, vec3<double> tag)
{
	return device_matrix<vec3<double>>{rand_vector(s.total(), tag), s};
}

device_patches<float> rand_patches(patch_index p, Size s, float tag)
{
	return device_patches<float>{rand_vector(p.value() * s.total(), tag), p, s};
}

device_patches<double> rand_patches(patch_index p, Size s, double tag)
{
	return device_patches<double>{rand_vector(p.value() * s.total(), tag), p, s};
}

device_patches<vec3<float>> rand_patches(patch_index p, Size s, vec3<float> tag)
{
	return device_patches<vec3<float>>{rand_vector(p.value() * s.total(), tag), p, s};
}

device_patches<vec3<double>> rand_patches(patch_index p, Size s, vec3<double> tag)
{
	return device_patches<vec3<double>>{rand_vector(p.value() * s.total(), tag), p, s};
}

/*
**
*** Catch2 checks, which compare matrices and patches. Eps is the expected L2 error (for each patch/
*** matrix) and margin its error margin.
**
*/

template<typename T>
struct L2 final
{
	__device__ double operator()(T lhs, T rhs) const noexcept
	{
		return static_cast<double>(sqrtf((lhs - rhs) * (lhs - rhs)));
	}
};

template<>
struct L2<vec3<float>> final
{
	__device__ double operator()(vec3<float> lhs, vec3<float> rhs) const noexcept
	{
		const auto x = lhs._1 - rhs._1;
		const auto y = lhs._2 - rhs._2;
		const auto z = lhs._3 - rhs._3;

		return norm3d(x, y, z);
	}
};

template<>
struct L2<vec3<double>> final
{
	__device__ double operator()(vec3<double> lhs, vec3<double> rhs) const noexcept
	{
		const auto x = lhs._1 - rhs._1;
		const auto y = lhs._2 - rhs._2;
		const auto z = lhs._3 - rhs._3;

		return norm3d(x, y, z);
	}
};

template<typename Complex>
constexpr __device__ double abs(const Complex& val) noexcept
{
	return sqrt(val.x * val.x + val.y * val.y + val.z * val.z);
}

template<>
struct L2<cuComplex> final
{
	__device__ double operator()(cuComplex lhs, cuComplex rhs) const noexcept
	{
		return cuCabsf(cuCsubf(lhs, rhs));
	}
};

template<>
struct L2<cuDoubleComplex> final
{
	__device__ double operator()(cuDoubleComplex lhs, cuDoubleComplex rhs) const noexcept
	{
		return cuCabs(cuCsub(lhs, rhs));
	}
};

template<>
struct L2<vec3<cuComplex>> final
{
	__device__ double operator()(vec3<cuComplex> lhs, vec3<cuComplex> rhs) const noexcept
	{
		const auto x = cuCabsf(cuCsubf(lhs._1, rhs._1));
		const auto y = cuCabsf(cuCsubf(lhs._2, rhs._2));
		const auto z = cuCabsf(cuCsubf(lhs._3, rhs._3));

		return norm3d(x, y, z);
	}
};

template<>
struct L2<vec3<cuDoubleComplex>> final
{
	__device__ double operator()(vec3<cuDoubleComplex> lhs,
								 vec3<cuDoubleComplex> rhs) const noexcept
	{
		const auto x = cuCabs(cuCsub(lhs._1, rhs._1));
		const auto y = cuCabs(cuCsub(lhs._2, rhs._2));
		const auto z = cuCabs(cuCsub(lhs._3, rhs._3));

		return norm3d(x, y, z);
	}
};

//! A template function that returns the L2 error of two matrices.
/*!
 * \param lhs Left hand side matrix.
 * \param rhs Right hand side matrix.
 * \return L2 error between lhs and rhs.
 */
template<typename T>
double l2_error(const device_matrix<T>& lhs, const device_matrix<T>& rhs)
{
	Expects(lhs.size() == rhs.size());
	Expects(lhs.ld() == rhs.ld());
	Expects(lhs.col_maj() == rhs.col_maj());

	return sqrt(thrust::inner_product(lhs.cbegin(), lhs.cend(), rhs.cbegin(), 0.0,
									  thrust::plus<double>(), L2<T>{}));
}

//! A template function that returns the L2 error of each pair of patches.
/*!
 * \param lhs Left hand side patches.
 * \param rhs Right hand side patches.
 * \return L2 error between lhs and rhs for each patch.
 */
template<typename T>
inline std::vector<double> l2_error(const device_patches<T>& lhs, const device_patches<T>& rhs)
{
	Expects(lhs.col_maj_patches() == rhs.col_maj_patches());
	Expects(lhs.size_patches() == rhs.size_patches());
	Expects(lhs.patch_count() == rhs.patch_count());

	auto errs = std::vector<double>(lhs.patch_count());
	for(size_t i = 0; i < errs.size(); i++)
	{
		const auto lhs_cbegin = lhs.cbegin(patch_index{i});
		const auto lhs_cend = lhs.cend(patch_index{i});
		const auto rhs_cbegin = rhs.cbegin(patch_index{i});
		errs.at(i) = sqrt(thrust::inner_product(lhs_cbegin, lhs_cend, rhs_cbegin, 0.0,
												thrust::plus<double>{}, L2<T>{}));
	}

	return errs;
}

template<typename T>
void is_equal_impl(const device_patches<T>& lhs, const device_patches<T>& rhs, double eps,
				   double margin)
{
	REQUIRE(lhs.patch_count() == lhs.patch_count());
	REQUIRE(lhs.size_patches() == rhs.size_patches());
	REQUIRE(lhs.col_maj_patches() == rhs.col_maj_patches());

	const auto errs = l2_error(lhs, rhs);
	for(std::size_t i = 0; i < errs.size(); i++)
	{
		const auto total_per_patch = gsl::narrow_cast<double>(lhs.total_per_patch());
		if(errs.at(i) / total_per_patch != Approx{eps}.margin(margin))
		{
			FAIL("The relative L2-error is too large, starting at patch no: "
				 << i << ". \nIs:     " << errs.at(i) / total_per_patch << "\neps:    " << eps
				 << "\nmargin: " << margin);
			break;
		}
	}
}

template<typename T>
void is_equal_impl(const device_matrix<T>& lhs, const device_matrix<T>& rhs, double eps,
				   double margin)
{
	REQUIRE(lhs.size() == rhs.size());
	REQUIRE(lhs.col_maj() == rhs.col_maj());

	const auto total = gsl::narrow_cast<double>(lhs.total());
	const auto err = l2_error(lhs, rhs) / total;
	if(err != Approx{eps}.margin(margin))
	{
		FAIL("The relative L2-error is too large.\nIs:     " << err << "\neps:    " << eps
															 << "\nmargin: " << margin);
	}
}

template<typename T>
void not_equal_impl(const device_matrix<T>& lhs, const device_matrix<T>& rhs, double eps,
					double margin)
{
	if(lhs.size() != rhs.size())
	{
		CHECK(lhs.size() != rhs.size());
		return;
	}
	if(lhs.col_maj() != rhs.col_maj())
	{
		CHECK(lhs.col_maj() != rhs.col_maj());
		return;
	}

	const auto total = gsl::narrow_cast<double>(lhs.total());
	CHECK(l2_error(lhs, rhs) / total != Approx{eps}.margin(margin));
}

void is_equal(const device_patches<float>& lhs, const device_patches<float>& rhs, double eps,
			  double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void is_equal(const device_patches<double>& lhs, const device_patches<double>& rhs, double eps,
			  double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void is_equal(const device_patches<vec3<float>>& lhs, const device_patches<vec3<float>>& rhs,
			  double eps, double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void is_equal(const device_patches<vec3<double>>& lhs, const device_patches<vec3<double>>& rhs,
			  double eps, double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void is_equal(const device_patches<cuComplex>& lhs, const device_patches<cuComplex>& rhs,
			  double eps, double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void is_equal(const device_patches<cuDoubleComplex>& lhs,
			  const device_patches<cuDoubleComplex>& rhs, double eps, double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void is_equal(const device_patches<vec3<cuComplex>>& lhs,
			  const device_patches<vec3<cuComplex>>& rhs, double eps, double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void is_equal(const device_patches<vec3<cuDoubleComplex>>& lhs,
			  const device_patches<vec3<cuDoubleComplex>>& rhs, double eps, double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void is_equal(const device_matrix<size_t>& lhs, const device_matrix<size_t>& rhs, double eps,
			  double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void is_equal(const device_matrix<float>& lhs, const device_matrix<float>& rhs, double eps,
			  double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void is_equal(const device_matrix<double>& lhs, const device_matrix<double>& rhs, double eps,
			  double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void is_equal(const device_matrix<vec3<float>>& lhs, const device_matrix<vec3<float>>& rhs,
			  double eps, double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void is_equal(const device_matrix<vec3<double>>& lhs, const device_matrix<vec3<double>>& rhs,
			  double eps, double margin)
{
	is_equal_impl(lhs, rhs, eps, margin);
}

void not_equal(const device_matrix<float>& lhs, const device_matrix<float>& rhs, double eps,
			   double margin)
{
	not_equal_impl(lhs, rhs, eps, margin);
}

void not_equal(const device_matrix<double>& lhs, const device_matrix<double>& rhs, double eps,
			   double margin)
{
	not_equal_impl(lhs, rhs, eps, margin);
}

void not_equal(const device_matrix<vec3<float>>& lhs, const device_matrix<vec3<float>>& rhs,
			   double eps, double margin)
{
	not_equal_impl(lhs, rhs, eps, margin);
}

void not_equal(const device_matrix<vec3<double>>& lhs, const device_matrix<vec3<double>>& rhs,
			   double eps, double margin)
{
	not_equal_impl(lhs, rhs, eps, margin);
}