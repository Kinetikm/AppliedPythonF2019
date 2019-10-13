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
        self._a = None
        self._ia = None
        self._ja = None

        self.shape = None

        print("init_matrix_representation", init_matrix_representation)

        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            for i in range(1, 3):
                assert len(init_matrix_representation[0]) == len(init_matrix_representation[i])

            self.shape = (max(init_matrix_representation[0])+1, max(init_matrix_representation[1])+1)

            for idx, data_el in enumerate(init_matrix_representation[2]):
                if data_el == 0:
                    continue
                i = init_matrix_representation[0][idx]
                j = init_matrix_representation[1][idx]
                self[i, j] = data_el
        elif isinstance(init_matrix_representation, np.ndarray):
            print("init:", init_matrix_representation)
            print("size:", init_matrix_representation.shape)
            for i in range(init_matrix_representation.shape[0]):
                for j in range(init_matrix_representation.shape[1]):
                    self[i, j] = init_matrix_representation[2][i, j]
        else:
            raise ValueError

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
        if key[0] > self.shape[0] - 1 or key[1] > self.shape[1]:
            raise KeyError
        if value == 0 and self[key] == 0:
            return

        


        return

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        pass
