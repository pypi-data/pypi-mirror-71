#pragma once

template<typename FloatVec>
class device_patches;

struct float2;
using cuComplex = float2;

struct double2;
using cuDoubleComplex = double2;

namespace data_afmt
{
device_patches<float> patches(float tag);
device_patches<double> patches(double tag);

device_patches<cuComplex> patches_afmt(cuComplex tag);
device_patches<cuDoubleComplex> patches_afmt(cuDoubleComplex tag);
} // namespace data_afmt