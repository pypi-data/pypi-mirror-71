import sys
sys.path.insert(1, '../build')

import numpy as np
import patchdistances as pd
import pytest

def test_grey_matrix():
    A = np.random.rand(40, 20).astype('float32')
    assert np.array_equal(pd.identity(A), A)

def test_rgb_matrix():
    A = np.random.rand(40, 20, 3).astype('float32')
    assert np.array_equal(pd.identity(A), A)

def test_grey_patches():
    A = np.random.rand(10, 40, 20).astype('float32')
    assert np.array_equal(pd.identity(A), A)

def test_rgb_patches():
    A = np.random.rand(10, 40, 20, 3).astype('float32')
    assert np.array_equal(pd.identity(A), A)

def test_not_matrix_nor_patches():
    with pytest.raises(RuntimeError):
        A = np.random.rand(10, 40, 20, 10).astype('float32')
        pd.identity(A)