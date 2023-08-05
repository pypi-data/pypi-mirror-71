#include "../include/determinant.h"
#include "../include/device_patches.h"
#include "../include/utils.h"

#include <cuda_runtime.h>
#include <thrust/device_vector.h>

using uint = unsigned int;

//! Templated CUDA kernel to compute the determinant of an affine transformation from patch moments.
/*!
 * blockDim: 1, gridDim: Tf patches, Tg patches
 * The input and output memory is not allowed to overlap.
 * \param i_Tf A set of image moments matrices T.
 * \param i_Tg A set of image moments ymatrices T.
 * \param o_det Determinants of the affine transformation associated to the pair of moments i_Tf[i],
 * i_Tg[i].
 * \parma i_rows Rows of the matrices T.
 * \param i_stride Stride between the patches of Tf, Tg.
 */
template<typename Float>
__global__ void det_kernel(const Float* __restrict i_Tf, const Float* __restrict i_Tg,
						   Float* __restrict o_det, uint i_rows, uint i_stride)
{
	const auto off = blockIdx.x * i_stride;

	auto sum_fg = Float{};
	auto sum_gg = Float{};
	for(uint i = 0; i < i_rows; i++)
	{
		const auto f = i_Tf[off + i];
		const auto g = i_Tg[off + i];
		sum_fg += f * g;
		sum_gg += g * g;
	}

	o_det[blockIdx.x] = sum_fg / sum_gg;
}

//! Templated function to compute the determinant of an affine transformation from patch moments.
/*!
 * \param i_Tf A set of image moment matrices T.
 * \param i_Tg A set of image moment matrices T.
 * \return Determinants of the affine transformation associated to the pair of moments i_Tf[i],
 * i_Tg[i].
 */
template<typename Float>
thrust::device_vector<Float> determinant_impl(const device_patches<Float>& i_Tf,
											  const device_patches<Float>& i_Tg)
{
	Expects(i_Tf.patch_count() == i_Tg.patch_count());
	Expects(i_Tf.ld() == i_Tg.ld());

	auto dets = thrust::device_vector<Float>{i_Tf.patch_count()};
	const auto blockDim = dim3{1};
	const auto gridDim = dim3{gsl::narrow<uint>(i_Tf.patch_count())};
	const auto rows = gsl::narrow_cast<uint>(i_Tf.rows_patches());
	const auto stride = gsl::narrow_cast<uint>(i_Tf.ld());

	det_kernel<<<gridDim, blockDim>>>(i_Tf.data().get(), i_Tg.data().get(), dets.data().get(), rows,
									  stride);

	check(cudaDeviceSynchronize(), cudaSuccess);

	return dets;
}

thrust::device_vector<float> determinant(const device_patches<float>& i_Tf,
										 const device_patches<float>& i_Tg)
{
	return determinant_impl(i_Tf, i_Tg);
}

thrust::device_vector<double> determinant(const device_patches<double>& i_Tf,
										  const device_patches<double>& i_Tg)
{
	return determinant_impl(i_Tf, i_Tg);
}