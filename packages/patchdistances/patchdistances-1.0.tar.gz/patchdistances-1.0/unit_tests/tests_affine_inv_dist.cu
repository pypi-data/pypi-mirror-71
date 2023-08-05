#define CATCH_CONFIG_ENABLE_BENCHMARKING

#include "../extern/Catch2/single_include/catch2/catch.hpp"
#include "../include/affine_inv_dist.h"
#include "../include/device_patches.h"
#include "../include/enums.h"
#include "../include/extract_patches.h"
#include "../src/affine_inv_dist_impl.h"
#include "data_affine.h"
#include "data_orthogonal.h"
#include "data_reconstruction.h"
#include "utils.h"

#include "../extern/gsl/gsl_util"

constexpr aid_params procrustes()
{
	auto params = aid_params{};
	params.solver = solver_t::procrustes;
	params.func_family = func_family_t::clip;
	params.levels = 4;
	params.higher_order_moments = false;
	params.imed = false;
	params.interpolation = interpolation_t::nn;

	return params;
}

constexpr aid_params least_squares()
{
	auto params = aid_params{};
	params.solver = solver_t::least_squares;
	params.func_family = func_family_t::clip;
	params.levels = 4;
	params.higher_order_moments = false;
	params.imed = false;
	params.interpolation = interpolation_t::nn;

	return params;
}

