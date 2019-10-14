#!/usr/bin/env python
# coding: utf-8

import numpy as np
import collections


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

    def __init__(self, init_matrix_representation=None):
        """
        :param init_matrix_representation: can be usual dense matrix
        or
        (row_ind, col, data) tuple with np.arrays,
            where data, row_ind and col_ind satisfy the relationship:
            a[row_ind[k], col_ind[k]] = data[k]
        """
        self.a = []
        self.ia = [0]
        self.ja = []
        self.shape = (0, 0)
        if init_matrix_representation is None:
            return
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.a = init_matrix_representation[2]
            self.ja = init_matrix_representation[1]
            self.shape = (max(init_matrix_representation[0]) + 1,
                          max(init_matrix_representation[1]) + 1)
            ia = init_matrix_representation[0]
            for i in range(len(self.a)):
                if self.a[i] == 0:
                    del self.a[i]
                    del self.ja[i]
                    del ia[i]
            c = collections.Counter()
            for item in ia:
                c[item] += 1
            nnz = 0
            for i in range(self.shape[0]):
                if i in c:
                    nnz += c[i]
                self.ia.append(nnz)
        elif isinstance(init_matrix_representation, np.ndarray):
            flag = True
            for i in range(len(init_matrix_representation)-1):
                flag = len(init_matrix_representation[i]) == len(init_matrix_representation[i+1])
            if flag:
                nnz = 0
                for i in range(len(init_matrix_representation)):
                    for j in range(len(init_matrix_representation[0])):
                        if init_matrix_representation[i][j] != 0:
                            self.a.append(init_matrix_representation[i][j])
                            nnz += 1
                            self.ja.append(j)
                    self.ia.append(nnz)
                self.shape = (len(init_matrix_representation), len(init_matrix_representation[0]))
            else:
                raise ValueError
        else:
            raise ValueError

    def __getitem__(self, item):
        row, col = item
        els_in_row = self.ia[row+1] - self.ia[row]
        if (0 <= row < self.shape[0]) and (0 <= col < self.shape[1]):
            if els_in_row == 0:
                return 0
            else:
                if col not in self.ja:
                    return 0
                else:
                    els_behind = self.ia[row]
                    for i in range(els_in_row):
                        if self.ja[els_behind + i] == col:
                            return self.a[els_behind + i]
                    return 0
        else:
            raise IndexError

    @property
    def nnz(self):
        return len(self.a)

    def __setitem__(self, key, value):
        row, col = key
        try:
            val = self.__getitem__(key)
        except IndexError:
            return
        if val != value:
            els_in_row = self.ia[row + 1] - self.ia[row]
            els_behind = self.ia[row]
            if value == 0:
                for i in range(els_in_row):
                    if self.ja[els_behind + i] == col:
                        del self.a[els_behind + i]
                        del self.ja[els_behind + i]
                        self.ia[row + 1:] = [k - 1 for k in self.ia[row + 1:]]
                        return
            else:
                if val != 0:
                    for i in range(els_in_row):
                        if self.ja[els_behind + i] == col:
                            self.a[els_behind + i] = value
                            return
                else:
                    self.ia[row + 1:] = [k + 1 for k in self.ia[row + 1:]]
                    if els_in_row > 0:
                        for i in range(els_in_row+1):
                            try:
                                if self.ja[els_behind + i] > col:
                                    self.ja.insert(els_behind + i, col)
                                    self.a.insert(els_behind + i, value)
                                    return
                            except IndexError:
                                self.ja.insert(els_behind + i, col)
                                self.a.insert(els_behind + i, value)

                    else:
                        self.ja.insert(els_behind, col)
                        self.a.insert(els_behind, value)
        else:
            return

    def to_dense(self):
        """
            Return dense representation of matrix (2D np.array).
        """
        dense_matr = np.zeros(self.shape)
        els_passed = 0
        for i in range(1, len(self.ia)):
            while els_passed < self.ia[i]:
                dense_matr[i - 1][self.ja[els_passed]] = self.a[els_passed]
                els_passed += 1
        return dense_matr

    def __add__(self, other):
        if self.shape == other.shape:
            result = CSRMatrix(np.zeros(self.shape))
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    result[i][j] = self.__getitem__([i, j]) + other[i, j]
            return CSRMatrix(result)
        else:
            raise ValueError

    def __sub__(self, other):
        if self.shape == other.shape:
            result = CSRMatrix(np.zeros(self.shape))
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    result[i][j] = self.__getitem__([i, j]) - other[i, j]
            return CSRMatrix(result)
        else:
            raise ValueError

    def __mul__(self, other):
        if self.shape == other.shape:
            result = CSRMatrix(np.zeros(self.shape))
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    result[i][j] = self.__getitem__([i, j]) * other[i, j]
            return CSRMatrix(result)
        else:
            raise ValueError

    def __rmul__(self, other):
        result = CSRMatrix()
        result.a = self.a.copy()
        result.ja = self.ja.copy()
        result.ia = self.ia.copy()
        result.shape = self.shape
        for i in range(len(result.a)):
            result.a[i] *= other
        return result

    def __truediv__(self, other):
        if other != 0:
            result = CSRMatrix()
            result.a = self.a.copy()
            result.ja = self.ja.copy()
            result.ia = self.ia.copy()
            result.shape = self.shape
            for i in range(len(result.a)):
                result.a[i] /= other
            return result
        else:
            raise ZeroDivisionError

    def transpose(self):
        c = collections.Counter()
        for item in self.ja:
            c[item] += 1
        sum = 0
        tmp_ia = [0]
        tmp_ja = []
        for i in range(self.shape[1]):
            if i in c:
                sum += c[i]
            tmp_ia.append(sum)
        for i in range(self.shape[0]):
            els_in_row = self.ia[i+1] - self.ia[i]
            for j in range(els_in_row):
                tmp_ja.append(i)
        prev = -1
        for index in range(self.shape[1]):
            for i in range(c[index]):
                old_index = self.ja[prev+1:].index(index) + prev + 1
                ja_val = self.ja[old_index]
                a_val = self.a[old_index]
                tmp_ja_val = tmp_ja[old_index]
                del self.ja[old_index]
                del self.a[old_index]
                del tmp_ja[old_index]
                prev += 1
                self.ja.insert(prev, ja_val)
                self.a.insert(prev, a_val)
                tmp_ja.insert(prev, tmp_ja_val)
        self.ia = tmp_ia
        self.ja = tmp_ja
        self.shape = self.shape[1], self.shape[0]
        return self

    def __matmul__(self, other):
        if self.shape[0] != other.shape[1]:
            raise ValueError
        result = CSRMatrix(np.zeros((self.shape[0], other.shape[1])))
        other.transpose()
        for i in range(self.shape[0]):
            for j in range(other.shape[0]):
                val = 0
                row_a = self.ja[self.ia[i]:self.ia[i+1]]
                row_b = other.ja[self.ia[j]:self.ia[j+1]]
                p1 = 0
                p2 = 0
                while p1 < len(row_a) and p2 < len(row_b):
                    if row_a[p1] == row_b[p2]:
                        val += self.__getitem__([i, row_a[p1]]) * other[j, row_b[p2]]
                        p1 += 1
                        p2 += 1
                    else:
                        if row_a[p1] > row_b[p2]:
                            p2 += 1
                        else:
                            p1 += 1
                result[i, j] = val
        return result
