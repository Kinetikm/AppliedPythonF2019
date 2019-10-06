#!/usr/bin/env python
# coding: utf-8


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
        self.A = []
        self.IA = [0]
        self.JA = []

        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            row_ind, col_ind, data = init_matrix_representation

            self.A = deepcopy(data)
            self.JA = deepcopy(col_ind)
            count = 0

            if row_ind[0] != 0:
                for _ in range(row_ind[0]):
                    self.IA.append(count)
            for i in range(len(row_ind) - 1):
                count += 1
                if row_ind[i] != row_ind[i + 1]:
                    for _ in range(row_ind[i + 1] - row_ind[i]):
                        self.IA.append(count)
            count += 1
            self.IA.append(count)

        elif isinstance(init_matrix_representation, np.ndarray):
            count = 0

            for i in range(len(init_matrix_representation)):
                for j in range(len(init_matrix_representation[0])):
                    if init_matrix_representation[i][j] != 0:
                        self.A.append(init_matrix_representation[i][j])
                        self.JA.append(j)
                        count += 1
                self.IA.append(count)

        else:
            raise ValueError

        self._nnz = len(self.A)

    def get_nnz(self):
        return self._nnz

    nnz = property(fget=get_nnz)

    def __getitem__(self, item):

        row_num, col_num = item

        for el in range(self.IA[row_num], self.IA[row_num + 1]):
            if self.JA[el] == col_num:
                return self.A[el]
        return 0

    def __setitem__(self, key, value):
        rn, cn = key
        rn += 1

        if value != 0:
            num_items = self.IA[rn]
            for i in range(rn, len(self.IA)):
                self.IA[i] += 1

            self.A = self.A[:num_items] + [value] + self.A[num_items:]
            self.JA = self.JA[:num_items] + [cn] + self.JA[num_items:]

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        dense_matrix = np.zeros((len(self.IA) - 1, max(self.JA) + 1))

        for i in range(1, len(self.IA)):
            if self.IA[i - 1] != self.IA[i]:
                for j in range(self.IA[i - 1], self.IA[i]):
                    dense_matrix[i - 1, self.JA[j]] = self.A[j]

        return dense_matrix

    def __add__(self, other):
        if isinstance(other, CSRMatrix):
            row_ind = []
            col_ind = []
            data = []

            for r in range(1, len(self.IA)):
                data_self = {}
                if self.IA[r - 1] != self.IA[r]:
                    for i in range(self.IA[r - 1], self.IA[r]):
                        data_self[self.JA[i]] = self.A[i]
                if other.IA[r - 1] != other.IA[r]:
                    for i in range(other.IA[r - 1], other.IA[r]):
                        if other.JA[i] in data_self:
                            data_self[other.JA[i]] += other.A[i]
                        else:
                            data_self[other.JA[i]] = other.A[i]

                for col, value in data_self.items():
                    if value:
                        row_ind.append(r - 1)
                        col_ind.append(col)
                        data.append(value)

            return CSRMatrix((row_ind, col_ind, data))

    def __sub__(self, other):
        if isinstance(other, CSRMatrix):
            row_ind = []
            col_ind = []
            data = []

            for r in range(1, len(self.IA)):
                data_self = {}
                if self.IA[r - 1] != self.IA[r]:
                    for i in range(self.IA[r - 1], self.IA[r]):
                        data_self[self.JA[i]] = self.A[i]
                if other.IA[r - 1] != other.IA[r]:
                    for i in range(other.IA[r - 1], other.IA[r]):
                        if other.JA[i] in data_self:
                            data_self[other.JA[i]] -= other.A[i]
                        else:
                            data_self[other.JA[i]] = -other.A[i]

                for col, value in data_self.items():
                    if value:
                        row_ind.append(r - 1)
                        col_ind.append(col)
                        data.append(value)

            return CSRMatrix((row_ind, col_ind, data))

    def __mul__(self, other):
        if isinstance(other, CSRMatrix):
            row_ind = []
            col_ind = []
            data = []

            for r in range(1, len(self.IA)):
                data_self = {}
                data_res = {}
                if self.IA[r - 1] != self.IA[r]:
                    for i in range(self.IA[r - 1], self.IA[r]):
                        data_self[self.JA[i]] = self.A[i]
                if other.IA[r - 1] != other.IA[r]:
                    for i in range(other.IA[r - 1], other.IA[r]):
                        if other.JA[i] in data_self:
                            data_res[other.JA[i]] = data_self[other.JA[i]] * other.A[i]

                for col, value in data_res.items():
                    if value:
                        row_ind.append(r - 1)
                        col_ind.append(col)
                        data.append(value)

            return CSRMatrix((row_ind, col_ind, data))

    def __rmul__(self, other):
        result = deepcopy(self)
        for i in range(len(result.A)):
            result.A[i] *= other
        return result

    def __truediv__(self, other):
        result = deepcopy(self)
        for i in range(len(result.A)):
            result.A[i] /= other
        return result

    def __matmul__(self, other):
        if isinstance(other, CSRMatrix):
            if (max(self.JA) + 1) != (len(other.IA) - 1):
                raise ValueError

            row_ind = []
            col_ind = []
            data = []

            for i in range(len(self.IA) - 1):
                for j in range(max(other.JA) + 1):
                    cell_data = 0
                    for k in range(max(self.JA) + 1):
                        if self[i, k] and other[k, j]:
                            cell_data += self[i, k] * other[k, j]
                    if cell_data:
                        data.append(cell_data)
                        col_ind.append(j)
                        row_ind.append(i)

            return CSRMatrix((row_ind, col_ind, data))
