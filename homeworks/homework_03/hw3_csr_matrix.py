#!/usr/bin/env python
# coding: utf-8


import numpy as np
import copy


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
        self._a = []
        self._ia = [0]
        self._ja = []
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            _row_ind = init_matrix_representation[0]
            _col_ind = init_matrix_representation[1]
            _data = init_matrix_representation[2]
            self._a = list(_data)
            self._ja = list(_col_ind)
            _cur_nnz = 0
            for i in range(max(_row_ind) + 1):
                _cur_nnz += _row_ind.count(i)
                self._ia.append(_cur_nnz)
        elif isinstance(init_matrix_representation, np.ndarray):
            _cur_nnz = 0
            for i, item in enumerate(init_matrix_representation):
                for j, element in enumerate(item):
                    if element:
                        self._a.append(element)
                        self._ja.append(j)
                        _cur_nnz += 1
                self._ia.append(_cur_nnz)
            self._max_rows = len(init_matrix_representation)
            self._max_cols = len(init_matrix_representation[0])
        else:
            raise ValueError
        self._nnz = len(self._a)

    def __getitem__(self, indexes):
        i = indexes[0]
        j = indexes[1]
        try:
            index = self._ia[i] + self._ja[self._ia[i]:self._ia[i+1]].index(j)
            return self._a[index]
        except ValueError:
            return 0

    def __setitem__(self, indexes, value):
        i = indexes[0]
        j = indexes[1]
        if self[i, j]:
            index = self._ia[i] + self._ja[self._ia[i]:self._ia[i + 1]].index(j)
            self._a[index] = value
        else:
            if (self._ia[i] - self._ia[i+1]) != 0:
                for l, item in enumerate(self._ja[self._ia[i]:self._ia[i+1]]):
                    if item > j:
                        index = self._ia[i] + l
                        self._ja.insert(index, j)
                        self._a.insert(index, value)
                        self._ia[i+1:] = list(map(lambda x: x + 1, self._ia[i+1:]))
                        break
            else:
                index = self._ia[i]
                self._ja.insert(index, j)
                self._a.insert(index, value)
                self._ia[i+1:] = list(map(lambda x: x + 1, self._ia[i+1:]))

    def __add__(self, other):
        if max(self._ja) != max(other._ja) or len(self._ia) != len(other._ia):
            raise ValueError
        row_ind = []
        col_ind = []
        data = []
        for i in range(len(self._ia) - 1):
            d = {}
            for j in range(self._ia[i], self._ia[i+1]):
                d[self._ja[j]] = self[i, self._ja[j]]
            for j in range(other._ia[i], other._ia[i+1]):
                if other._ja[j] in d:
                    d[other._ja[j]] += other[i, other._ja[j]]
                else:
                    d[other._ja[j]] = other[i, other._ja[j]]
            for j, item in d.items():
                if item:
                    row_ind.append(i)
                    col_ind.append(j)
                    data.append(item)
        return CSRMatrix((row_ind, col_ind, data))

    def __sub__(self, other):
        if max(self._ja) != max(other._ja) or len(self._ia) != len(other._ia):
            raise ValueError
        row_ind = []
        col_ind = []
        data = []
        for i in range(len(self._ia) - 1):
            d = {}
            for j in range(self._ia[i], self._ia[i+1]):
                d[self._ja[j]] = self[i, self._ja[j]]
            for j in range(other._ia[i], other._ia[i+1]):
                if other._ja[j] in d:
                    d[other._ja[j]] -= other[i, other._ja[j]]
                else:
                    d[other._ja[j]] = -other[i, other._ja[j]]
            for j, item in d.items():
                if item:
                    row_ind.append(i)
                    col_ind.append(j)
                    data.append(item)
        return CSRMatrix((row_ind, col_ind, data))

    def __mul__(self, other):
        if max(self._ja) != max(other._ja) or len(self._ia) != len(other._ia):
            raise ValueError
        if isinstance(other, CSRMatrix):
            row_ind = []
            col_ind = []
            data = []
            for i in range(len(self._ia) - 1):
                d = {}
                for j in range(self._ia[i], self._ia[i+1]):
                    if other[i, self._ja[j]]:
                        d[self._ja[j]] = self[i, self._ja[j]]
                    else:
                        d[self._ja[j]] = 0
                for j in range(other._ia[i], other._ia[i+1]):
                    if other._ja[j] in d:
                        d[other._ja[j]] = self[i, other._ja[j]] * other[i, other._ja[j]]
                    else:
                        d[other._ja[j]] = 0
                for j, item in d.items():
                    if item:
                        row_ind.append(i)
                        col_ind.append(j)
                        data.append(item)
            return CSRMatrix((row_ind, col_ind, data))
        else:
            return self.__rmul__(other)

    def __rmul__(self, other):
        matrix_copy = copy.deepcopy(self)
        matrix_copy._a = [item * other for item in matrix_copy._a]
        return matrix_copy

    def __truediv__(self, other):
        try:
            return self.__rmul__(1 / other)
        except ZeroDivisionError:
            print('ERROR: ZeroDivisionError.')

    def __matmul__(self, other):
        if self._max_cols != other._max_rows:
            raise ValueError
        row_ind = []
        col_ind = []
        data = []
        other = other.transpose()
        for i_self in range(len(self._ia) - 1):
            for i_other in range(len(other._ia) - 1):
                d = {}
                scalar_product = 0
                for k in range(self._ia[i_self], self._ia[i_self+1]):
                    d[self._ja[k]] = self[i_self, self._ja[k]]
                for j in d.keys():
                    scalar_product += self[i_self, j] * other[i_other, j]
                if scalar_product:
                    data.append(scalar_product)
                    row_ind.append(i_self)
                    col_ind.append(i_other)
        return CSRMatrix((row_ind, col_ind, data))

    def dot(self, other):
        return self.__matmul__(other)

    def transpose(self):
        values = np.zeros((self._max_cols, self._max_rows))
        for i in range(self._max_rows):
            for j in range(self._ia[i], self._ia[i+1]):
                values[self._ja[j], i] = self._a[j]
        return CSRMatrix(values)

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        mat = np.zeros((self._max_rows, self._max_cols))
        for i in range(self._max_rows):
            if self._ia[i] != self._ia[i + 1]:
                for k in range(self._ia[i], self._ia[i + 1]):
                    mat[i, self._ja[k]] = self._a[k]
        return mat

    def __str__(self):
        return str(self.to_dense())

    @property
    def nnz(self):
        return self._nnz
