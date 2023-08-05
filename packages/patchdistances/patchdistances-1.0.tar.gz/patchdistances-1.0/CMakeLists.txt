cmake_minimum_required(VERSION 3.10 FATAL_ERROR)
project(pd LANGUAGES CXX CUDA)

include(CTest)

set(pd_inc
  include/affine_inv_dist.h
  include/Cols.h
  include/determinant.h
  include/device_matrix.h
  include/device_patches.h
  include/enums.h
  include/extract_patches.h
  include/greedy_k_center.h
  include/identity_solver.h
  include/imed.h
  include/least_squares_solver.h
  include/local_nearest_neighbor.h
  include/log_polar_transform.h
  include/math.h
  include/metric.h
  include/nearest_neighbor.h
  include/partition_NA.h
  include/patch_index.h
  include/pimpl.h
  include/procrustes_solver.h
  include/quickselect.h
  include/rec_image.h
  include/Rows.h
  include/sample.h
  include/sim_inv_dist.h
  include/Size.h
  include/strided_range.h
  include/type_traits.h
  include/unique_cublas_handle.h
  include/unique_cufft_plan.h
  include/utils.h
  include/vec3.h
  include/warp_perspective.h
  src/affine_inv_dist_impl.h
  src/affine_inv_dist.cu
  src/determinant.cu
  src/extract_patches.cu
  src/identity_solver.cu
  src/imed.cu
  src/least_squares_solver.cu
  src/local_nearest_neighbor.cu
  src/log_polar_transform.cu
  src/nearest_neighbor.cu
  src/pimpl_impl.h
  src/procrustes_solver.cu
  src/rec_image.cu
  src/sim_inv_dist_impl.h
  src/sim_inv_dist.cu
  src/warp_perspective.cu
)

set(pd_py_inc
  include/pimpl.h
  src/pimpl_impl.h
  py_bindings/affine_inv_dist_py.cu
  py_bindings/affine_inv_dist_py.h
  py_bindings/core_py.cu
  py_bindings/core_py.h
  py_bindings/sim_inv_dist_py.cu
  py_bindings/sim_inv_dist_py.h
  py_bindings/utils.cu
  py_bindings/utils.h
)

set(pd_tests_inc
  unit_tests/debug.h
  unit_tests/data_affine.cu
  unit_tests/data_affine.h
  unit_tests/data_afmt.cu
  unit_tests/data_afmt.h
  unit_tests/data_orthogonal.cu
  unit_tests/data_orthogonal.h
  unit_tests/data_similar.cu
  unit_tests/data_similar.h
  unit_tests/data_reconstruction.cu
  unit_tests/data_reconstruction.h
  unit_tests/tests_affine_inv_dist.cu
  unit_tests/tests_extract_patches.cu
  unit_tests/tests_identity_solver.cu
  unit_tests/tests_imed.cu
  unit_tests/tests_least_squares_solver.cu
  unit_tests/tests_local_nearest_neighbor.cu
  unit_tests/tests_log_polar_transform.cu
  unit_tests/tests_main.cpp
  unit_tests/tests_nearest_neighbor.cu
  unit_tests/tests_partition_NA.cu
  unit_tests/tests_procrustes_solver.cu
  unit_tests/tests_quickselect.cu
  unit_tests/tests_rec_image.cu
  unit_tests/tests_sample.cu
  unit_tests/tests_sim_inv_dist.cu
  unit_tests/tests_utils.cu
  unit_tests/tests_vec3.cu
  unit_tests/tests_warp_perspective.cu
  unit_tests/utils.cu
  unit_tests/utils.h
)

include_directories(SYSTEM extern extern/pybind11/include/pybind11)

if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  set(cuda_libs cufft cublas cublasLt nppc nppig cudart_static)
  set(warnings "/W3")
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
  set(cuda_libs -lcublasLt_static -lcublas_static -lcufft_static_nocallback
                -llapack_static -lculibos -lcudart_static -lpthread -ldl -lcublasLt_static)
                # cublaslLT_static needs to be linked twice
  set(warnings "-Werror -Wall -Wextra -Wduplicated-cond -Wduplicated-branches -Wlogical-op \
              -Wrestrict -Wnull-dereference -Wformat-signedness -Wodr -Wredundant-decls -Wcast-align \
              -Wmissing-include-dirs -Wswitch-enum -Wswitch-default -Wredundant-decls \
              -Wmissing-format-attribute -Wformat-nonliteral -Wconversion -Wpointer-arith \
              -Wsequence-point -Wparentheses")
endif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")

set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} \
  -gencode arch=compute_30,code=[compute_30] \
  -gencode arch=compute_60,code=[compute_60] \
  -Xcudafe \"--diag_suppress=unsigned_compare_with_zero\" \
	-Xcudafe \"--diag_suppress=decl_modifiers_ignored\" \
  -Xcudafe \"--diag_suppress=2803\" \
  -Xcompiler \"${warnings}\" \
  -expt-extended-lambda"
) # The choice of virtual architecture is based on atomicAddBlock used in affine_inv_dist_impl.h.

#
## static library
#
add_library(pd_static STATIC ${pd_inc})
target_compile_features(pd_static PRIVATE cxx_std_14)
set_target_properties(pd_static PROPERTIES POSITION_INDEPENDENT_CODE ON)

if(APPLE)
  set_property(TARGET pd_static PROPERTY BUILD_RPATH ${CMAKE_CUDA_IMPLICIT_LINK_DIRECTORIES})
endif(APPLE)

#
## python bindings
#
add_library(pd_py_static STATIC ${pd_py_inc})
find_package(PythonLibs REQUIRED)
target_include_directories(pd_py_static PRIVATE ${PYTHON_INCLUDE_DIRS})
target_compile_features(pd_py_static PRIVATE cxx_std_14)
set_target_properties(pd_py_static PROPERTIES POSITION_INDEPENDENT_CODE ON)

if(MSVC)
  set(PYBIND11_CPP_STANDARD /std:c++17)
else()
  set(PYBIND11_CPP_STANDARD -std=c++17)
endif()

# The module name must coincide with the name in py_bindings/py_bindings.cpp!
add_subdirectory(extern/pybind11)
pybind11_add_module(patchdistances py_bindings/py_bindings.cpp)
target_compile_features(patchdistances PRIVATE cxx_std_17)
target_link_libraries(patchdistances PRIVATE pd_py_static pd_static ${cuda_libs})

#
## unit tests
#
add_subdirectory(extern/Catch2)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/extern/Catch2/contrib")
include(Catch)

add_executable(pd_tests ${pd_tests_inc})

catch_discover_tests(pd_tests WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/unit_tests")

target_compile_features(pd_tests PRIVATE cxx_std_14)
set_target_properties(pd_tests PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
set_target_properties(pd_tests PROPERTIES POSITION_INDEPENDENT_CODE ON)
target_link_libraries(pd_tests PRIVATE pd_static ${cuda_libs} Catch2::Catch2)