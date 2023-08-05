Invariant patch distances and clustering
========================================

This package includes methods for clustering patches and reconstructing images using invariant patch distances.
The package is build upon the CUDA C++ project: `invariant_patch_distances <https://gitlab.com/a.schulze/invariant_patch_distances>`_.
The package has the following dependencies: an NVIDIA graphics card of compute capability 3.x or higher,
CUDA 10.0 and CMake 3.10.

Example
-------

The following example shows how to cluster patches and reconstruct an image using these clusters.

.. code:: python

    import patchdistances as pd

    # Load image as Float32 numpy array. It can either be gray-scale or rgb.
    img = load_image()

    // Initialize the distance class.
    // Alternatively: similarity_inv_dist.
    aid = pd.affine_inv_dist()

    // Greedy-k-center clustering of the image patches using the distance.
    labels, indices_of_labels = aid.greedy_k_center(
        image=img,
        patch_shape=(7,7),
        clusters=20,
        first_patch_idx=0,
        solver=pd.solver_t.procrustes,
        func_family=pd.func_t.superlevelsets,
        use_imed=False,
        interpolation=pd.inter_t.bicubic,
    )

    // Reconstruct the image using the previously clustered patches.
    // Alternatively: reconstruct_w_translation.
    reconstructed_image, nearest_neighbor_labeling = aid.reconstruct(
        image=img,
        labels=labels,
        rec_type=pd.rec_t.Median,
        solver=pd.solver_t.procrustes,
        func_family=pd.func_t.superlevelsets,
        use_imed=False,
        interpolation=pd.inter_t.bicubic,
    )