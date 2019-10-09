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
        self.A = []
        self.IA = [0]
        self.JA = []

        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            s = 0
            self.max_col = max(init_matrix_representation[1]) + 1
            num = max(init_matrix_representation[0]) + 1
            self.IA = [0]*(num + 1)
            for k, item in enumerate(init_matrix_representation[0]):
                row = item % num
                if init_matrix_representation[2][k]:
                    self.A.append(init_matrix_representation[2][k])
                    self.JA.append(init_matrix_representation[1][k])
                    s += 1
                self.IA[row + 1] = s
            i = self.IA.index(s)
            self.IA[i:] = [s for _ in self.IA[i:]]

        elif isinstance(init_matrix_representation, np.ndarray):
            number = 0
            for i, line in enumerate(init_matrix_representation):
                for j, item in enumerate(line):
                    if item:
                        self.A.append(item)
                        self.JA.append(j)
                        number += 1
                self.IA.append(number)
            self.max_col = len(init_matrix_representation[0])

        else:
            raise ValueError

        self._nnz = self.IA[-1]

    @property
    def nnz(self):
        return self._nnz

    def __getitem__(self, indexes):
        try:
            i = indexes[0]
            j = indexes[1]
            k = self.JA[self.IA[i]:self.IA[i+1]].index(j) + self.IA[i]
            return self.A[k]
        except ValueError:
            return 0

    def __setitem__(self, indexes, value):
        i = indexes[0]
        j = indexes[1]
        if self[i, j]:
            k = self.JA[self.IA[i]:self.IA[i+1]].index(j) + self.IA[i]
            self.A[k] = value
        else:
            if (self.IA[i] - self.IA[i+1]) != 0:
                for l, item in enumerate(self.JA[self.IA[i]:self.IA[i+1]]):
                    if item > j:
                        index = l + self.IA[i]
                        self.JA.insert(index, j)
                        self.A.insert(index, value)
                        self.IA[i+1:] = [k + 1 for k in self.IA[i+1:]]
                        break
            else:
                self.JA.insert(self.IA[i], j)
                self.A.insert(self.IA[i], value)
                self.IA[i+1:] = [k + 1 for k in self.IA[i+1:]]

    def __add__(self, other):
        if (self.max_col != other.max_col) or (len(self.IA) != len(other.IA)):
            raise ValueError
        else:
            row = []
            col = []
            data = []
            for i in range(len(self.IA)-1):
                d = {}
                for k in range(self.IA[i], self.IA[i+1]):
                    d[self.JA[k]] = self.A[k]
                for l in range(other.IA[i], other.IA[i+1]):
                    if other.JA[l] in d:
                        d[other.JA[l]] += other.A[l]
                    else:
                        d[other.JA[l]] = other.A[l]

                for j, item in d.items():
                    if item:
                        row.append(i)
                        col.append(j)
                        data.append(item)
            return CSRMatrix((row, col, data))

    def __sub__(self, other):
        if (self.max_col != other.max_col) or (len(self.IA) != len(other.IA)):
            raise ValueError
        else:
            row = []
            col = []
            data = []
            for i in range(len(self.IA)-1):
                d = {}
                for k in range(self.IA[i], self.IA[i+1]):
                    d[self.JA[k]] = self.A[k]
                for l in range(other.IA[i], other.IA[i+1]):
                    if other.JA[l] in d:
                        d[other.JA[l]] -= other.A[l]
                    else:
                        d[other.JA[l]] = -other.A[l]

                for j, item in d.items():
                    if item:
                        row.append(i)
                        col.append(j)
                        data.append(item)
            return CSRMatrix((row, col, data))

    def __rmul__(self, other):
        row = []
        col = []
        data = []
        if isinstance(other, (float, int)):
            for i in range(len(self.IA)-1):
                for k in range(self.IA[i], self.IA[i+1]):
                    row.append(i)
                    col.append(self.JA[k])
                    data.append(self.A[k]*2.5)
            return CSRMatrix((row, col, data))
        else:
            if (self.max_col != other.max_col) or (len(self.IA) != len(other.IA)):
                raise ValueError
            else:
                for i in range(len(self.IA)-1):
                    d1 = {}
                    d2 = {}
                    for k in range(self.IA[i], self.IA[i+1]):
                        d1[self.JA[k]] = self.A[k]
                    for l in range(other.IA[i], other.IA[i+1]):
                        d2[other.JA[l]] = other.A[l]
                    for j in d1:
                        if j in d2:
                            row.append(i)
                            col.append(j)
                            data.append(d2[j]*d1[j])
                return CSRMatrix((row, col, data))

    def __mul__(self, other):
        row = []
        col = []
        data = []
        if isinstance(other, (float, int)):
            for i in range(len(self.IA)-1):
                for k in range(self.IA[i], self.IA[i+1]):
                    row.append(i)
                    col.append(self.JA[k])
                    data.append(self.A[k]*2.5)
            return CSRMatrix((row, col, data))
        else:
            if (self.max_col != other.max_col) or (len(self.IA) != len(other.IA)):
                raise ValueError
            else:
                for i in range(len(self.IA)-1):
                    d1 = {}
                    d2 = {}
                    for k in range(self.IA[i], self.IA[i+1]):
                        d1[self.JA[k]] = self.A[k]
                    for l in range(other.IA[i], other.IA[i+1]):
                        d2[other.JA[l]] = other.A[l]
                    for j in d1:
                        if j in d2:
                            row.append(i)
                            col.append(j)
                            data.append(d2[j]*d1[j])
                return CSRMatrix((row, col, data))

    def __truediv__(self, alpha):
        if isinstance(alpha, (float, int)):
            row = []
            col = []
            data = []
            for i in range(len(self.IA)-1):
                for k in range(self.IA[i], self.IA[i+1]):
                    row.append(i)
                    col.append(self.JA[k])
                    data.append(self.A[k]/alpha)
            return CSRMatrix((row, col, data))

    def __matmul__(self, other):

        other = CSRMatrix(other.to_dense().transpose())
        if max(other.JA) != max(self.JA):
            raise ValueError
        else:
            row = []
            col = []
            data = []
            for i in range(len(self.IA)-1):
                for l in range(len(other.IA)-1):
                    d = {}
                    d1 = {}
                    s = 0
                    for k in range(self.IA[i], self.IA[i+1]):
                        d[self.JA[k]] = self.A[k]
                    for k in range(other.IA[l], other.IA[l+1]):
                        d1[other.JA[k]] = other.A[k]

                    for j in d1:
                        if j in d:
                            s += d[j]*d1[j]
                    if s:
                        row.append(i)
                        col.append(l)
                        data.append(s)
            return CSRMatrix((row, col, data))

    def dot(self, other):

        other = CSRMatrix(other.to_dense().transpose())
        if max(other.JA) != max(self.JA):
            raise ValueError
        else:
            row = []
            col = []
            data = []
            for i in range(len(self.IA)-1):
                for l in range(len(other.IA)-1):
                    d = {}
                    d1 = {}
                    s = 0
                    for k in range(self.IA[i], self.IA[i+1]):
                        d[self.JA[k]] = self.A[k]
                    for k in range(other.IA[l], other.IA[l+1]):
                        d1[other.JA[k]] = other.A[k]

                    for j in d1:
                        if j in d:
                            s += d[j]*d1[j]
                    if s:
                        row.append(i)
                        col.append(l)
                        data.append(s)
            return CSRMatrix((row, col, data))

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        dense_matrix = np.zeros((len(self.IA)-1, self.max_col))
        for i in range(len(self.IA)-1):
            for k in range(self.IA[i], self.IA[i+1]):
                dense_matrix[i, self.JA[k]] = self.A[k]
        return dense_matrix
