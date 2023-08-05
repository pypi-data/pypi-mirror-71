#pragma once

template<typename FloatVec>
class device_patches;

template<typename Float>
class vec3;

/*
** Image and labels to test image reconstruction.
*/
namespace data_reconstruction
{
device_matrix<float> image(float tag);
device_matrix<double> image(double tag);
device_matrix<vec3<float>> image(vec3<float> tag);
device_matrix<vec3<double>> image(vec3<double> tag);

device_patches<float> labels(float tag);
device_patches<double> labels(double tag);
device_patches<vec3<float>> labels(vec3<float> tag);
device_patches<vec3<double>> labels(vec3<double> tag);
} // namespace data_reconstruction