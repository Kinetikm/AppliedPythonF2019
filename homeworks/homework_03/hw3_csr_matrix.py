#!/usr/bin/env python
# coding: utf-8


from __future__ import division
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
    4. _nnz attribute -- number of nonzero elements in matrix
    """

    @property
    def nnz(self):
        return self._nnz

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: can be usual dense matrix
        or
        (row_ind, col, data) tuple with np.arrays,
            where data, row_ind and col_ind satisfy the relationship:
            a[row_ind[k], col_ind[k]] = data[k]
        """
        self.A = np.array([])
        self.IA = np.array([0])
        self.JA = np.array([])
        self._nnz = 0
        if isinstance(init_matrix_representation, type(None)):
            pass
        elif isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.A = np.array(init_matrix_representation[2])
            self.JA = np.array(init_matrix_representation[1])
            self.IA = np.array([0])
            self._nnz = 0
            self.shape = (max(init_matrix_representation[0]) + 1, max(self.JA) + 1)
            if init_matrix_representation[0][0] != 0:
                for k in range(init_matrix_representation[0][0]):
                    self.IA = np.append(self.IA, 0)
            for i in range(len(init_matrix_representation[0]) - 1):
                self._nnz += 1
                if init_matrix_representation[0][i] != init_matrix_representation[0][i+1]:
                    for k in range(init_matrix_representation[0][i+1] - init_matrix_representation[0][i]):
                        self.IA = np.append(self.IA, self._nnz)
            self._nnz = len(self.A)
            self.IA = np.append(self.IA, self._nnz)
        elif isinstance(init_matrix_representation, np.ndarray):
            self.shape = init_matrix_representation.shape
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    if init_matrix_representation[i, j] != 0:
                        self._nnz += 1
                        self.A = np.append(self.A, init_matrix_representation[i, j])
                        self.JA = np.append(self.JA, j)
                self.IA = np.append(self.IA, self._nnz)
        else:
            raise ValueError

    def __getitem__(self, pos):
        i, j = pos
        if self.IA[i+1] == self.IA[i]:
            return 0
        else:
            for index in range(self.IA[i]+1, self.IA[i+1]+1):
                if self.JA[index-1] == j:
                    return self.A[index-1]
        return 0

    def __setitem__(self, pos, value):
        i, j = pos
        if value == 0:
            if self[i, j] != 0:
                elements = {}
                for index in range(self.IA[i], self.IA[i+1]):
                    elements[self.JA[index]] = self.A[index]
                del elements[j]
                resA = np.array([])
                resJA = np.array([])
                new_row_A = np.array([elements[j] for j in sorted(elements.keys())])
                new_row_JA = np.array([key for key in sorted(elements.keys())])
                resA = np.append(resA, self.A[:self.IA[i]])
                resA = np.append(resA, new_row_A)
                resA = np.append(resA, self.A[self.IA[i+1]:])
                resJA = np.append(resJA, self.JA[:self.IA[i]])
                resJA = np.append(resJA, new_row_JA)
                resJA = np.append(resJA, self.JA[self.IA[i+1]:])
                for index in range(i+1, len(self.IA)):
                    self.IA[index] -= 1
                self.JA = resJA
                self.A = resA
                self._nnz = self.IA[-1]
                return self
            else:
                return self
        else:
            if self[i, j] != 0:
                for index in range(self.IA[i]+1, self.IA[i+1]+1):
                    if self.JA[index-1] == j:
                        self.A[index-1] = value
                        return self
            else:
                elements = {}
                for index in range(self.IA[i], self.IA[i+1]):
                    elements[self.JA[index]] = self.A[index]
                elements[j] = value
                resA = np.array([])
                resJA = np.array([])
                new_row_A = np.array([elements[j] for j in sorted(elements.keys())])
                new_row_JA = np.array([key for key in sorted(elements.keys())])
                resA = np.append(resA, self.A[:self.IA[i]])
                resA = np.append(resA, new_row_A)
                resA = np.append(resA, self.A[self.IA[i+1]:])
                resJA = np.append(resJA, self.JA[:self.IA[i]])
                resJA = np.append(resJA, new_row_JA)
                resJA = np.append(resJA, self.JA[self.IA[i+1]:])
                for index in range(i+1, len(self.IA)):
                    self.IA[index] += 1
                self.JA = resJA
                self.A = resA
                self._nnz = self.IA[-1]
                return self

    def __add__(self, other):
        if self.shape != other.shape:
            raise ValueError
        resA = np.array([])
        resIA = np.array([0])
        resJA = np.array([])
        for i in range(len(self.IA)-1):
            if self.IA[i+1] - self.IA[i] != 0 or other.IA[i+1] - other.IA[i] != 0:
                elements = {}
                for j in range(self.IA[i], self.IA[i+1]):
                    elements[self.JA[j]] = self.A[j]
                for j in range(other.IA[i], other.IA[i+1]):
                    if other.JA[j] not in elements:
                        elements[other.JA[j]] = other.A[j]
                    else:
                        elements[other.JA[j]] += other.A[j]
                for col, value in sorted(elements.items()):
                    if value != 0:
                        resA = np.append(resA, value)
                        resJA = np.append(resJA, col)
                resIA = np.append(resIA, len(resA))
        result = CSRMatrix(None)
        result.A = resA
        result.IA = resIA
        result.JA = resJA
        result._nnz = result.IA[-1]
        result.shape = self.shape
        return result

    def __sub__(self, other):
        if self.shape != other.shape:
            raise ValueError
        resA = np.array([])
        resIA = np.array([0])
        resJA = np.array([])
        for i in range(len(self.IA)-1):
            if self.IA[i+1] - self.IA[i] != 0 or other.IA[i+1] - other.IA[i] != 0:
                elements = {}
                for j in range(self.IA[i], self.IA[i+1]):
                    elements[self.JA[j]] = self.A[j]
                for j in range(other.IA[i], other.IA[i+1]):
                    if other.JA[j] not in elements:
                        elements[other.JA[j]] = -other.A[j]
                    else:
                        elements[other.JA[j]] -= other.A[j]
                for col, value in sorted(elements.items()):
                    if value != 0:
                        resA = np.append(resA, value)
                        resJA = np.append(resJA, col)
                resIA = np.append(resIA, len(resA))
        result = CSRMatrix(None)
        result.shape = self.shape
        result.A = resA
        result.IA = resIA
        result.JA = resJA
        result._nnz = result.IA[-1]
        return result

    def __mul__(self, other):
        if self.shape != other.shape:
            raise ValueError
        result = CSRMatrix(None)
        result.shape = self.shape
        if type(other) == CSRMatrix:
            resA = np.array([])
            resIA = np.array([0])
            resJA = np.array([])
            for i in range(len(self.IA)-1):
                if self.IA[i+1] - self.IA[i] != 0 or other.IA[i+1] - other.IA[i] != 0:
                    elements = {}
                    for j in range(self.IA[i], self.IA[i+1]):
                        for k in range(other.IA[i], other.IA[i+1]):
                            if self.JA[j] == other.JA[k]:
                                elements[self.JA[j]] = self.A[j] * other.A[k]
                    for col, value in sorted(elements.items()):
                        if value != 0:
                            resA = np.append(resA, value)
                            resJA = np.append(resJA, col)
                    resIA = np.append(resIA, len(resA))
            result.A = resA
            result.IA = resIA
            result.JA = resJA
            result._nnz = result.IA[-1]
            return result
        else:
            if other == 0:
                result.A = []
                result.IA = [0]
                result.JA = []
                result._nnz = 0
                return result
            else:
                result.A = np.array([])
                for i in range(len(self.A)):
                    result.A = np.append(result.A, self.A[i] * other)
                result.JA = self.JA
                result.IA = self.IA
                result._nnz = self._nnz
                return result

    def __rmul__(self, other):
        result = CSRMatrix(None)
        result.shape = self.shape
        if other == 0:
            result.A = []
            result.IA = [0]
            result.JA = []
            result._nnz = 0
            return result
        else:
            result.A = np.array([])
            for i in range(len(self.A)):
                result.A = np.append(result.A, self.A[i] * other)
            result.JA = self.JA
            result.IA = self.IA
            result._nnz = self._nnz
            return result

    def __truediv__(self, other):
        result = CSRMatrix(None)
        result.shape = self.shape
        result.A = self.A
        result.IA = self.IA
        result.JA = self.JA
        result._nnz = self._nnz
        for i in range(len(self.A)):
            result.A[i] /= other
        return result

    def transpose(self):
        result = CSRMatrix(None)
        _nnz = 0
        resA = np.array([])
        resIA = np.array([0])
        resJA = np.array([])
        strs = [[] for i in range(self.shape[1])]
        values = [[] for i in range(self.shape[1])]
        for i in range(len(self.IA)-1):
            for index in range(self.IA[i], self.IA[i+1]):
                strs[int(self.JA[index])].append(i)
                values[int(self.JA[index])].append(self.A[index])
        for s in strs:
            _nnz += len(s)
            resIA = np.append(resIA, _nnz)
        for k in range(len(strs)):
            resA = np.append(resA, values[k])
            resJA = np.append(resJA, strs[k])
        result.shape = (self.shape[1], self.shape[0])
        result.A = resA
        result.JA = resJA
        result.IA = resIA
        result._nnz = resIA[-1]
        return result

    def __matmul__(self, other):
        if self.shape[1] != other.shape[0]:
            raise ValueError
        C = other.transpose()
        summ = 0
        ks = 0
        ls = 0
        result = CSRMatrix(None)
        result.shape = (self.shape[0], other.shape[1])
        result.A = np.array([])
        result.IA = np.array([0])
        result.JA = np.array([])
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
                summ = 0
                ls = C.IA[j]
                ks = self.IA[i]
                while ls != C.IA[j+1] and ks != self.IA[i+1]:
                    if self.JA[ks] == C.JA[ls]:
                        summ += self.A[ks] * C.A[ls]
                        ks += 1
                        ls += 1
                    elif self.JA[ks] > C.JA[ls]:
                        ls += 1
                    else:
                        ks += 1
                if summ != 0:
                    result.A = np.append(result.A, summ)
                    result.JA = np.append(result.JA, j)
            ls = C.IA[j+1]
            ks = self.IA[i+1]
            result.IA = np.append(result.IA, len(result.A))
        result._nnz = result.IA[-1]
        return result

    def dot(self, other):
        if self.shape[1] != other.shape[0]:
            raise ValueError
        C = other.transpose()
        summ = 0
        ks = 0
        ls = 0
        result = CSRMatrix(None)
        result.shape = (self.shape[0], other.shape[1])
        result.A = np.array([])
        result.IA = np.array([0])
        result.JA = np.array([])
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
                summ = 0
                ls = C.IA[j]
                ks = self.IA[i]
                while ls != C.IA[j+1] and ks != self.IA[i+1]:
                    if self.JA[ks] == C.JA[ls]:
                        summ += self.A[ks] * C.A[ls]
                        ks += 1
                        ls += 1
                    elif self.JA[ks] > C.JA[ls]:
                        ls += 1
                    else:
                        ks += 1
                if summ != 0:
                    result.A = np.append(result.A, summ)
                    result.JA = np.append(result.JA, j)
            ls = C.IA[j+1]
            ks = self.IA[i+1]
            result.IA = np.append(result.IA, len(result.A))
        result._nnz = result.IA[-1]
        return result

    def to_dense(self):
        result = []
        string = []
        found = False
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                for k in range(self.IA[i], self.IA[i+1]):
                    if self.JA[k] == j:
                        string.append(self.A[k])
                        found = True
                if found is False:
                    string.append(0)
                found = False
            result.append(string)
            string = []
        result = np.array(result)
        return result
