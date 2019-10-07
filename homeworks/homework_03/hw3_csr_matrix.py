#!/usr/bin/env python
# coding: utf-8
from typing import List

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
            l = []
            for i in range(3):
                l.append(len(init_matrix_representation[i]))
            if l[0] == l[1] == l[2]:
                rows = max(init_matrix_representation[0])
                self.a = []
                self.ia = [0] * (rows + 2)
                self.ja = []
                for i in range(l[0]):
                    if init_matrix_representation[2][i] != 0:
                        self.a.append(init_matrix_representation[2][i])
                        self.ja.append(init_matrix_representation[1][i])
                        for j in range(init_matrix_representation[0][i], rows + 1):
                            self.ia[j + 1] += 1
            else:
                raise ValueError
        elif isinstance(init_matrix_representation, np.ndarray):
            self.cols = len(init_matrix_representation[0])
            self.rows = len(init_matrix_representation)
            self.a = []
            self.ia = [0] * (self.rows + 1)
            self.ja = []
            for i in range(len(init_matrix_representation)):
                if len(init_matrix_representation[i]) == self.cols:
                    for j in range(self.cols):
                        if init_matrix_representation[i][j] != 0:
                            self.a.append(init_matrix_representation[i][j])
                            self.ja.append(j)
                            for k in range(i, self.rows):
                                self.ia[k + 1] += 1
        else:
            raise ValueError

    @property
    def nnz(self):
        return self.ia[len(self.ia) - 1]

    def __getitem__(self, item):
        row = item[0]
        col = item[1]
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.ia[row + 1] != self.ia[row]:
                for pointer in range(self.ia[row], self.ia[row + 1]):
                    if col == self.ja[pointer]:
                        return self.a[pointer]
                return 0
            else:
                return 0
        else:
            raise IndexError

    def __setitem__(self, key, value):
        row = key[0]
        col = key[1]
        if 0 <= row < self.rows and 0 <= col < self.cols:
            for i in range(self.ia[row], self.ia[row + 1]):
                if self.ja[i] == col:
                    if value != 0:
                        self.a[i] = value
                    else:
                        del self.ja[i]
                        del self.a[i]
                        for j in range(row, self.rows):
                            self.ia[j + 1] -= 1
                    return
            if value != 0:
                self.ja.insert(self.ia[row], col)
                self.a.insert(self.ia[row], value)
                for i in range(row, self.rows):
                    self.ia[i + 1] += 1
            else:
                del self.ja[row]
                del self.a[row]
                for j in range(row, self.rows):
                    self.ia[j + 1] -= 1
        else:
            raise IndexError

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        dense = np.zeros((self.rows, self.cols))
        pointer = 0
        for i in range(self.rows):
            while pointer < self.ia[i + 1]:
                dense[i, self.ja[pointer]] = self.a[pointer]
                pointer += 1
        return dense

