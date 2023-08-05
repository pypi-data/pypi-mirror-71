#define CATCH_CONFIG_ENABLE_BENCHMARKING

#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_matrix.h"
#include "../include/enums.h"
#include "../include/extract_patches.h"
#include "../include/rec_image.h"
#include "../include/utils.h"
#include "utils.h"

TEMPLATE_TEST_CASE("Reconstruction from patches (Median)", "[reconstruction]", float, double,
				   vec3<float>, vec3<double>)
{
	using T = TestType;

	GIVEN("Given a set of patches extracted from an image")
	{
		const auto vec = std::vector<T>{
			T{1.0}, T{1.0}, T{1.0}, T{1.0}, T{1.0}, //
			T{2.0}, T{2.0}, T{2.0}, T{2.0}, T{2.0}, //
			T{3.0}, T{3.0}, T{3.0}, T{3.0}, T{3.0}, //
			T{4.0}, T{4.0}, T{4.0}, T{4.0}, T{4.0}, //
			T{5.0}, T{5.0}, T{5.0}, T{5.0}, T{5.0}, //
		};
		const auto col_maj = true;
		const auto img = device_matrix<T>{thrust::device_vector<T>{vec}, 5_rows, 5_cols, col_maj};
		const auto patches = extract_patches(img, 3_rows, 3_cols);
		const auto p_count = patches.patch_count();
		const auto labels_rows = img.rows() - 3 + 1;
		const auto labels_cols = img.cols() - 3 + 1;

		REQUIRE(p_count == labels_cols * labels_rows);

		WHEN("the image is reconstructed (trivial)")
		{
			const auto img_rec = rec_image(patches, img.size(), rec_t::median);

			THEN("it equals the original image")
			{
				const auto eps = 0.0;
				const auto margin = 0.0;
				is_equal(img, img_rec, eps, margin);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Reconstruction from patches (Mean)", "[reconstruction]", float, double,
				   vec3<float>, vec3<double>)
{
	using T = TestType;

	GIVEN("Given a set of patches extracted from an image")
	{
		const auto vec = std::vector<T>{
			T{1.0}, T{1.0}, T{1.0}, T{1.0}, T{1.0}, //
			T{2.0}, T{2.0}, T{2.0}, T{2.0}, T{2.0}, //
			T{3.0}, T{3.0}, T{3.0}, T{3.0}, T{3.0}, //
			T{4.0}, T{4.0}, T{4.0}, T{4.0}, T{4.0}, //
			T{5.0}, T{5.0}, T{5.0}, T{5.0}, T{5.0}, //
		};
		const auto col_maj = true;
		const auto img = device_matrix<T>{thrust::device_vector<T>{vec}, 5_rows, 5_cols, col_maj};
		const auto patches = extract_patches(img, 3_rows, 3_cols);
		const auto p_count = patches.patch_count();
		const auto labels_rows = img.rows() - 3 + 1;
		const auto labels_cols = img.cols() - 3 + 1;

		REQUIRE(p_count == labels_cols * labels_rows);

		WHEN("the image is reconstructed (trivial)")
		{
			const auto img_rec = rec_image(patches, img.size(), rec_t::mean);

			THEN("it equals the original image")
			{
				const auto eps = 0.0;
				const auto margin = 0.0;
				is_equal(img, img_rec, eps, margin);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Reconstruction from patches and indices (Median)", "[reconstruction]", float,
				   double, vec3<float>, vec3<double>)
{
	using T = TestType;

	GIVEN("Given a set of patches and their indices extracted from an image")
	{
		const auto vec = std::vector<T>{
			T{1.0}, T{1.0}, T{1.0}, T{1.0}, T{1.0}, //
			T{2.0}, T{2.0}, T{2.0}, T{2.0}, T{2.0}, //
			T{3.0}, T{3.0}, T{3.0}, T{3.0}, T{3.0}, //
			T{4.0}, T{4.0}, T{4.0}, T{4.0}, T{4.0}, //
			T{5.0}, T{5.0}, T{5.0}, T{5.0}, T{5.0}, //
		};
		const auto col_maj = true;
		const auto img = device_matrix<T>{thrust::device_vector<T>{vec}, 5_rows, 5_cols, col_maj};
		const auto patches = extract_patches(img, 3_rows, 3_cols);
		const auto p_count = patches.patch_count();
		const auto labels_rows = img.rows() - 3 + 1;
		const auto labels_cols = img.cols() - 3 + 1;

		REQUIRE(p_count == labels_cols * labels_rows);

		const auto labels_idx =
			device_matrix<std::size_t>{d_seq(p_count), Rows{labels_rows}, Cols{labels_cols}};

		WHEN("the image is reconstructed (median)")
		{
			const auto img_rec = rec_image(labels_idx, patches, rec_t::median);

			THEN("it equals the original image")
			{
				const auto eps = 0.0;
				const auto margin = 0.0;
				is_equal(img, img_rec, eps, margin);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Reconstruction from patches and indices (Mean)", "[reconstruction]", float,
				   double, vec3<double>)
{
	using T = TestType;

	GIVEN("Given a set of patches and their indices extracted from an image")
	{
		const auto vec = std::vector<T>{
			T{1.0}, T{1.0}, T{1.0}, T{1.0}, T{1.0}, //
			T{2.0}, T{2.0}, T{2.0}, T{2.0}, T{2.0}, //
			T{3.0}, T{3.0}, T{3.0}, T{3.0}, T{3.0}, //
			T{4.0}, T{4.0}, T{4.0}, T{4.0}, T{4.0}, //
			T{5.0}, T{5.0}, T{5.0}, T{5.0}, T{5.0}, //
		};
		const auto col_maj = true;
		const auto img = device_matrix<T>{thrust::device_vector<T>{vec}, 5_rows, 5_cols, col_maj};
		const auto patches = extract_patches(img, 3_rows, 3_cols);
		const auto p_count = patches.patch_count();
		const auto labels_rows = img.rows() - 3 + 1;
		const auto labels_cols = img.cols() - 3 + 1;

		REQUIRE(p_count == labels_cols * labels_rows);

		const auto labels_idx =
			device_matrix<std::size_t>{d_seq(p_count), Rows{labels_rows}, Cols{labels_cols}};

		WHEN("the image is reconstructed (mean)")
		{
			const auto img_rec = rec_image(labels_idx, patches, rec_t::mean);

			THEN("it equals the original image")
			{
				const auto eps = 0.0;
				const auto margin = 0.0;
				is_equal(img, img_rec, eps, margin);
			}
		}
	}
}

TEST_CASE("Benchmark image reconstruction", "[reconstruction][!benchmark]")
{
	const auto patches = rand_patches(PATCH_COUNT_BENCHMARK, PATCH_SIZE_BENCHMARK, BENCHMARK_T{});
	const auto labels_idx = device_matrix<std::size_t>{d_seq(PATCH_COUNT_BENCHMARK.value()),
													   PATCH_COUNT_SIZE_BENCHMARK};

	BENCHMARK("Image reconstruction (mean)")
	{
		return rec_image(labels_idx, patches, rec_t::mean);
	};

	BENCHMARK("Image reconstruction (median)")
	{
		return rec_image(labels_idx, patches, rec_t::median);
	};
}