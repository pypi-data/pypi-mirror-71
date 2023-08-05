#pragma once

template<typename FloatVec>
class device_patches;

template<typename Float>
class device_matrix;

template<typename Float>
class vec3;

#include <cstddef>
#include <vector>

/*
** Patches which are related by similar affine matrices.
*/
namespace data_similar
{
device_patches<float> patches_lhs(float tag);
device_patches<double> patches_lhs(double tag);
device_patches<float> patches_rhs(float tag);
device_patches<double> patches_rhs(double tag);

device_patches<vec3<float>> patches_lhs(vec3<float> tag);
device_patches<vec3<double>> patches_lhs(vec3<double> tag);
device_patches<vec3<float>> patches_rhs(vec3<float> tag);
device_patches<vec3<double>> patches_rhs(vec3<double> tag);

device_patches<float> patches_rhs_log_polar(float tag);
device_patches<double> patches_rhs_log_polar(double tag);
device_patches<vec3<float>> patches_rhs_log_polar(vec3<float> tag);
device_patches<vec3<double>> patches_rhs_log_polar(vec3<double> tag);

device_patches<float> perspective_matrices();

device_patches<float> clustering();
std::vector<size_t> clustering_solution();

void distance_matrix(const device_matrix<double>& dist_mat, double margin_low, double margin_high);
} // namespace data_similar