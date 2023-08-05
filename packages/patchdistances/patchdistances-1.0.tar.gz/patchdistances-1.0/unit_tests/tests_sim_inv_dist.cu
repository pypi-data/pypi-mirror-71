#define CATCH_CONFIG_ENABLE_BENCHMARKING

#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/device_matrix.h"
#include "../include/enums.h"
#include "../include/extract_patches.h"
#include "../include/math.h"
#include "../include/sim_inv_dist.h"
#include "../include/utils.h"
#include "data_afmt.h"
#include "data_reconstruction.h"
#include "data_similar.h"
#include "utils.h"

#include <cstddef>
#include <type_traits>
#include <utility>

auto default_params()
{
	auto params = sid_params{};
	params.log_polar_size = 16;
	params.descriptors_rows = 4_rows;
	params.descriptors_cols = 4_cols;
	params.sigma = 0.5f;

	return params;
}

TEMPLATE_TEST_CASE("Analytical Fourier-Mellin transform", "[similarity_invariant_distance]", float,
				   double)
{
	const auto patches = data_afmt::patches(TestType{});

	sim_inv_dist dist{};
	const auto afmt_patches = dist.afmt(patches, 0.5f);

	using complex_t = std::remove_pointer_t<decltype(afmt_patches.data().get())>;
	const auto solution = data_afmt::patches_afmt(complex_t{});

	constexpr auto eps = 0.0;
	constexpr auto margin = 0.01;
	is_equal(afmt_patches, solution, eps, margin);
}

TEMPLATE_TEST_CASE("Similarity transformations", "[similarity_invariant_distance]", float, double,
				   vec3<float>, vec3<double>)
{
	GIVEN("A set of similar images (embedded in a homogeneous background)")
	{
		const auto patches0 = data_similar::patches_lhs(TestType{});
		const auto patches1 = data_similar::patches_rhs(TestType{});

		WHEN("the similarity transformations are computed")
		{
			sim_inv_dist dist{};
			const auto As = dist.perspective_transformations(patches0, patches1, default_params());

			THEN("they equal the known solution")
			{
				const auto solution = data_similar::perspective_matrices();

				constexpr auto eps = 0.0;
				constexpr auto margin = 0.1;
				is_equal(As, solution, eps, margin);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Distance matrix (similarity invariant distance)",
				   "[similarity_invariant_distance]", float, double, vec3<float>, vec3<double>)
{
	GIVEN("A set of similar images (embedded in a homogeneous background)")
	{
		const auto patches0 = data_similar::patches_lhs(TestType{});
		const auto patches1 = data_similar::patches_rhs(TestType{});

		WHEN("the similarity invariant distance is computed")
		{
			sim_inv_dist dist{};
			const auto dist_mat = dist.distance_matrix(patches0, patches1, default_params());

			THEN("it is ~0")
			{
				constexpr auto margin_low = std::is_floating_point<TestType>::value ? 0.2 : 0.3;
				constexpr auto margin_high = std::is_floating_point<TestType>::value ? 1.0 : 2.0;
				data_similar::distance_matrix(dist_mat, margin_low, margin_high);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Reconstruction (similarity invariant distance)",
				   "[similarity_invariant_distance]", float, double, vec3<float>, vec3<double>)
{
	GIVEN("an image and labels")
	{
		const auto img = data_reconstruction::image(TestType{});
		const auto labels = data_reconstruction::labels(TestType{});
		const auto patches = extract_patches(img, labels.size_patches());

		WHEN("the image is reconstructed using the labels")
		{
			sim_inv_dist dist{};
			const auto image_reconstruction_mean = dist.reconstruct(
				patches, labels, img.size(), rec_t::mean, default_params(), interpolation_t::nn);
			const auto image_reconstruction_median = dist.reconstruct(
				patches, labels, img.size(), rec_t::median, default_params(), interpolation_t::nn);

			THEN("it is equal to the original image")
			{
				constexpr auto eps = 0.0;
				constexpr auto margin = 0.0;
				is_equal(std::get<0>(image_reconstruction_mean), img, eps, margin);
				is_equal(std::get<0>(image_reconstruction_median), img, eps, margin);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Reconstruction with translation(similarity invariant distance)",
				   "[similarity_invariant_distance]", float, double, vec3<float>, vec3<double>)
{
	GIVEN("an image and labels")
	{
		const auto img = data_reconstruction::image(TestType{});
		const auto labels = data_reconstruction::labels(TestType{});
		const auto patches = extract_patches(img, labels.size_patches());

		WHEN("the image is reconstructed using the labels and with allowing translation of labels")
		{
			sim_inv_dist dist{};
			const auto image_reconstruction_mean = dist.reconstruct_w_translation(
				patches, labels, img.size(), rec_t::mean, default_params(), interpolation_t::nn);
			const auto image_reconstruction_median = dist.reconstruct_w_translation(
				patches, labels, img.size(), rec_t::median, default_params(), interpolation_t::nn);

			THEN("it is equal to the original image")
			{
				constexpr auto eps = 0.0;
				constexpr auto margin = 0.0;
				is_equal(std::get<0>(image_reconstruction_mean), img, eps, margin);
				is_equal(std::get<0>(image_reconstruction_median), img, eps, margin);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Greedy k-center clustering (similarity invariant distance)",
				   "[greedy_k_center][similarity_invariant_distance]", float)
{
	GIVEN("A set of images containing similar and non similar images.")
	{
		const auto patches = data_similar::clustering();
		const auto solution = data_similar::clustering_solution();
		const auto label_count = solution.size();
		const auto first_label = solution.at(0);

		WHEN("Greedy k-center clustering is applied.")
		{
			sim_inv_dist dist{};
			const auto labels_indices =
				dist.greedy_k_center(patches, label_count, first_label, default_params());
			const auto& labels = std::get<0>(labels_indices);
			const auto& indices = std::get<1>(labels_indices);

			THEN("Non similar images are picked.")
			{
				for(size_t i = 0; i < label_count; i++)
				{
					CHECK(indices.at(i) == solution.at(i));
				}

				const auto solution_patches = copy(patches, indices);
				constexpr auto eps = 0.0;
				constexpr auto margin = 0.0;
				is_equal(labels, solution_patches, eps, margin);
			}
		}
	}
}

TEST_CASE("Similarity invariant distance (benchmark)",
		  "[similarity_invariant_distance][!benchmark]")
{
	const auto patches = rand_patches(PATCH_COUNT_BENCHMARK, PATCH_SIZE_BENCHMARK, BENCHMARK_T{});
	const auto labels = rand_patches(LABEL_COUNT_BENCHMARK, PATCH_SIZE_BENCHMARK, BENCHMARK_T{});
	sim_inv_dist dist{};

	BENCHMARK("Distance matrix")
	{
		return dist.distance_matrix(patches, labels);
	};

	BENCHMARK("Greedy k-center clustering")
	{
		return dist.greedy_k_center(patches, LABEL_COUNT_BENCHMARK.value());
	};

	BENCHMARK("Reconstruction (mean)")
	{
		return dist.reconstruct(patches, labels, IMG_SIZE_BENCHMARK, rec_t::mean);
	};
}