TEMPLATE_TEST_CASE("Image moments T", "[affine_invariant_distance]", float, double)
{
	using T = TestType;

	GIVEN("a set of patches")
	{
		const auto patches_first = data_orthogonal::patches_rhs(T{});
		const auto patches_high = data_orthogonal::patches_rhs(T{});

		const auto high_order_moments = true;
		const auto solution_first = data_orthogonal::moments_clip_rhs(T{}, !high_order_moments);
		const auto solution_high = data_orthogonal::moments_clip_rhs(T{}, high_order_moments);

		WHEN("the image moments are computed")
		{
			const auto ff = func_family_t::clip;
			const auto levels = gsl::narrow<uint>(solution_first.rows_patches());
			const auto T_first = image_moments(patches_first, ff, levels, !high_order_moments);
			const auto T_high = image_moments(patches_high, ff, levels, high_order_moments);

			THEN("they equal the known solution")
			{
				constexpr auto eps = 0.0;
				constexpr auto margin = 0.01;
				is_equal(T_first, solution_first, eps, margin);
				is_equal(T_high, solution_high, eps, margin);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Tile", "[affine_invariant_distance]", float, double)
{
	using T = TestType;

	GIVEN("a vector")
	{
		const auto tiles = size_t{10};
		const auto tile_size = 100;
		const auto input = [&] {
			auto tmp = std::vector<T>(tile_size);
			std::iota(tmp.begin(), tmp.end(), 0.0);
			return thrust::device_vector<T>(tmp);
		}();
		const auto solution = [&] {
			auto tmp = thrust::device_vector<T>{};
			for(size_t i = 0; i < tiles; i++)
			{
				tmp.insert(tmp.end(), input.cbegin(), input.cend());
			}
			return tmp;
		}();
		auto result = thrust::device_vector<T>(solution.size());

		WHEN("tiled")
		{
			tile(input.cbegin(), input.cend(), result.begin(), tiles);

			THEN("it equals the result")
			{
				const auto mat_solution = device_matrix<T>{solution, Rows{tiles}, Cols{tile_size}};
				const auto mat_result = device_matrix<T>{result, Rows{tiles}, Cols{tile_size}};

				constexpr auto eps = 0.0;
				constexpr auto margin = 0.0;
				is_equal(mat_result, mat_solution, eps, margin);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Distance matrix (orthogonal matrix) (affine invariant distance)",
				   "[affine_invariant_distance]", float, double, vec3<float>, vec3<double>)
{
	GIVEN("A set of rotated images (embedded in a homogeneous background)")
	{
		const auto patches0 = data_orthogonal::patches_lhs(TestType{});
		const auto patches1 = data_orthogonal::patches_rhs(TestType{});

		WHEN("the affine invariant distance is computed")
		{
			affine_inv_dist dist{};
			const auto dist_mat_l = dist.distance_matrix(patches0, patches1, least_squares());
			const auto dist_mat_p = dist.distance_matrix(patches0, patches1, procrustes());

			THEN("it is ~0")
			{
				constexpr auto margin_low = 0.0;
				constexpr auto margin_high = 1.0;
				data_orthogonal::distance_matrix(dist_mat_l, margin_low, margin_high);
				data_orthogonal::distance_matrix(dist_mat_p, margin_low, margin_high);
			}
		}
	}
}

TEST_CASE("Distance matrix (affine matrix) (affine invariant distance)",
		  "[affine_invariant_distance]")
{
	GIVEN("A set of affinely transformed images (embedded in a homogeneous background)")
	{
		const auto patches0 = data_affine::patches_lhs();
		const auto patches1 = data_affine::patches_rhs();

		WHEN("the affine invariant distance is computed")
		{
			// Non orthogonal transformation matrices can only be solved by least squares.
			affine_inv_dist dist{};
			const auto dist_mat = dist.distance_matrix(patches0, patches1, least_squares());

			THEN("it is ~0")
			{
				constexpr auto margin_low = 0.0;
				constexpr auto margin_high = 1.0;
				data_affine::distance_matrix(dist_mat, margin_low, margin_high);
			}
		}
	}
}

TEMPLATE_TEST_CASE("Distance matrix (rank deficient T) (affine invariant distance)",
				   "[affine_invariant_distance]", float, double, vec3<float>, vec3<double>)
{
	using T = TestType;

	GIVEN("A set of affinely transformed small patches (with rank deficient T)")
	{
		const auto rows = 5_rows;
		const auto cols = 5_cols;
		const auto img0_vec = std::vector<T>{
			T{1.0}, T{1.0}, T{0.0}, T{0.0}, T{0.0}, //
			T{1.0}, T{1.0}, T{0.0}, T{0.0}, T{0.0}, //
			T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
			T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
			T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
		};

		const auto img1_vec = std::vector<T>{
			T{0.0}, T{0.0}, T{0.0}, T{1.0}, T{1.0}, //
			T{0.0}, T{0.0}, T{0.0}, T{1.0}, T{1.0}, //
			T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
			T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
			T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
		};

		const auto img2_vec = std::vector<T>{
			T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
			T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
			T{0.0}, T{0.0}, T{0.0}, T{0.0}, T{0.0}, //
			T{0.0}, T{0.0}, T{0.0}, T{1.0}, T{1.0}, //
			T{0.0}, T{0.0}, T{0.0}, T{1.0}, T{1.0}, //
		};
		REQUIRE(img0_vec.size() == rows.value() * cols.value());
		REQUIRE(img1_vec.size() == rows.value() * cols.value());
		REQUIRE(img2_vec.size() == rows.value() * cols.value());

		const auto img_0 = device_patches<T>{img0_vec, patch_index{1}, rows, cols};
		const auto img_1 = device_patches<T>{img1_vec, patch_index{1}, rows, cols};
		const auto img_2 = device_patches<T>{img2_vec, patch_index{1}, rows, cols};

		const auto patches_0 = append(img_0, img_2, img_1);
		const auto patches_1 = append(img_1, img_2);

		WHEN("the affine invariant distance is computed")
		{
			// Remark: This does not work with the least squares solver.
			affine_inv_dist dist{};
			const auto dist_mat = dist.distance_matrix(patches_0, patches_1, procrustes());

			THEN("it is ~0")
			{
				REQUIRE(dist_mat.size() == Size{3_rows, 2_cols});

				CHECK(dist_mat.at(0_rows, 0_cols) == Approx{0.0}.margin(0.0));
				CHECK(dist_mat.at(1_rows, 0_cols) == Approx{0.0}.margin(0.0));
				CHECK(dist_mat.at(2_rows, 0_cols) == Approx{0.0}.margin(0.0));
				CHECK(dist_mat.at(0_rows, 1_cols) == Approx{0.0}.margin(0.0));
				CHECK(dist_mat.at(1_rows, 1_cols) == Approx{0.0}.margin(0.0));
				CHECK(dist_mat.at(2_rows, 1_cols) == Approx{0.0}.margin(0.0));
			}
		}
	}
}

TEMPLATE_TEST_CASE("Reconstruction (affine invariant distance)", "[affine_invariant_distance]",
				   float, double, vec3<float>, vec3<double>)
{
	GIVEN("an image and labels")
	{
		const auto img = data_reconstruction::image(TestType{});
		const auto labels = data_reconstruction::labels(TestType{});
		const auto patches = extract_patches(img, labels.size_patches());

		WHEN("the image is reconstructed using the labels")
		{
			// TODO: GelsBatched in least squares solver runs indefinitely on full power for this
			// problem.
			affine_inv_dist dist{};
			const auto image_reconstruction_mean =
				dist.reconstruct(patches, labels, img.size(), rec_t::mean, procrustes());
			const auto image_reconstruction_median =
				dist.reconstruct(patches, labels, img.size(), rec_t::median, procrustes());

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

TEMPLATE_TEST_CASE("Reconstruction with translation (affine invariant distance)",
				   "[affine_invariant_distance]", float, double, vec3<float>, vec3<double>)
{
	GIVEN("an image and labels")
	{
		const auto img = data_reconstruction::image(TestType{});
		const auto labels = data_reconstruction::labels(TestType{});
		const auto patches = extract_patches(img, labels.size_patches());

		WHEN("the image is reconstructed using the labels and allowing translation of labels")
		{
			// TODO: GelsBatched in least squares solver runs indefinitely on full power for this
			// 	problem.
			affine_inv_dist dist{};
			const auto image_reconstruction_mean = dist.reconstruct_w_translation(
				patches, labels, img.size(), rec_t::mean, procrustes());
			const auto image_reconstruction_median = dist.reconstruct_w_translation(
				patches, labels, img.size(), rec_t::median, procrustes());

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

// Clustering is only tested for float, because it is based on the distance matrix, which is tested
// more extensively.
TEST_CASE("Greedy k-center clustering (affine invariant distance)",
		  "[greedy_k_center][affine_invariant_distance]")
{
	GIVEN("A set of images containing affinely tranformed and non affinely transformed images.")
	{
		const auto patches = data_orthogonal::clustering();
		const auto solution = data_orthogonal::clustering_solution();
		const auto label_count = solution.size();
		const auto first_label = solution.at(0);

		WHEN("Greedy k-center clustering is applied.")
		{
			// TODO: GelsBatched in least squares solver runs indefinitely on full power for this
			// problem.
			affine_inv_dist dist{};
			const auto labels_indices =
				dist.greedy_k_center(patches, label_count, first_label, procrustes());
			const auto& labels = std::get<0>(labels_indices);
			const auto& indices = std::get<1>(labels_indices);

			THEN("Non transformed images are picked.")
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

TEST_CASE("Affine invariant distance (benchmark)", "[affine_invariant_distance][!benchmark]")
{
	const auto patches = rand_patches(PATCH_COUNT_BENCHMARK, PATCH_SIZE_BENCHMARK, BENCHMARK_T{});
	const auto labels = rand_patches(LABEL_COUNT_BENCHMARK, PATCH_SIZE_BENCHMARK, BENCHMARK_T{});
	affine_inv_dist dist{};

	BENCHMARK("Distance matrix (affine)")
	{
		return dist.distance_matrix(patches, labels);
	};

	BENCHMARK("Greedy k-center clustering (affine)")
	{
		return dist.greedy_k_center(patches, LABEL_COUNT_BENCHMARK.value());
	};

	BENCHMARK("Reconstruction (affine, mean)")
	{
		return dist.reconstruct(patches, labels, IMG_SIZE_BENCHMARK, rec_t::mean);
	};

	const auto proc = [] {
		auto tmp = aid_params{};
		tmp.solver = solver_t::procrustes;
		return tmp;
	}();

	BENCHMARK("Distance matrix (orthogonal)")
	{
		return dist.distance_matrix(patches, labels, proc);
	};

	BENCHMARK("Greedy k-center clustering (orthogonal)")
	{
		return dist.greedy_k_center(patches, LABEL_COUNT_BENCHMARK.value(), 0, proc);
	};

	BENCHMARK("Reconstruction (orthogonal, mean)")
	{
		return dist.reconstruct(patches, labels, IMG_SIZE_BENCHMARK, rec_t::mean, proc);
	};
}