#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/vec3.h"

TEST_CASE("Vec3", "[sample_bicubic]")
{
	CHECK(vec3<float>{1.0f} == vec3<float>{1.0f});
	CHECK_FALSE(vec3<float>{1.0f} != vec3<float>{1.0f});
	CHECK_FALSE(vec3<float>{0.0f} == vec3<float>{1.0f});
	CHECK(vec3<float>{1.0f, 1.0f, 1.0f} == vec3<float>{1.0f});
	CHECK(vec3<float>{0.0f, 1.0f, 1.0f} != vec3<float>{1.0f});

	auto val = vec3<float>{0.0f};
	val += vec3<float>{1.0};
	CHECK(val == vec3<float>{1.0f});

	val = vec3<float>{0.0f};
	val -= vec3<float>{1.0};
	CHECK(val == vec3<float>{-1.0f});

	val = vec3<float>{1.0f};
	val *= vec3<float>{2.0};
	CHECK(val == vec3<float>{2.0f});

	val = vec3<float>{1.0f};
	val /= vec3<float>{2.0};
	CHECK(val == vec3<float>{0.5f});

	val = vec3<float>{1.0f};
	val *= 2.0;
	CHECK(val == vec3<float>{2.0f});

	val = vec3<float>{1.0f};
	val /= 2.0;
	CHECK(val == vec3<float>{0.5f});

	CHECK(-vec3<float>{1.0f} == vec3<float>{-1.0f});
	CHECK(vec3<float>{2.0f} + vec3<float>{1.0f} == vec3<float>{3.0f});
	CHECK(vec3<float>{2.0f} - vec3<float>{2.0f} == vec3<float>{0.0f});
	CHECK(vec3<float>{2.0f} * vec3<float>{2.0f} == vec3<float>{4.0f});
	CHECK(vec3<float>{2.0f} / vec3<float>{2.0f} == vec3<float>{1.0f});
	CHECK(2.0f * vec3<float>{1.0f} == vec3<float>{2.0f});
	CHECK(vec3<float>{1.0f} * 2.0f == vec3<float>{2.0f});
	CHECK(vec3<float>{1.0f} / 2.0f == vec3<float>{0.5f});
}
