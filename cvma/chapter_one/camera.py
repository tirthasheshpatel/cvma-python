"""The Camera Module used to create camera models

As the book goes, we can create a camera with a total of 11
intrinsic and extrinsic parameters. If some parameters are not
available, you can make them variable and change them during the
calibration process.
"""

import numpy as np

def get_rotation_matrix(rotation_angles):
    """Get the rotation matrix from euler's angles

    Parameters
    -----
    rotation_angles: array-like or list
        Three euler angles in the order [sai, theta, phi] where
        sai = rotation along the x-axis
        theta = rotation along the y-axis
        phi = rotation along the z-axis
    
    Returns
    -----
    A rotation matrix of shape (3, 3)

    Refrences
    -----
    Computing Euler angles from a rotation matrix by Gregory G. Slabaugh
    https://www.gregslabaugh.net/publications/euler.pdf
    """
    sai = rotation_angles[0] # s
    theta = rotation_angles[1] # t
    phi = rotation_angles[2] # p
    # find all the required sines and cosines
    cs = np.cos(sai)
    ct = np.cos(theta)
    cp = np.cos(phi)
    ss = np.sin(sai)
    st = np.sin(theta)
    sp = np.sin(phi)
    # contruct the rotation matrix along the x-axis
    rotation_matrix = np.array([
        [ct*cp, ss*st*cp-cs*sp, cs*st*cp+ss*sp],
        [ct*sp, ss*st*sp+cs*cp, cs*st*sp-ss*cp],
        [  -st,          sp*ct,          cp*ct]
    ])
    return rotation_matrix

class Camera(object):
    """The camera model

    Parameters
    -----
    alpha: float
        The intrinsic magnification parameter along the x-axis
    
    beta: float
        The intrinsic magnification parameter along the y-axis
    
    x0: float
        X-axis component of the offset of camera's origin from
        the normalized image plane
    
    y0: float
        Y-axis component of the offset of camera's origin from
        the normalized image plane
    
    theta: float
        The skewness of the camera
    
    rotation_matrix: array-like of shape (3, 3)
        Rotation matrix to tranform a point in the world co-ordinate plane
        to a point in the camera co-ordinate frame. This should only be specified
        if the euler's angles are not specified under the parameter `rotation_angles`

    rotation_angles: array-like or list
        Three euler angles in the order [sai, theta, phi] where
        sai = rotation along the x-axis
        theta = rotation along the y-axis
        phi = rotation along the z-axis
        This should only be specified if the rotation_matrix is not specified
    
    translation_vector: array-like of shape (3, ), optional
        The translation vector used to translate from world co-ordinate system
        to the camera co-ordinate system. If None, it falls to the default zero vector
    """

    __slots__ = (
        "_alpha", "_beta",
        "_x0", "_y0",
        "_theta",
        "_r1", "_r2", "_r3",
        "__rotation_angles",
        "_t1", "_t2", "_t3",
        "_calibration_matrix",
        "_perspective_projection_matrix"
    )

    def __init__(
        self,
        alpha, beta,
        x0, y0,
        theta,
        rotation_matrix=None,
        rotation_angles=None,
        translation_vector=None
    ):
        self._alpha = alpha
        self._beta = beta
        self._x0 = x0
        self._y0 = y0
        self._theta = theta
        if rotation_angles is not None and rotation_matrix is not None:
            raise ValueError("conflicting inputs: `rotation_matrix` and `rotation_angles`")
        elif rotation_angles is not None:
            rotation_matrix = get_rotation_matrix(rotation_angles)
            self.__rotation_angles = rotation_angles
        else:
            raise AttributeError("no attribute explaining rotation to translate to the camera co-ordinate frame from the world co-ordinate frame.")
        self._r1 = rotation_matrix[0, :].reshape(-1, 1)
        self._r2 = rotation_matrix[1, :].reshape(-1, 1)
        self._r3 = rotation_matrix[2, :].reshape(-1, 1)
        if translation_vector is None:
            translation_vector = np.zeros(3)
        translation_vector = np.asarray(translation_vector).reshape(-1,)
        self._t1 = translation_vector[0]
        self._t2 = translation_vector[1]
        self._t3 = translation_vector[2]
    
    def get_calibration_matrix(self):
        """Get the calibration matrix of the camera
        
        Returns
        -----
        Calibration matrix of the camera
        """
        if self._calibration_matrix is not None:
            return self._calibration_matrix
        return self._build_calibration_matrix()
    
    def get_perspective_projection_matrix(self):
        """Get the full perspective projection matrix

        Returns
        -----
        Perspective projection matrix
        """
        if self._perspective_projection_matrix is not None:
            return self._perspective_projection_matrix
        return self._build_perspective_projection_matrix()

    def _project(self, w_point):
        if self._perspective_projection_matrix is None:
            self._build_perspective_projection_matrix()

        m1 = self._perspective_projection_matrix[0, :]
        m2 = self._perspective_projection_matrix[1, :]
        m3 = self._perspective_projection_matrix[2, :]

        x = np.inner(m1, w_point) / np.inner(m3, w_point)
        y = np.inner(m2, w_point) / np.inner(m3, w_point)

        return np.array([x, y]).reshape(*w_point.shape)
