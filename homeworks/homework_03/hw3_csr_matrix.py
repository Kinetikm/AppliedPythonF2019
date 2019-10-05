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
        (row_ind, col, data) tuple with np.arrays,
            where data, row_ind and col_ind satisfy the relationship:
            a[row_ind[k], col_ind[k]] = data[k]
        """
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self._a = []
            self._ia = [0]
            self._ja = []
            tmp = []
            for i in range(len(init_matrix_representation[0])):
                tmp.append({init_matrix_representation[0][i], init_matrix_representation[1][i], init_matrix_representation[2][i]})
            tmp.sort(key=lambda x: tmp[x][1])
            tmp.sort(key=lambda x: tmp[x][0])
            for element in tmp:
                if self._ia[-1] != element[0]:
                    tmp_i = self._ia[-1]
                    for i in range(element[0] - tmp_i):
                        self._ia.append(self._ia[tmp_j+1])
                self._a.append(element[2])
                self._ja.append(element[1])
                self._ia[-1] += 1
        elif isinstance(init_matrix_representation, np.ndarray):
            for i in range(len(init_matrix_representation)):
                for j in range(len(init_matrix_representation[i])):
                    if init_matrix_representation[i][j]:
                        self._a.append(init_matrix_representation[i][j])
                        if len(self.ia != i + 1):
                            tmp = self._a[-1]
                            for k in range(i - tmp):
                                self._ia.append(self._a[tmp])
                        self._ia[-1] += 1
                        self._ja.append(j)
        else:
            raise ValueError

    def get_a(self):
        return self._a

    def get_ia(self):
        return self._ia

    def get_ja(self):
        return self._ja

    def __add__(self, other):
        pass

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        raise NotImplementedError
