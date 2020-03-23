
Utilities for CVMA module

This module contains the common helper functions often encountered while doing
Computer Vision.
















Convert a vector or matrix to its homogeneous form.

Converts a vector [x1, x2, ..., xn] to [x1, x2, ..., xn, 1]
Converts a matrix
[[x11, x12, ..., x1n],
 [x21, x22, ..., x2n],
 ...
 [xm1, xm2, ..., xmn]]
to
[[x11, x12, ..., x1n, aux1],
 [x21, x22, ..., x2n, aux2],
 ...
 [xm1, xm2, ..., xmn, auxm],
 [  0,   0, ...,   0,    1]]
where matrix_auxilary_entries = [aux1, aux2, ..., auxm]

:Parameters:

    **data: array-like of shape (m, ) or (m, n)**
        The vector or matrix to be converted into its homogeneous form

    **matrix_auxilary_entries: array-like of shape (m, )**
        The auxilary entries of the last column of transformed matrix

:Returns:

    Transformed vector or matrix to its homogeneous form
        ..








.. rubric:: Notes

Arrays of shape (m, ), (m, 1), and (1, m) are considered equivalent.
Note also that the dtype of data is only considered during transformation
If the dtype of matrix_auxilary_entries doesn't match with the data than it
will be typecasted to the dype of data. In case a failure, an exeception is
thrown.


.. rubric:: Examples

>>> import cvma.utils
>>> import numpy as np
>>> v = [0., 0.]
>>> cvma.utils.to_homogeneous(v)
array([0., 0., 1.])
>>> rotation_matrix = np.array([[1., 0.], [0., 1.]])
>>> transition_vector = np.array([2., 1.])
>>> transformation_matrix = cvma.utils.to_homogeneous(rotation_matrix, transition_vector)
array([[1., 0., 2.],
       [0., 1., 1.],
       [0., 0., 1.]])



