#pragma once

#include "../include/Size.h"

template<typename FloatVec>
class device_patches;

template <typename Float>
class device_matrix;

/*
** Patches which are related by (non orthogonal) affine matrices.
*/
namespace data_affine
{
device_patches<float> patches_lhs();
device_patches<float> patches_rhs();
device_patches<float> perspective_matrices();
void distance_matrix(const device_matrix<double>& dist_mat, double margin_low, double margin_high);
} // namespace data_affine