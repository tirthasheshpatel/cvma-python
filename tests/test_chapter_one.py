import numpy as np
from cvma.chapter_one import Camera, get_rotation_matrix
import pytest


CAMERA_PARAMS = (
    {
        "alpha"             : 1.0,
        "beta"              : 1.0,
        "x0"                : 0.0,
        "y0"                : 0.0,
        "theta"             : np.pi / 2,
        "rotation_angles"   : [0., 0., 0.],
        "translation_vector": [0., 0., 0.]
    }
)


@pytest.mark.parametrize("angles, expected", [
    (
        [0., 0., 0.],
        np.array([
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]
        ])
    )
])
def test_get_rotation_matrix(angles, expected):
    r = get_rotation_matrix(angles)
    assert np.allclose(expected, expected)


@pytest.mark.parametrize("params, expected", [
    (
        CAMERA_PARAMS,
        np.array([
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]
        ])
    )
])
def test_camera_calibration_matrix(params, expected):
    camera = Camera(**params)
    calibration_matrix = camera.get_calibration_matrix()
    assert np.allclose(calibration_matrix, expected)


@pytest.mark.parametrize("params, expected", [
    (
        CAMERA_PARAMS,
        np.array([
            [1., 0., 0., 0.],
            [0., 1., 0., 0.],
            [0., 0., 1., 0.]
        ])
    )
])
def test_camera_perspective_projection_matrix(params, expected):
    camera = Camera(**params)
    perspective_projection_matrix = camera.get_perspective_projection_matrix()
    assert np.allclose(perspective_projection_matrix, expected)


@pytest.mark.parametrize("params", [
    CAMERA_PARAMS
])
@pytest.mark.parametrize("w_point, expected", [
    ([0., 0., 1.], [0., 0.]),
    ([0., 1., 1.], [[0., 1.]]),
    ([1., 1., 1.], [[1.], [1.]])
])
def test_camera_project(params, w_point, expected):
    camera = Camera(**params)
    c_point = camera.project(w_point)
    assert np.allclose(c_point, expected)


def test_camera_cached_calibration_matrix():
    camera = Camera(**CAMERA_PARAMS)
    calibration_matrix = camera.get_calibration_matrix()
    with pytest.warns(RuntimeWarning, match=r"using the cached matrix"):
        cached_calibration_matrix = camera.get_calibration_matrix()


def test_camera_cached_perspective_projection_matrix():
    camera = Camera(**CAMERA_PARAMS)
    perspective_projection_matrix = camera.get_perspective_projection_matrix()
    with pytest.warns(RuntimeWarning, match=r"using the cached matrix"):
        cached_perspective_projection_matrix = camera.get_perspective_projection_matrix()


@pytest.mark.parametrize("params, expected_err, expected_msg", [
    (
        {
            **CAMERA_PARAMS,
            "rotation_matrix": np.array([
                [1., 0., 0.],
                [0., 1., 0.],
                [0., 0., 1.]
            ])
        },
        ValueError,
        r"conflicting inputs"
    ),
    (
        {
            "alpha"             : 1.0,
            "beta"              : 1.0,
            "x0"                : 0.0,
            "y0"                : 0.0,
            "theta"             : np.pi / 2,
            "translation_vector": [0., 0., 0.]
        },
        AttributeError,
        r"no attribute explaining rotation"
    )
])
def test_camera_init_exceptions(params, expected_err, expected_msg):
    with pytest.raises(expected_err, match=expected_msg):
        camera = Camera(**params)
