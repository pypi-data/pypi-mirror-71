#include "../include/device_patches.h"
#include "../include/log_polar_transform.h"
#include "../include/sample.h"
#include "../include/vec3.h"

#include "../extern/gsl/gsl_util"

#include <thrust/for_each.h>
#include <thrust/iterator/counting_iterator.h>

#include <cmath>

constexpr auto TwoPi = 6.283185307179586476925286766559005768394338798750211641949f;
constexpr auto Pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164062f;

//! Returns radius for log polar interpolation for a given image size.
/*!
 * \param i_size
 * \param bool i_whole_image If true the radius covers the whole image, otherwise it is the largest
 * radius contained in the image.
 * \return Log-polar radius.
 */
float get_log_polar_radius(const Size& i_size, bool i_whole_image)
{
	if(i_whole_image)
	{
		// +1 to avoid too small radii, because of rounding errors.
		const auto a2 = gsl::narrow_cast<float>(i_size.cols() * i_size.cols() + 1) / 4.0f;
		const auto b2 = gsl::narrow_cast<float>(i_size.rows() * i_size.rows() + 1) / 4.0f;

		return sqrt(a2 + b2);
	}
	else
	{
		// Too small radii, because of rounding errors do not matter here.
		return gsl::narrow_cast<float>(std::min(i_size.cols(), i_size.rows())) * 0.5f;
	}
}

//! Log-polar interpolation of patches with a fixed radius of 2*pi.
/*!
 * \param i_patches Patches to interpolate.
 * \param i_M Rows of the interpolated patches.
 * \param i_N Columns of the interpolated patches.
 * \param i_embed If true the patches are embedded in a black background first.
 * Otherwise, the largest disk contained in the patches is interpolated.
 * \param i_transpose If true the output will be transposed.
 * \return Log-polar interpolated patches.
 */
template<typename T>
device_patches<T> log_polar_transform_impl(const device_patches<T>& i_patches, Rows i_N, Cols i_M,
										   bool i_embed, bool i_transpose)
{
	const auto R = get_log_polar_radius(i_patches.size_patches(), i_embed);
	const auto rows = gsl::narrow_cast<int>(i_patches.rows_patches());
	const auto cols = gsl::narrow_cast<int>(i_patches.cols_patches());
	const auto rows_2 = gsl::narrow_cast<float>(i_patches.rows_patches() - 1) / 2.0f;
	const auto cols_2 = gsl::narrow_cast<float>(i_patches.cols_patches() - 1) / 2.0f;
	const auto ld = i_patches.ld();
	const auto col_maj = i_patches.col_maj_patches();

	// Angular and radial sampling steps
	const auto N = i_N.value();
	const auto M = i_M.value();
	const auto d_rho = TwoPi / gsl::narrow_cast<float>(N);
	const auto d_theta = TwoPi / gsl::narrow_cast<float>(M);

	const auto rows_out = i_transpose ? M : N;
	const auto cols_out = i_transpose ? N : M;
	auto o_patches = device_patches<T>{patch_index{i_patches.patch_count()}, Rows{rows_out},
									   Cols{cols_out}, col_maj};
	const auto o_ld = o_patches.ld();
	auto o_ptr = o_patches.data().get();
	const auto i_ptr = i_patches.data().get();

	// Each thread computes one pixel of a log_polar patch.
	const auto out_first = thrust::counting_iterator<std::size_t>{0};
	const auto out_last = thrust::counting_iterator<std::size_t>{o_patches.total()};
	thrust::for_each(out_first, out_last, [=] __device__(std::size_t el) {
		const auto p_no = el / o_ld;
		const auto p_el = el - p_no * o_ld;

		const auto _col_maj = i_transpose ? !col_maj : col_maj;
		const auto n = _col_maj ? p_el % N : p_el / M;
		const auto m = _col_maj ? p_el / N : p_el % M;

		// To be able to use FFT in the similarity invariant distance, the radius must be exp(2*pi)!
		// Thus, after computing the beam, we have to scale it accordingly.
		const auto beam = exp(n * d_rho) / exp(TwoPi) * R;
		const auto angle = m * d_theta;
		const auto x = beam * cos(angle) + cols_2;
		const auto y = beam * sin(angle) + rows_2;

		o_ptr[el] = sample(i_ptr + p_no * ld, x, y, rows, cols, col_maj, interpolation_t::bicubic);
	});

	return o_patches;
}

//! Template function to check if any component of a vec3 is nan.
template<typename T>
__device__ constexpr bool isnan(const vec3<T>& val) noexcept
{
	return isnan(val._1) || isnan(val._2) || isnan(val._3);
}

//! Inverse log-polar interpolation of patches for a fixed log polar radius of 2*pi.
/*!
 * \param i_patches Patches to interpolate.
 * \param i_M Rows of the interpolated patches.
 * \param i_N Columns of the interpolated patches.
 * \param i_embed If true, the patches were embedded in a black background in the forward
 * transformation. Otherwise, the largest disk contained in the patches was interpolated.
 * \param i_transposed If true, the input is transposed.
 * \return Inverse log-polar interpolated patches.
 */
