

















Get the rotation matrix from euler's angles

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
















The camera model

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














.. rubric:: Methods

.. autosummary::
   :toctree:

   get_calibration_matrix
   get_perspective_projection_matrix
   project

