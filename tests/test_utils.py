"""Test Suite for utilities.

To add new tests, please use @pytest.mark.parametrize for passing
paramters to the tests. Refrain from using fixtures or other unit test
style.
"""

import numpy as np
from cvma.utils import to_homogeneous
import pytest


@pytest.mark.parametrize(
    "data, matrix_aux_entries",
    [
        (np.array([1, 2]), None),
        (np.array([[1.0, 2.0]]), None),
        (np.array([[1.0], [2.0]]), None),
        (np.array([[1.0, 2.0], [3.0, 4.0]]), None),
        (np.array([[1.0, 2.0], [3.0, 4.0]]), [20.0, 1.0]),
    ],
)
def test_to_homogeneous(data, matrix_aux_entries):
    res = to_homogeneous(data, matrix_aux_entries)
    assert res.dtype == data.dtype


def test_to_homogeneous_bad_input():
    data = np.array([[1, 2], [3, 4]])
    matrix_auxilary_entries = np.array([[1, 2, 3, 4]])
    with pytest.raises(ValueError, match=r"bad matrix_auxilary_entries"):
        to_homogeneous(data, matrix_auxilary_entries)