template<typename T>
device_patches<T> log_polar_inv_transform_impl(const device_patches<T>& i_patches, Rows i_Y,
											   Cols i_X, bool i_embed, bool i_transposed)
{
	const auto R = get_log_polar_radius(Size{i_Y, i_X}, i_embed);
	const auto rows = gsl::narrow_cast<int>(i_patches.rows_patches());
	const auto cols = gsl::narrow_cast<int>(i_patches.cols_patches());
	const auto ld = i_patches.ld();
	const auto ld_patches = i_patches.ld_patches();
	const auto col_maj = i_patches.col_maj_patches();

	const auto Y = i_Y.value();
	const auto X = i_X.value();
	const auto Y_2 = gsl::narrow_cast<float>(Y - 1) * 0.5f;
	const auto X_2 = gsl::narrow_cast<float>(X - 1) * 0.5f;

	// Angular and radial sampling steps
	const auto N = i_transposed ? i_patches.cols_patches() : i_patches.rows_patches();
	const auto M = i_transposed ? i_patches.rows_patches() : i_patches.cols_patches();
	const auto d_rho = TwoPi / gsl::narrow_cast<float>(N);
	const auto d_theta = TwoPi / gsl::narrow_cast<float>(M);

	auto o_patches = device_patches<T>{patch_index{i_patches.patch_count()}, i_Y, i_X, col_maj};
	const auto o_ld = o_patches.ld();
	auto o_ptr = o_patches.data().get();
	const auto i_ptr = i_patches.data().get();
	const auto o_p_total = o_patches.total();

	// Each thread computes one pixel of the inverse log_polar patch.
	const auto out_first = thrust::counting_iterator<std::size_t>{0};
	const auto out_last = thrust::counting_iterator<std::size_t>{o_p_total};
	thrust::for_each(out_first, out_last, [=] __device__(std::size_t el) {
		const auto p_no = el / o_ld;
		const auto p_el = (p_no + 1) * o_ld - el - 1;

		const auto x = static_cast<float>(col_maj ? p_el / Y : p_el % X);
		const auto y = static_cast<float>(col_maj ? p_el % Y : p_el / X);

		// Cave: the log polar transformation uses a fixed radius of exp(2*pi)!
		// Thus, n has to be scaled accordingly.
		const auto x_2 = x - X_2;
		const auto y_2 = y - Y_2;
		const auto m = (atan2(y_2, x_2) + Pi) / d_theta;
		const auto n = log(sqrt(x_2 * x_2 + y_2 * y_2) * exp(TwoPi) / R) / d_rho;
		const auto val =
			i_transposed
				? sample(i_ptr + p_no * ld, n, m, rows, cols, col_maj, interpolation_t::bicubic)
				: sample(i_ptr + p_no * ld, m, n, rows, cols, col_maj, interpolation_t::bicubic);

		o_ptr[el] = isnan(val) ? T{} : val; // center is nan (atan2)
	});

	return o_patches;
}

device_patches<float> log_polar_transform(const device_patches<float>& i_patches, Rows i_M,
										  Cols i_N, bool i_embed, bool i_transpose)
{
	return log_polar_transform_impl(i_patches, i_M, i_N, i_embed, i_transpose);
}

device_patches<double> log_polar_transform(const device_patches<double>& i_patches, Rows i_M,
										   Cols i_N, bool i_embed, bool i_transpose)
{
	return log_polar_transform_impl(i_patches, i_M, i_N, i_embed, i_transpose);
}

device_patches<vec3<float>> log_polar_transform(const device_patches<vec3<float>>& i_patches,
												Rows i_M, Cols i_N, bool i_embed, bool i_transpose)
{
	return log_polar_transform_impl(i_patches, i_M, i_N, i_embed, i_transpose);
}

device_patches<vec3<double>> log_polar_transform(const device_patches<vec3<double>>& i_patches,
												 Rows i_M, Cols i_N, bool i_embed, bool i_transpose)
{
	return log_polar_transform_impl(i_patches, i_M, i_N, i_embed, i_transpose);
}

device_patches<float> log_polar_inv_transform(const device_patches<float>& i_patches, Rows i_Y,
											  Cols i_X, bool i_embed, bool i_transposed)
{
	return log_polar_inv_transform_impl(i_patches, i_Y, i_X, i_embed, i_transposed);
}

device_patches<double> log_polar_inv_transform(const device_patches<double>& i_patches, Rows i_Y,
											   Cols i_X, bool i_embed, bool i_transposed)
{
	return log_polar_inv_transform_impl(i_patches, i_Y, i_X, i_embed, i_transposed);
}

device_patches<vec3<float>> log_polar_inv_transform(const device_patches<vec3<float>>& i_patches,
													Rows i_Y, Cols i_X, bool i_embed,
													bool i_transposed)
{
	return log_polar_inv_transform_impl(i_patches, i_Y, i_X, i_embed, i_transposed);
}

device_patches<vec3<double>> log_polar_inv_transform(const device_patches<vec3<double>>& i_patches,
													 Rows i_Y, Cols i_X, bool i_embed,
													 bool i_transposed)
{
	return log_polar_inv_transform_impl(i_patches, i_Y, i_X, i_embed, i_transposed);
}