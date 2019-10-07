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
        self.A = np.array([])
        self.IA = np.array([0], dtype=int)
        self.JA = np.array([], dtype=int)
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            row_ind = init_matrix_representation[0]
            col_ind = init_matrix_representation[1]
            data = init_matrix_representation[2]
            self.shape = tuple([max(row_ind) + 1, max(col_ind) + 1])
            matrix = np.zeros(self.shape, dtype=int)
            for i in range(len(data)):
                matrix[row_ind[i], col_ind[i]] = data[i]
            for i in range(self.shape[0]):
                nonzero = 0
                for j in range(self.shape[1]):
                    if matrix[i][j] != 0:
                        self.A = np.append(self.A, matrix[i][j])
                        self.JA = np.append(self.JA, j)
                        nonzero += 1
                self.IA = np.append(self.IA, self.IA[i] + nonzero)
            self.__nnz = len(self.A)
        elif isinstance(init_matrix_representation, np.ndarray):
            self.shape = init_matrix_representation.shape
            for i in range(self.shape[0]):
                nonzero = 0
                for j in range(self.shape[1]):
                    if init_matrix_representation[i][j] != 0:
                        self.A = np.append(self.A, init_matrix_representation[i][j])
                        self.JA = np.append(self.JA, j)
                        nonzero += 1
                self.IA = np.append(self.IA, self.IA[i] + nonzero)
            self.__nnz = len(self.A)
        else:
            raise ValueError

    @property
    def nnz(self):
        return self.__nnz

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        matrix = np.zeros(self.shape)
        element = 0
        for i in range(1, len(self.IA)):
            number = self.IA[i] - self.IA[i - 1]
            for j in range(number):
                matrix[i - 1][self.JA[element]] = self.A[element]
                element += 1
        return matrix

    def __getitem__(self, item):
        try:
            koord = list(item)
        except TypeError:
            koord = []
            if type(item) != int:
                raise IndexError
            koord.append(item)
        if len(koord) > 2:
            raise IndexError
        if len(koord) == 2:
            for i in range(self.IA[koord[0] + 1] - self.IA[koord[0]]):
                element = self.A[self.IA[koord[0]] + i]
                if koord[1] == self.JA[self.IA[koord[0]] + i]:
                    return element
            return 0
        if len(koord) == 1:
            arr = np.zeros((self.shape[1],))
            for i in range(self.IA[koord[0] + 1] - self.IA[koord[0]]):
                element = self.A[self.IA[koord[0]] + i]
                arr[self.JA[self.IA[koord[0]] + i]] = element
            return arr
        raise IndexError

    def __setitem__(self, key, value):
        i, j = key
        if value and self[key[0], key[1]]:
            k = self.JA.tolist().index(j, self.IA[i], self.IA[i + 1])
            self.A[k] = value
        elif value and not self[key[0], key[1]]:
            try:
                k = self.JA.tolist().index(j, self.IA[i], self.IA[i + 1])
            except ValueError:
                self.A = np.insert(self.A, self.IA[i + 1], value)
                self.JA = np.insert(self.JA, self.IA[i + 1], j)
            else:
                self.A = np.insert(self.A, k, value)
                self.JA = np.insert(self.JA, k, j)
            for k in range(i + 1, len(self.IA)):
                self.IA[k] += 1
            self.__nnz += 1
        elif self[key[0], key[1]]:
            k = self.JA.tolist().index(j, self.IA[i], self.IA[i + 1])
            self.A = np.delete(self.A, k)
            self.JA = np.delete(self.JA, k)
            for k in range(i + 1, len(self.IA)):
                self.IA[k] -= 1
            self.__nnz -= 1

    def __add__(self, other):
        if self.shape != other.shape:
            raise ValueError
        matrix1 = self.to_dense()
        matrix2 = other.to_dense()
        return CSRMatrix(matrix1 + matrix2)

    def __sub__(self, other):
        if self.shape != other.shape:
            raise ValueError
        matrix1 = self.to_dense()
        matrix2 = other.to_dense()
        return CSRMatrix(matrix1 - matrix2)

    def __mul__(self, other):
        if (type(other) == int) or type(other) == float:
            if other == 0:
                return CSRMatrix(np.zeros(self.shape))
            new = deepcopy(self)
            new.A *= float(other)
            return new
        if type(self) != type(other):
            return ValueError
        if self.shape != other.shape:
            raise ValueError
        matrix1 = self.to_dense()
        matrix2 = other.to_dense()
        return CSRMatrix(matrix1 * matrix2)

    def __rmul__(self, other):
        if (type(other) == int) or type(other) == float:
            if other == 0:
                return CSRMatrix(np.zeros(self.shape))
            new = deepcopy(self)
            new.A *= other
            return new
        if type(self) != type(other):
            return ValueError

    def __truediv__(self, other):
        if (type(other) == int) or type(other) == float:
            if other == 0:
                raise ZeroDivisionError
            new = deepcopy(self)
            new.A /= other
            return new
        raise ValueError

    def __matmul__(self, other):
        if type(self) != type(other):
            raise ValueError
        if self.shape[1] != other.shape[0]:
            raise ValueError
        result = (self.to_dense()) @ (other.to_dense())
        return CSRMatrix(result)

        '''for i in range(self.shape[0]):
            amount = self.IA[i + 1] - self.IA[i]
            for j in range(other.shape[1]):
                element = self.IA[i]
                temp = 0
                for k in range(amount):
                    if (element < len(self.A)) and (other[self.JA[element], j] != 0):
                        temp += self.A[element] * other[self.JA[element], j]
                    element += 1
                result[i, j] = temp
        return CSRMatrix(result)
        raise NotImplementedError'''

    '''def dot(self, other):
        if type(self) != type(other):
            raise ValueError
        if self.shape[1] != other.shape[0]:
            raise ValueError
        result = np.zeros((self.shape[0], other.shape[1]))
        element = 0
        for i in range(self.shape[0]):
            amount = self.IA[i + 1] - self.IA[i]
            for j in range(other.shape[1]):
                element = self.IA[i]
                temp = 0
                for k in range(amount):
                    if (element < len(self.A)) and (other[self.JA[element], j] != 0):
                        temp += self.A[element] * other[self.JA[element], j]
                    element += 1
                result[i, j] = temp
        return CSRMatrix(result)
        raise NotImplementedError'''
