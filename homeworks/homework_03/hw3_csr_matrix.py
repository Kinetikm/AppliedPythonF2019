#!/usr/bin/env python
# coding: utf-8


import numpy as np


class CSRMatrix:
    """
    CSR (2D) matrix.
    Here you can read how CSR sparse matrix works: https://en.wikipedia.org/wiki/Sparse_matrix

    Must be implemented:
    1. Getting and setting element by indexes of row and col.
    a[i, j] = v -- set value in i-th row and j-th column to value
    b = a[i, j] -- get value from i-th row and j-th column
    2. Pointwise operations.
    c = a + b -- sum of two CSR matrix of the same shape
    c = a - b -- difference --//--
    c = a * b -- product --//--
    c = alpha * a -- product of scalar alpha and CSR matrix a
    c = a / alpha -- divide CSR matrix a by nonzero scalar alpha
    3. Scalar product
    c = a.dot(b) -- matrix multiplication if shapes match
    c = a @ b --//--
    4. nnz attribute -- number of nonzero elements in matrix
    """

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: can be usual dense matrix
        or
        (row_ind, col_ind, data) tuple with np.arrays,
            where data, row_ind and col_ind satisfy the relationship:
            a[row_ind[k], col_ind[k]] = data[k]
        """
        self._A = None
        self._IA = None
        self._JA = None

        raise NotImplementedError

        # if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
        #     for idx, data_el in enumerate(init_matrix_representation[2]):
        #         i = init_matrix_representation[idx]
        #         j = init_matrix_representation[idx]
        #         self[i, j] = data_el
        # elif isinstance(init_matrix_representation, np.ndarray):
        #     # print("init:", init_matrix_representation)
        #     # print("size:", init_matrix_representation.shape)
        #     for i in range(init_matrix_representation.shape[0]):
        #         for j in range(init_matrix_representation.shape[1]):
        #             self[i, j] = init_matrix_representation[2][i, j]
        # else:
        #     raise ValueError

        return

    def __matmul__(self, other):
        pass

    def __add__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __getitem__(self, key):
        print("getting:", key)
        return

    def __setitem__(self, key, value):
        print("assigment:", key, value)
        return

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        pass
