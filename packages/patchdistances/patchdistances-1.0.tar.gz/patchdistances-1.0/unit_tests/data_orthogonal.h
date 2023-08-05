#pragma once

template<typename FloatVec>
class device_patches;

template <typename Float>
class device_matrix;

template<typename Float>
class vec3;

#include <cstddef>
#include <vector>

/*
** Patches which are related by orthogonal affine matrices.
*/
namespace data_orthogonal
{
device_patches<float> patches_lhs(float tag);
device_patches<double> patches_lhs(double tag);
device_patches<float> patches_rhs(float tag);
device_patches<double> patches_rhs(double tag);

device_patches<vec3<float>> patches_lhs(vec3<float> tag);
device_patches<vec3<double>> patches_lhs(vec3<double> tag);
device_patches<vec3<float>> patches_rhs(vec3<float> tag);
device_patches<vec3<double>> patches_rhs(vec3<double> tag);

device_patches<float> perspective_matrices(float tag);
device_patches<float> perspective_matrices(double tag);
device_patches<float> perspective_matrices(vec3<float> tag);
device_patches<float> perspective_matrices(vec3<double> tag);

void distance_matrix(const device_matrix<double>& dist_mat, double margin_low, double margin_high);

device_patches<float> moments_clip_rhs(float tag, bool high_order);
device_patches<double> moments_clip_rhs(double tag, bool high_order);

device_patches<float> clustering();
std::vector<size_t> clustering_solution();
} // namespace data_orthogonal