#!/usr/bin/env python
# coding: utf-8


from copy import deepcopy
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
        self._matrix = []
        self._imatrix = [0]
        self._jmatrix = []
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            row_ind = init_matrix_representation[0]
            col_ind = init_matrix_representation[1]
            data = init_matrix_representation[2]
            sum_ = 0
            idx = 0
            # TODO: Переделать это
            for i in range(max(row_ind) + 1):
                sum_ += list(row_ind).count(i)
                self._imatrix.append(sum_)
            self._matrix = list(data)
            self._jmatrix = list(col_ind)
        elif isinstance(init_matrix_representation, np.ndarray):
            sum_ = 0
            for i, item in enumerate(init_matrix_representation):
                for j, element in enumerate(item):
                    if element:
                        self._matrix.append(element)
                        self._jmatrix.append(j)
                        sum_ += 1
                self._imatrix.append(sum_)
            self._max_cols = len(init_matrix_representation[0])
        else:
            raise ValueError
        self._nnz = len(self._matrix)

    def __getitem__(self, indexes):
        '''
        :param indexes: i and j indexes
        '''
        i = indexes[0]
        j = indexes[1]
        try:
            idx_matrix = self._jmatrix[self._imatrix[i]:self._imatrix[i+1]].index(j) + self._imatrix[i]
            return self._matrix[idx_matrix]
        except ValueError:
            return 0

    def __setitem__(self, indexes, value):
        i = indexes[0]
        j = indexes[1]
        if self[i, j]:
            idx_matrix = self._jmatrix[self._imatrix[i]:self._imatrix[i + 1]].index(j) + self._imatrix[i]
            self._matrix[idx_matrix] = value
        else:
            if (self._imatrix[i] - self._imatrix[i+1]) != 0:
                for l, item in enumerate(self._jmatrix[self._imatrix[i]:self._imatrix[i+1]]):
                    if item > j:
                        index = l + self._imatrix[i]
                        self._jmatrix.insert(index, j)
                        self._matrix.insert(index, value)
                        self._imatrix[i+1:] = list(map(lambda x: x + 1, self._imatrix[i+1:]))
                        break
            else:
                index = self._imatrix[i]
                self._jmatrix.insert(index, j)
                self._matrix.insert(index, value)
                self._imatrix[i+1:] = list(map(lambda x: x + 1, self._imatrix[i+1:]))

    def __add__(self, other):
        if max(self._jmatrix) != max(other._jmatrix) or len(self._imatrix) != len(other._imatrix):
            raise ValueError
        row_ind = []
        col_ind = []
        data = []
        for i in range(len(self._imatrix) - 1):
            d = {}
            for j in range(self._imatrix[i], self._imatrix[i+1]):
                d[self._jmatrix[j]] = self[i, self._jmatrix[j]]
            for j in range(other._imatrix[i], other._imatrix[i+1]):
                if other._jmatrix[j] in d:
                    d[other._jmatrix[j]] += other[i, other._jmatrix[j]]
                else:
                    d[other._jmatrix[j]] = other[i, other._jmatrix[j]]
            for j, item in d.items():
                if item:
                    row_ind.append(i)
                    col_ind.append(j)
                    data.append(item)
        return CSRMatrix((row_ind, col_ind, data))

    def __sub__(self, other):
        if max(self._jmatrix) != max(other._jmatrix) or len(self._imatrix) != len(other._imatrix):
            raise ValueError
        row_ind = []
        col_ind = []
        data = []
        for i in range(len(self._imatrix) - 1):
            d = {}
            for j in range(self._imatrix[i], self._imatrix[i+1]):
                d[self._jmatrix[j]] = self[i, self._jmatrix[j]]
            for j in range(other._imatrix[i], other._imatrix[i+1]):
                if other._jmatrix[j] in d:
                    d[other._jmatrix[j]] -= other[i, other._jmatrix[j]]
                else:
                    d[other._jmatrix[j]] = -other[i, other._jmatrix[j]]
            for j, item in d.items():
                if item:
                    row_ind.append(i)
                    col_ind.append(j)
                    data.append(item)
        return CSRMatrix((row_ind, col_ind, data))

    def __mul__(self, other):
        if max(self._jmatrix) != max(other._jmatrix) or len(self._imatrix) != len(other._imatrix):
            raise ValueError
        if isinstance(other, CSRMatrix):
            row_ind = []
            col_ind = []
            data = []
            for i in range(len(self._imatrix) - 1):
                d = {}
                for j in range(self._imatrix[i], self._imatrix[i+1]):
                    if other[i, self._jmatrix[j]]:
                        d[self._jmatrix[j]] = self[i, self._jmatrix[j]]
                    else:
                        d[self._jmatrix[j]] = 0
                for j in range(other._imatrix[i], other._imatrix[i+1]):
                    if other._jmatrix[j] in d:
                        d[other._jmatrix[j]] = self[i, other._jmatrix[j]] * other[i, other._jmatrix[j]]
                    else:
                        d[other._jmatrix[j]] = 0
                for j, item in d.items():
                    if item:
                        row_ind.append(i)
                        col_ind.append(j)
                        data.append(item)
            return CSRMatrix((row_ind, col_ind, data))
        else:
            return self.__rmul__(other)

    def __rmul__(self, other):
        new_matrix = deepcopy(self)
        new_matrix._matrix = [item * other for item in new_matrix._matrix]
        return new_matrix

    def __truediv__(self, other):
        try:
            new_matrix = deepcopy(self)
            new_matrix._matrix = [item / other for item in new_matrix._matrix]
            return new_matrix
        except ZeroDivisionError:
            print('A-ta-ta, nizya tak dealt')

    def __matmul__(self, other):
        if self._max_cols != len(other._imatrix) - 1:
            raise ValueError
        row_ind = []
        col_ind = []
        data = []
        other = other.transpose()
        for i_self in range(len(self._imatrix) - 1):
            for i_other in range(len(other._imatrix) - 1):
                d = {}
                scalar_product = 0
                for k in range(self._imatrix[i_self], self._imatrix[i_self+1]):
                    d[self._jmatrix[k]] = self[i_self, self._jmatrix[k]]
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
        values = np.zeros((self._max_cols, len(self._imatrix) - 1))
        for i in range(len(self._imatrix) - 1):
            for j in range(self._imatrix[i], self._imatrix[i+1]):
                values[self._jmatrix[j], i] = self._matrix[j]
        return CSRMatrix(values)

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        mat = np.zeros((len(self._imatrix) - 1, self._max_cols))
        for i in range(len(self._imatrix) - 1):
            if self._imatrix[i] != self._imatrix[i+1]:
                for k in range(self._imatrix[i], self._imatrix[i+1]):
                    mat[i, self._jmatrix[k]] = self._matrix[k]
        return mat

    def __str__(self):
        return str(self.to_dense())

    @property
    def nnz(self):
        return self._nnz
