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
        self.A = []
        self.IA = [0]
        self.JA = []
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            for i in range(len(init_matrix_representation[0])):
                self.A.append(init_matrix_representation[2][i])
                self.JA.append(init_matrix_representation[1][i])
            for i in range(max(init_matrix_representation[0])+1):
                self.IA.append(list(init_matrix_representation[0]).count(i)+self.IA[-1])
        elif isinstance(init_matrix_representation, np.ndarray):
            for i in range(len(init_matrix_representation)):
                count_elem_in_row = 0
                for j in range(len(init_matrix_representation[0])):
                    if init_matrix_representation[i][j] != 0:
                        count_elem_in_row += 1
                        self.JA.append(j)
                        self.A.append(init_matrix_representation[i][j])
                self.IA.append(count_elem_in_row + self.IA[-1])
        else:
            raise ValueError
        self.A = np.array(self.A)
        self.A.astype(float)
        self.IA = np.array(self.IA)
        self.JA = np.array(self.JA)

    @property
    def nnz(self):
        return int(self.IA[-1])

    def __add__(self, value):
        c = copy.deepcopy(self)
        ind = []
        for k in range(0, len(value.IA) - 1):
            for m in range(value.IA[k+1] - value.IA[k]):
                ind.append(k)
        for i in range(len(ind)):
                c[ind[i], value.JA[i]] += value.A[i]
        return c

    def __sub__(self, value):
        c = copy.deepcopy(self)
        ind = []
        for k in range(0, len(value.IA) - 1):
            for m in range(value.IA[k+1] - value.IA[k]):
                ind.append(k)
        for i in range(len(value.A)):
            c[ind[i], value.JA[i]] -= value.A[i]
        return c

    def __mul__(self, value):
        ind = []
        b = CSRMatrix(np.zeros((len(self.IA)-1, max(self.JA) + 1)))
        for k in range(0, len(value.IA) - 1):
            for m in range(value.IA[k+1] - value.IA[k]):
                ind.append(k)
        for i in range(len(value.A)):
            if value[ind[i], value.JA[i]] != 0 and self[ind[i], value.JA[i]] != 0:
                b[ind[i], value.JA[i]] = self[ind[i], value.JA[i]] * value.A[i]
        return b

    def __rmul__(self, value):
        c = copy.deepcopy(self)
        c.A = np.multiply(self.A, value, casting="unsafe")
        return c

    def __truediv__(self, value):
        if isinstance(value, float):
            c = copy.deepcopy(self)
            c.A = np.true_divide(self.A, value, casting="unsafe")
            return c
        ind = []
        b = CSRMatrix(np.zeros((len(self.IA)-1, max(self.JA) + 1), dtype=np.float32))
        for k in range(0, len(value.IA) - 1):
            for m in range(value.IA[k + 1] - value.IA[k]):
                ind.append(k)
        for i in range(len(value.A)):
            if value[ind[i], value.JA[i]] != 0 and self[ind[i], value.JA[i]] != 0:
                b[ind[i], value.JA[i]] = self[ind[i], value.JA[i]] / value.A[i]
        return b

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        count = 0
        if len(self.JA) == 0:
            return None
        a = np.zeros((len(self.IA)-1, int(max(self.JA)) + 1))
        for i in range(len(self.IA)-1):
            for j in range(self.IA[i+1] - self.IA[i]):
                a[i][int(self.JA[count])] = self.A[count]
                count += 1
        return a

    def __getitem__(self, key):
        i = key[0]
        j = key[1]
        pos1 = self.IA[i+1]
        pos0 = self.IA[i]
        ind = np.where(self.JA[pos0:pos1] == j)[0]
        if not len(ind):
            return 0
        elif len(ind) == 1:
            return self.A[int(ind) + int(pos0)]
        else:
            return self.A[int(ind[0]) + int(pos0)]

    def __setitem__(self, key, value):
        i = key[0]
        j = key[1]
        if self[key] != 0:
            if value != 0:
                pos1 = self.IA[i+1]
                pos0 = self.IA[i]
                ind = np.where(self.JA[pos0:pos1] == j)[0]
                self.A[ind + pos0] = value
            else:
                pos1 = self.IA[i+1]
                pos0 = self.IA[i]
                ind = np.where(self.JA[pos0:pos1] == j)[0]
                for k in range(i+1, len(self.IA)):
                    self.IA[k] -= 1
                self.A = np.delete(self.A, pos0 + ind)
                self.JA = np.delete(self.JA, pos0 + ind)
        else:
            if value == 0:
                return
            for k in range(i+1, len(self.IA)):
                self.IA[k] += 1
            pos1 = self.IA[i+1]
            pos0 = self.IA[i]
            for t in range(pos0, pos1):
                if len(self.JA) == 0:
                    self.JA = np.insert(self.JA, 0, j)
                    self.A = np.insert(self.A, 0, value)
                    return

                if pos1 > len(self.JA):
                    self.JA = np.insert(self.JA, pos1-1, j)
                    self.A = np.insert(self.A, pos1-1, value)
                    return

                if self.JA[t] > j:
                    self.JA = np.insert(self.JA, t, j)
                    self.A = np.insert(self.A, t, value)
                    return
            self.JA = np.insert(self.JA, t, j)
            self.A = np.insert(self.A, t, value)

    def __matmul__(self, other):
        '''Сложность O(N^3)'''
        if max(self.JA)+1 != len(other.IA)-1:
            raise ValueError
        c = CSRMatrix(np.zeros((len(self.IA)-1, max(other.JA) + 1)))
        inda = []
        for k in range(0, len(self.IA) - 1):
            for m in range(self.IA[k+1] - self.IA[k]):
                inda.append(k)
        indb = []
        for k in range(0, len(other.IA) - 1):
            for m in range(other.IA[k+1] - other.IA[k]):
                indb.append(k)
        temp = 0
        for i in range(len(self.IA)-1):
            for j in range(max(other.JA)+1):
                for k in range(len(other.IA)-1):
                    if self[i, k] & other[k, j]:
                        temp += self[i, k] * other[k, j]
                if temp != 0:
                    c[i, j] = temp
                    temp = 0
        return c
