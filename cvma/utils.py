import numpy as np

__all__ = ["to_homogeneous"]


def to_homogeneous(data, matrix_auxilary_entries=None):
    """Convert a vector or matrix to its homogeneous form

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

    Parameters
    -----
    data: array-like of shape (m, ) or (m, n)
        The vector or matrix to be converted into its homogeneous form
    
    matrix_auxilary_entries: array-like of shape (m, )
        The auxilary entries of the last column of transformed matrix
    
    Returns
    -----
    Transformed vector or matrix to its homogeneous form

    Note
    -----
    Arrays of shape (m, ), (m, 1), and (1, m) are considered equivalent.
    Note also that the dtype of data is only considered during transformation
    If the dtype of matrix_auxilary_entries doesn't match with the data than it
    will be typecasted to the dype of data. In case a failure, an exeception is
    thrown.
    """
    data = np.asarray(data)

    if len(data.shape) == 1 or (data.shape[1] == 1 or data.shape[0] == 1):
        if len(data.shape) == 1:
            expected_shape = (data.shape[0] + 1,)
        elif data.shape[0] == 1:
            expected_shape = (1, data.shape[1] + 1)
        elif data.shape[1] == 1:
            expected_shape = (data.shape[0] + 1, 1)

        data = data.reshape(-1,)
        res = np.concatenate((data, [1]))

        return res.reshape(expected_shape)
    else:
        m = data.shape[0]
        n = data.shape[1]
        dtype = data.dtype

        if matrix_auxilary_entries is None:
            matrix_auxilary_entries = np.zeros(m, dtype=dtype)
        else:
            matrix_auxilary_entries = np.asarray(matrix_auxilary_entries)
        if matrix_auxilary_entries.size != m:
            raise ValueError(
                f"bad matrix_auxilary_entries size: {matrix_auxilary_entries.size} != {m}"
            )
        else:
            matrix_auxilary_entries = matrix_auxilary_entries.reshape(-1,)

        res = np.empty((m + 1, n + 1), dtype=dtype)
        res[:m, :n] = data
        res[:m, n] = matrix_auxilary_entries
        res[m, :n] = np.zeros(n, dtype=dtype)
        res[m, n] = 1

        return res
