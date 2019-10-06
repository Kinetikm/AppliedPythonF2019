#!/usr/bin/env python
# coding: utf-8

from __future__ import division
import numpy as np
from copy import deepcopy


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
        self._rows = [0]
        self._data = []
        self._cols = []
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            i, j, data = init_matrix_representation
            m = max(i) + 1
            n = max(j) + 1
            initial_np_matrix = np.zeros((m, n))
            for k in range(len(data)):
                initial_np_matrix[i[k], j[k]] = data[k]
            self.__init_from_nparray(initial_np_matrix)
        elif isinstance(init_matrix_representation, np.ndarray):
            self.__init_from_nparray(init_matrix_representation)
        elif init_matrix_representation is None:
            pass
        else:
            raise ValueError
        self._nnz = len(self._data)

    def __init_from_nparray(self, nparray):
        m, n = nparray.shape
        for i in range(m):
            self._rows.append(self._rows[-1])
            for j in range(n):
                if nparray[i][j]:
                    self._data.append(nparray[i][j])
                    self._cols.append(j)
                    self._rows[i+1] += 1

    def get_rows(self):
        return self._rows

    def get_cols(self):
        return self._cols

    def get_data(self):
        return self._data

    @classmethod
    def empty_matrix(cls, m):
        return cls(np.zeros((m, 1)))

    def __getitem__(self, coord):
        x, y = coord
        prev_row_values_count = self._rows[x]
        curr_row_values_count = self._rows[x+1]
        for i in range(prev_row_values_count, curr_row_values_count):
            if self._cols[i] == y:
                return self._data[i]
        return 0.

    nnz = property()

    @nnz.setter
    def nnz(self, value):
        if value != len(self._data):
            raise AttributeError
        self._nnz = value

    @nnz.getter
    def nnz(self):
        return self._nnz

    def __setitem__(self, coord, value):
        i, j = coord
        if value and self[coord]:
            k = self._cols.index(j, self._rows[i], self._rows[i + 1])
            self._data[k] = value
        elif value and not self[coord]:
            try:
                k = self._cols.index(j, self._rows[i], self._rows[i + 1])
            except ValueError:
                self._data.insert(self._rows[i + 1], value)
                self._cols.insert(self._rows[i + 1], j)
            else:
                self._data.insert(k, value)
                self._cols.insert(k, j)
            for k in range(i + 1, len(self._rows)):
                self._rows[k] += 1
            self._nnz += 1
        elif self[coord]:
            k = self._cols.index(j, self._rows[i], self._rows[i + 1])
            self._data.pop(k)
            self._cols.pop(k)
            for p in range(i + 1, len(self._rows)):
                self._rows[p] -= 1
            self._nnz -= 1

    def _binary_operator(self, other, command):
        m = len(self._rows) - 1
        result = CSRMatrix.empty_matrix(m)
        for i in range(1, len(self._rows)):
            for j in self._cols[self._rows[i-1]:self._rows[i]]:
                result[i-1, j] = self[i-1, j]
        for i in range(1, len(other.get_rows())):
            for j in other.get_cols()[other.get_rows()[i - 1]:other.get_rows()[i]]:
                if command == 'add':
                    result[i - 1, j] += other[i-1, j]
                elif command == 'sub':
                    result[i-1, j] -= other[i-1, j]
        return result

    def __add__(self, other):
        return self._binary_operator(other, 'add')

    def __sub__(self, other):
        return self._binary_operator(other, 'sub')

    def __mul__(self, other):
        m = len(self._rows) - 1
        result = CSRMatrix.empty_matrix(m)
        if isinstance(other, CSRMatrix):
            for i in range(1, len(self._rows)):
                for j in self._cols[self._rows[i - 1]:self._rows[i]]:
                    result[i - 1, j] = self[i - 1, j] * other[i - 1, j]
        else:
            for i in range(1, len(self._rows)):
                for j in self._cols[self._rows[i - 1]:self._rows[i]]:
                    result[i - 1, j] = self[i - 1, j] * other
        return result

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        return self * (1 / other)

    def __matmul__(self, other):
        return CSRMatrix(self.to_dense() @ other.to_dense())

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        m = len(self._rows) - 1
        n = max(self._cols) + 1
        result = np.zeros((m, n))
        for i in range(m):
            for j in range(self._rows[i], self._rows[i + 1]):
                result[i][self._cols[j]] = self._data[j]
        return result
