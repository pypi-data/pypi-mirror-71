#include "../include/device_matrix.h"
#include "../include/device_patches.h"
#include "../include/vec3.h"
#include "data_reconstruction.h"

#include <vector>

namespace data_reconstruction
{
template<typename FloatVec>
device_matrix<FloatVec> image_impl(FloatVec /*tag*/)
{
	using T = FloatVec;

	const auto data = std::vector<T>{
		T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
		T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
		T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
		T{0.0}, T{0.0}, T{0.0}, T{1.0}, T{1.0}, T{1.0}, T{1.0}, T{0.0}, T{0.0}, T{0.0}, //
		T{0.0}, T{0.0}, T{0.0}, T{1.0}, T{1.0}, T{1.0}, T{1.0}, T{0.0}, T{0.0}, T{0.0}, //
		T{0.0}, T{0.0}, T{0.0}, T{1.0}, T{1.0}, T{1.0}, T{1.0}, T{0.0}, T{0.0}, T{0.0}, //
		T{0.0}, T{0.0}, T{0.0}, T{1.0}, T{1.0}, T{1.0}, T{1.0}, T{0.0}, T{0.0}, T{0.0}, //
		T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
		T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
		T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
	};

	return device_matrix<FloatVec>{data, 10_rows, 10_cols};
}

device_matrix<float> image(float tag)
{
	return image_impl(tag);
}

device_matrix<double> image(double tag)
{
	return image_impl(tag);
}

device_matrix<vec3<float>> image(vec3<float> tag)
{
	return image_impl(tag);
}

device_matrix<vec3<double>> image(vec3<double> tag)
{
	return image_impl(tag);
}

template<typename FloatVec>
device_patches<FloatVec> labels_impl(FloatVec /*tag*/)
{
	using T = FloatVec;

	const auto data = std::vector<T>{
		T{0.0}, T{0.0}, T{0.0}, // label 0
		T{0.0}, T{0.0}, T{0.0}, //
		T{0.0}, T{0.0}, T{0.0}, //
		//
		T{1.0}, T{1.0}, T{1.0}, // label 1
		T{1.0}, T{1.0}, T{1.0}, //
		T{1.0}, T{1.0}, T{1.0}, //
		//
		T{0.0}, T{0.0}, T{0.0}, // label 2
		T{0.0}, T{0.0}, T{0.0}, //
		T{0.0}, T{0.0}, T{1.0}, //
		//
		T{0.0}, T{0.0}, T{0.0}, // label 3
		T{0.0}, T{0.0}, T{1.0}, //
		T{0.0}, T{0.0}, T{1.0}, //
		//
		T{0.0}, T{0.0}, T{1.0}, // label 4
		T{0.0}, T{0.0}, T{1.0}, //
		T{0.0}, T{0.0}, T{1.0}, //
		//
		T{0.0}, T{0.0}, T{1.0}, // label 5
		T{0.0}, T{0.0}, T{1.0}, //
		T{0.0}, T{0.0}, T{0.0}, //
		//
		T{0.0}, T{0.0}, T{0.0}, // label 6
		T{0.0}, T{1.0}, T{1.0}, //
		T{0.0}, T{1.0}, T{1.0}, //
		//
		T{0.0}, T{1.0}, T{1.0}, // label 7
		T{0.0}, T{1.0}, T{1.0}, //
		T{0.0}, T{1.0}, T{1.0}, //
	};

	return device_patches<T>{data, 8_patches, 3_rows, 3_cols};
}

device_patches<float> labels(float tag)
{
	return labels_impl(tag);
}

device_patches<double> labels(double tag)
{
	return labels_impl(tag);
}

device_patches<vec3<float>> labels(vec3<float> tag)
{
	return labels_impl(tag);
}

device_patches<vec3<double>> labels(vec3<double> tag)
{
	return labels_impl(tag);
}
} // namespace data_reconstruction