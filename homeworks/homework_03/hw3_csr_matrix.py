#!/usr/bin/env python
# coding: utf-8


import numpy as np


class CSRMatrix:
    """
    CSR (2D) matrix.
    Here you can read how CSR sparse matrix works: https://en.wikipedia.org/wiki/Sparse_matrix

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
        raise NotImplementedError
        self.a = []
        self.ia = [0]
        self.ja = []
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.a = init_matrix_representation[2]
            self.ja = init_matrix_representation[1]
            prev = init_matrix_representation[0][0]
            if (prev != 0):
                for k in range(prev):
                    self.ia += [0]
            count = 0
            for i in init_matrix_representation[0]:
                if prev + 1 == i:
                    self.ia += [count]
                elif prev + 1 < i:
                    for k in range(prev, i):
                        self.ia += [count]
                count += 1
                prev = i
            self.ia += [count]
        elif isinstance(init_matrix_representation, np.ndarray):
            count = 0
            for i in range(len(init_matrix_representation)):
                for j in range(len(init_matrix_representation[i])):
                    if (init_matrix_representation[i][j] != 0):
                        self.a += [init_matrix_representation[i][j]]
                        count += 1
                        self.ja += [j]
                self.ia += [count]
            if self.a == []:
                self.ia = [0]
        else:
            raise ValueError

    @property
    def nnz(self):
        return len(self.a)

    def __getitem__(self, ind):
        if ind[0] >= len(self.ia)-1:
            return 0
        elif self.ia[ind[0] + 1] == self.ia[ind[0]]:
            return 0
        else:
            try:
                result = self.ja[self.ia[ind[0]]:self.ia[ind[0] + 1]].index(ind[1])
                return self.a[self.ia[ind[0]]+result]
            except ValueError:
                return 0

    def __setitem__(self, ind, value):
        if len(self.a) == 0:
            self.a += [value]
            if ind[0] != 0:
                for i in range(ind[0]):
                    self.ia += [0]
            self.ia += [1]
            self.ja += [ind[1]]
        elif self[ind] != 0:
            result = self.ja[self.ia[ind[0]]:self.ia[ind[0] + 1]].index(ind[1])
            self.a[self.ia[ind[0]]+result] = value
        else:
            if len(self.ia) - 1 <= ind[0]:
                self.ia += [self.ia[-1] + 1]
                self.ja += [ind[0]]
                self.a += [value]
                return
            for j in range(self.ia[ind[0]], self.ia[ind[0] + 1]):
                if self.ja[j] > ind[1]:
                    self.ja.insert(j, ind[1])
                    self.a.insert(j, value)
                    break
                elif j == self.ia[ind[0] + 1] - 1:
                    self.ja.insert(j+1, ind[1])
                    self.a.insert(j+1, value)
            for i in range(ind[0] + 1, len(self.ia)):
                self.ia[i] += 1

    def __add__(self, other):
        # print(self.ia[:10], self.ja[:10], self.a[0:10])
        # print(other.ia[:10], other.ja[:10], other.a[0:10])
        if not isinstance(other, CSRMatrix):
            raise TypeError
        if self.ia == other.ia and self.ja == other.ja:
            data = [self.a[i] + other.a[i] for i in range(len(self.a))]
            row = []
            i = 0
            while len(row) != len(data):
                for j in range(self.ia[i + 1] - self.ia[i]):
                    row += [i]
                i += 1
            return CSRMatrix((row, self.ja, data))
        if len(self.ia) == len(other.ia):
            row = []
            column = []
            data = []
            self_ind = 0
            other_ind = 0
            for i in range(1, len(self.ia)):
                while self_ind < self.ia[i]:
                    if other_ind >= other.ia[i] or self.ja[self_ind] < other.ja[other_ind]:
                        data += [self.a[self_ind]]
                        row += [i-1]
                        column += [self.ja[self_ind]]
                        self_ind += 1
                    elif self.ja[self_ind] > other.ja[other_ind]:
                        data += [other.a[other_ind]]
                        row += [i - 1]
                        column += [other.ja[other_ind]]
                        other_ind += 1
                    elif self.ja[self_ind] == other.ja[other_ind]:
                        data += [other.a[other_ind] + self.a[self_ind]]
                        row += [i - 1]
                        column += [self.ja[self_ind]]
                        self_ind += 1
                        other_ind += 1

                if other_ind < other.ia[i]:
                    while other_ind < other.ia[i]:
                        data += [other.a[other_ind]]
                        row += [i - 1]
                        column += [other.ja[other_ind]]
                        other_ind += 1
            print(row[:10], column[:10], data[:10])
            print(CSRMatrix((row, column, data)).ia[:20], other.ja[:20])
            return CSRMatrix((row, column, data))

    def __sub__(self, other):
        if not isinstance(other, CSRMatrix):
            raise TypeError
        if self.ia == other.ia and self.ja == other.ja:
            data = [self.a[i] - other.a[i] for i in range(len(self.a))]
            row = []
            i = 0
            while len(row) != len(data):
                for j in range(self.ia[i + 1] - self.ia[i]):
                    row += [i]
                i += 1
            return CSRMatrix((row, self.ja, data))

    def __mul__(self, other):
        if isinstance(other, CSRMatrix) and self.ia == other.ia and self.ja == other.ja:
            data = [self.a[i] * other.a[i] for i in range(len(self.a))]
            row = []
            i = 0
            while len(row) != len(data):
                for j in range(self.ia[i + 1] - self.ia[i]):
                    row += [i]
                i += 1
            return CSRMatrix((row, self.ja, data))
        elif isinstance(other, int) or isinstance(other, float):
            data = [self.a[i] * other for i in range(len(self.a))]
            row = []
            i = 0
            while len(row) != len(data):
                for j in range(self.ia[i + 1] - self.ia[i]):
                    row += [i]
                i += 1
            return CSRMatrix((row, self.ja, data))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            data = [self.a[i] / other for i in range(len(self.a))]
            row = []
            i = 0
            while len(row) != len(data):
                for j in range(self.ia[i + 1] - self.ia[i]):
                    row += [i]
                i += 1
            return CSRMatrix((row, self.ja, data))

    class DenseMatrix():
        def __init__(self, list_of_lists):
            self.matrix = list_of_lists
            self.shape = [len(list_of_lists), len(list_of_lists[0])]

        def __getitem__(self, ind):
            return self.matrix[ind[0]][ind[1]]

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        # print(self.a, self.ia, self.ja)
        result = []
        count = 0
        for i in range(1, len(self.ia)):
            row = [0 for k in range(max(self.ja) + 1)]
            for j in range(self.ia[i] - self.ia[i-1]):
                row[self.ja[count]] = self.a[count]
                count += 1
            result += [row]
        return CSRMatrix.DenseMatrix(result)
'''
init = ([0,1],[0,0],[1,2])
init = [[0,0,0,0],[5,8,0,0],[0,0,3,0],[0,6,0,0]]
init = np.arange(0,6).reshape(2,3)
init = ([0,0,1,2],[1,2,0,1],[1,2,3,4])
init0 = ([0,1,1,2],[1,0,2,2],[1,1,1,1])
m = CSRMatrix(init)
l = CSRMatrix(init0)
print(m.to_dense().matrix)
print(l.to_dense().matrix)
matr = m+l
print(matr.to_dense().matrix)
print(matr[1,3])
print(matr.nnz)
print((m+l).nnz)
print((m+m).nnz)
print(m[1,0])
m[0,0] = 33
print(m.to_dense().matrix)
print(m[0,0])
'''
