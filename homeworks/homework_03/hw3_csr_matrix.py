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
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.A = init_matrix_representation[2][:]
            self.IA = [0] * (init_matrix_representation[0][len(init_matrix_representation[0])-1] + 2)
            self.JA = init_matrix_representation[1][:]
            self.N = max(init_matrix_representation[0]) + 1
            self.M = max(init_matrix_representation[1]) + 1
            self.nnz = len(self.A)
            for i in init_matrix_representation[0]:
                self.IA[i + 1] += 1
            for i in range(1, len(self.IA)-1):
                self.IA[i+1] += self.IA[i]
        elif isinstance(init_matrix_representation, np.ndarray):
            self.A = []
            self.IA = [0] * (len(init_matrix_representation) + 1)
            self.JA = []
            self.nnz = 0
            self.N = len(init_matrix_representation)
            self.M = len(init_matrix_representation[0])
            for i in range(len(init_matrix_representation)):
                for j in range(len(init_matrix_representation[0])):
                    if init_matrix_representation[i][j] != 0:
                        self.A.append(init_matrix_representation[i][j])
                        self.JA.append(j)
                        self.IA[i + 1] += 1
                        self.nnz += 1
            for i in range(1, len(self.IA)-1):
                self.IA[i+1] += self.IA[i]

        else:
            raise ValueError

    @property
    def nnz(self):
        return self._nnz

    @nnz.setter
    def nnz(self, value):
        if value == len(self.A):
            self._nnz = value

    def __setitem__(self, key, value):
        i = key[0]
        j = key[1]
        if value:
            if self.__getitem__(key) != 0:
                for c in range(self.IA[i], self.IA[i + 1]):
                    if self.JA[c] == j:
                        self.A[c] = value
            else:
                if not self.A:
                    self.A.append(value)
                    self.JA.append(j)
                    for c in range(i + 1, len(self.IA)):
                        self.IA[c] += 1
                else:
                    if self.IA[i + 1] - self.IA[i] > 0:
                        if j < self.JA[self.IA[i]]:
                            self.JA.insert(self.IA[i], j)
                            self.A.insert(self.IA[i], value)
                        else:
                            self.JA.insert(self.IA[i + 1], j)
                            self.A.insert(self.IA[i + 1], value)
                        for c in range(i + 1, len(self.IA)):
                            self.IA[c] += 1
                    else:
                        if self.IA[-1] == self.IA[i]:
                            self.A.append(value)
                            self.JA.append(j)
                            for c in range(i + 1, len(self.IA)):
                                self.IA[c] += 1
                        else:
                            self.JA.insert(self.IA[i], j)
                            self.A.insert(self.IA[i], value)
                            for c in range(i + 1, len(self.IA)):
                                self.IA[c] += 1
        else:
            if self.__getitem__(key) != 0:
                for c in range(self.IA[i], self.IA[i + 1]):
                    if self.JA[c] == j:
                        del self.A[c]
                        del self.JA[c]
                        break
                for c in range(i + 1, len(self.IA)):
                    self.IA[c] -= 1
        self.nnz = len(self.A)

    def __getitem__(self, item):
        i = item[0]
        j = item[1]
        if self.IA[i + 1] - self.IA[i] > 0:
            for c in range(self.IA[i], self.IA[i + 1]):
                if self.JA[c] == j:
                    return self.A[c]
        return 0

    def to_dense(self):
        matrix = []
        for i in range(0, self.N):
            row = [0] * self.M
            for j in range(self.IA[i], self.IA[i + 1]):
                row[self.JA[j]] = self.A[j]
            matrix.append(row)
        x = np.array(matrix)
        return x

    def __add__(self, other):
        result = copy.deepcopy(self)
        if self.N == other.N and self.M == other.M:
            for i in range(self.N):
                for j in range(self.M):
                    result[i, j] = self[i, j] + other[i, j]
        return result

    def __sub__(self, other):
        result = copy.deepcopy(self)
        if self.N == other.N and self.M == other.M:
            for i in range(self.N):
                for j in range(self.M):
                    result[i, j] = self[i, j] - other[i, j]
        return result

    def __mul__(self, other):
        result = copy.deepcopy(self)
        if isinstance(other, int) or isinstance(other, float):
            for i in range(len(self.A)):
                result.A[i] = self.A[i] * other
            return result
        elif isinstance(other, CSRMatrix):
            if self.M == other.M and self.N == other.N:
                result = copy.deepcopy(self)
                for i in range(self.N):
                    for j in range(other.M):
                        result[i, j] = self[i, j] * other[i, j]
                return result
        else:
            raise ValueError

    def __rmul__(self, other):
        return self*other

    def __truediv__(self, other):
        result = copy.deepcopy(self)
        if other != 0:
            for i in range(len(self.A)):
                result.A[i] = self.A[i] / other
        return result

    def __matmul__(self, other):
        if isinstance(other, CSRMatrix):
            if self.M == other.N:
                result = CSRMatrix(np.zeros((self.N, other.M)))
                for i in range(self.N):
                    for j in range(other.M):
                        x = 0
                        for k in range(self.M):
                            x += self[i, k] * other[k, j]
                        result[i, j] = x
                result.nnz = len(result.A)
                return result
            else:
                raise ValueError
        else:
            raise Exception

    def dot(self, other):
        return self @ other
