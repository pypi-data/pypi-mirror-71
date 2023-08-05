/*! \file local_nearest_neighbor.h
	\brief Local nearest neighbor for distance matrices.
*/

#include <thrust/pair.h>

#include <cstddef>

template<typename T>
class device_matrix;

class Size;

//! Struct which defines a labeling of image pixels by patches.
/*!
 * Each pixel is assigned a label (patch/ atom) and an offset for this label (translation).
 * Additionally, the pixel index which corresponds to the offset is provided.
 */
struct labeling
{
	//! Point or offset; (x,y).
	using point = thrust::pair<int, int>;

	//! Assigned label to each pixel.
	device_matrix<size_t> labels;
	//! Index of image patches corresponding to the offsets.
	device_matrix<size_t> patches;
	//! Offset of the label for each pixel.
	device_matrix<point> offsets;
};

//! A function that computes the nearest neighbor labeling, but also considers translation of
//! the labels around the center pixel of each image patch.
/*!
 * \param i_dist_mat Distance matrix of image patches and labels.
 * \param i_patches_shape Total number of patches (rows of i_dist_mat) shaped as they appear in the
 * image.
 * \param i_patch_size Size of the image patches, which were used to compute i_dist_mat. Must be
 * uneven.
 * \return Struct with the label index for each image patch, the image patch index for each image
 * patch corresponding to the nearest neighbor in the neighborhood and the offsets for each image
 * patch. See also best_patches struct.
 */
labeling local_nearest_neighbor(const device_matrix<double>& i_dist_mat,
								const Size& i_patches_shape, const Size& i_patch_size);