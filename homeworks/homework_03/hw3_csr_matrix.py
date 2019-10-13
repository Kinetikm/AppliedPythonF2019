#!/usr/bin/env python
# coding: utf-8
from typing import List

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
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            l = []
            for i in range(3):
                l.append(len(init_matrix_representation[i]))
            if l[0] == l[1] == l[2]:
                self.cols = max(init_matrix_representation[1]) + 1
                self.rows = max(init_matrix_representation[0]) + 1
                self.a = []
                self.ia = [0] * (self.rows + 1)
                self.ja = []
                for i in range(l[0]):
                    if init_matrix_representation[2][i] != 0:
                        self.a.append(init_matrix_representation[2][i])
                        self.ja.append(init_matrix_representation[1][i])
                        for j in range(init_matrix_representation[0][i], self.rows):
                            self.ia[j + 1] += 1
                self._nnz = self.ia[len(self.ia) - 1]
            else:
                raise ValueError
        elif isinstance(init_matrix_representation, np.ndarray):
            self.cols = len(init_matrix_representation[0])
            self.rows = len(init_matrix_representation)
            self.a = []
            self.ia = [0] * (self.rows + 1)
            self.ja = []
            for i in range(len(init_matrix_representation)):
                if len(init_matrix_representation[i]) == self.cols:
                    for j in range(self.cols):
                        if init_matrix_representation[i][j] != 0:
                            self.a.append(init_matrix_representation[i][j])
                            self.ja.append(j)
                            for k in range(i, self.rows):
                                self.ia[k + 1] += 1
            self._nnz = self.ia[len(self.ia) - 1]
        else:
            raise ValueError

    @property
    def nnz(self):
        return self._nnz

    def __getitem__(self, item):
        row = item[0]
        col = item[1]
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.ia[row + 1] != self.ia[row]:
                pointer = self.ia[row]
                end = self.ia[row + 1]
                while pointer < end:
                    if self.ja[pointer] == col:
                        return self.a[pointer]
                    pointer += 1
                if pointer == end:
                    return 0
            else:
                return 0
        else:
            raise IndexError

    def insertion (self, row, col, value):
        if value != 0:
            self.ja.insert(self.ia[row], col)
            self.a.insert(self.ia[row], value)
            for i in range(row, self.rows):
                self.ia[i + 1] += 1
            self._nnz += 1

    def __setitem__(self, key, value):
        row = key[0]
        col = key[1]
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.ia[row] != self.ia[row + 1]:
                for i in range(self.ia[row], self.ia[row + 1]):
                    if self.ja[i] == col:
                        if value != 0:
                            self.a[i] = value
                        else:
                            if self.a[i] != 0:
                                del self.ja[i]
                                del self.a[i]
                                for j in range(row, self.rows):
                                    self.ia[j + 1] -= 1
                                self._nnz -= 1
                        return
                    if self.ja[i] < col:
                        self.insertion(row, col, value)
                        return
            else:
                self.insertion(row, col, value)
        else:
            raise IndexError

    def create(self, rows, cols):
        if isinstance(self, CSRMatrix):
            ans = CSRMatrix(([0], [0], [0]))
            ans.rows = rows
            ans.cols = cols
            ans.ia = [0] * (rows + 1)
            ans._nnz = 0
            return ans
        else:
            raise TypeError

    def operation(self, other, sign):
        if isinstance(other, CSRMatrix):
            if self.cols == other.cols > 0 and self.rows == other.rows > 0:
                ans = self.create(self.rows, self.cols)
                for row in range(other.rows):
                    p1 = self.ia[row]
                    p2 = other.ia[row]
                    end1 = self.ia[row + 1]
                    end2 = other.ia[row + 1]
                    while p1 < end1 and p2 < end2:
                        if self.ja[p1] < other.ja[p2]:
                            ans.a.append(self.a[p1])
                            ans.ja.append(self.ja[p1])
                            for k in range(row, ans.rows):
                                ans.ia[k + 1] += 1
                            p1 += 1
                        elif self.ja[p1] > other.ja[p2]:
                            ans.ja.append(other.ja[p2])
                            if sign == '+':
                                ans.a.append(other.a[p2])
                            if sign == '-':
                                ans.a.append(-1 * other.a[p2])
                            for k in range(row, ans.rows):
                                ans.ia[k + 1] += 1
                            p2 += 1
                        elif self.ja[p1] == other.ja[p2]:
                            s = 0
                            if sign == '+':
                                s = self.a[p1] + other.a[p2]
                            if sign == '-':
                                s = self.a[p1] - other.a[p2]
                            if s != 0:
                                ans.a.append(s)
                                ans.ja.append(self.ja[p1])
                                for k in range(row, ans.rows):
                                    ans.ia[k + 1] += 1
                            p1 += 1
                            p2 += 1
                    for i in range(p1, end1):
                        ans.a.append(self.a[p1])
                        ans.ja.append(self.ja[p1])
                        for k in range(row, ans.rows):
                            ans.ia[k + 1] += 1
                    for i in range(p2, end2):
                        if sign == '+':
                            ans.a.append(other.a[p2])
                        if sign == '-':
                            ans.a.append(-1 * other.a[p2])
                        ans.ja.append(other.ja[p2])
                        for k in range(row, ans.rows):
                            ans.ia[k + 1] += 1
                ans._nnz = ans.ia[len(ans.ia) - 1]
                return ans
            else:
                raise IndexError
        else:
            raise TypeError

    def __add__(self, other):
        return self.operation(other, '+')

    def __sub__(self, other):
        return self.operation(other, '-')

    def __mul__(self, other):
        ans = self.create(self.rows, self.cols)
        if isinstance(other, CSRMatrix):
            if self.rows > 0 and self.cols > 0:
                for row in range(other.rows):
                    p1 = self.ia[row]
                    p2 = other.ia[row]
                    end1 = self.ia[row + 1]
                    end2 = other.ia[row + 1]
                    while p1 < end1 and p2 < end2:
                        if self.ja[p1] > other.ja[p2]:
                            p2 += 1
                        elif self.ja[p1] < other.ja[p2]:
                            p1 += 1
                        else:
                            ans.a.append(self.a[p1] * other.a[p2])
                            ans.ja.append(self.ja[p1])
                            for k in range(row, ans.rows):
                                ans.ia[k + 1] += 1
                            p1 += 1
                            p2 += 1
                ans._nnz = ans.ia[len(ans.ia) - 1]
                return ans
            else:
                raise IndexError
        else:
            raise TypeError

    def __rmul__(self, other):
        ans = self.create(self.rows, self.cols)
        if isinstance(other, (float, int)):
            if self.rows > 0 and self.cols > 0:
                if other == 0:
                    ans.a = []
                    ans.ja = []
                    ans.ia = [0] * (self.rows + 1)
                elif other != 0:
                    ans.ia = self.ia.copy()
                    ans.ja = self.ja.copy()
                    for elem in self.a:
                        ans.a.append(elem * other)
                ans._nnz = ans.ia[len(ans.ia) - 1]
                return ans
            else:
                raise IndexError
        else:
            raise TypeError

    def __truediv__(self, other):
        ans = self.create(self.rows, self.cols)
        if isinstance(other, (float, int)):
            if other == 0:
                raise ZeroDivisionError
            elif other != 0:
                ans.ia = self.ia.copy()
                ans.ja = self.ja.copy()
                for elem in self.a:
                    ans.a.append(elem / other)
            ans._nnz = ans.ia[len(ans.ia) - 1]
            return ans
        else:
            raise TypeError

    def __matmul__(self, other):
        if isinstance(other, CSRMatrix):
            if self.cols == other.rows:
                ans = self.create(self.rows, other.cols)
                d = {}
                for row_b in range(other.rows):
                    for elem_b in range(other.ia[row_b], other.ia[row_b + 1]):
                        if not other.ja[elem_b] in d.keys():
                            d[other.ja[elem_b]] = {}
                        d[other.ja[elem_b]][row_b] = other.a[elem_b]
                for row_a in range(self.rows):
                    for col_b in sorted(d.keys()):
                        s = 0
                        for elem_a in range(self.ia[row_a], self.ia[row_a + 1]):
                            col_a = self.ja[elem_a]
                            if col_a in d[col_b].keys():
                                s += self.a[elem_a] * d[col_b][col_a]
                        if s != 0:
                            ans.a.append(s)
                            ans.ja.append(col_b)
                            for k in range(row_a, ans.rows):
                                ans.ia[k + 1] += 1
                ans._nnz = ans.ia[len(ans.ia) - 1]
                return ans
            else:
                raise ValueError
        else:
            raise TypeError

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        dense = np.zeros((self.rows, self.cols))
        pointer = 0
        for i in range(self.rows):
            while pointer < self.ia[i + 1]:
                dense[i, self.ja[pointer]] = self.a[pointer]
                pointer += 1
        return dense


def get_next_elem(n, coordinate):
    if len(coordinate) == n:
        for i in range(len(coordinate) - 1, -1, -1):
            coordinate[i] += 1
            if coordinate[i] < 2:
                return
            coordinate[i] = 0
    else:
        raise ValueError
