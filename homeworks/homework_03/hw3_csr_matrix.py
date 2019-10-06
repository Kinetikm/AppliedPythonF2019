#!/usr/bin/env python
# coding: utf-8

import numpy as np


class CSRMatrix:
    def __init__(self, init_matrix):
        if isinstance(init_matrix, tuple) and len(init_matrix) == 3:
            row_ind, col_ind, data = init_matrix
            m, n = max(row_ind)+1, max(col_ind)+1
            num_of_elements = len(data)
            matrix = np.zeros((m, n))
            for i in range(num_of_elements):
                matrix[row_ind[i], col_ind[i]] = data[i]
            self.__init_from_np(matrix)
            self.__nnz = len(self.data)
        elif isinstance(init_matrix, np.ndarray):
            self.__init_from_np(init_matrix)
            self.__nnz = len(self.data)
        else:
            raise ValueError

    def __init_from_np(self, init_matrix):
        m, n = init_matrix.shape
        self.data = []
        self.rows = [0]
        self.colounms = []
        for i in range(0, m):
            self.rows.append(self.rows[i])
            for j in range(n):
                if init_matrix[i][j]:
                    self.data.append(init_matrix[i][j])
                    self.colounms.append(j)
                    self.rows[i+1] += 1

    @classmethod
    def empty_matrix(cls, num_of_rows):
        return cls(np.zeros((num_of_rows, 1)))

    @property
    def nnz(self):
        return self.__nnz

    def __getitem__(self, coor):
        i, j = coor
        try:
            k = self.colounms.index(j, self.rows[i], self.rows[i+1])
        except ValueError:
            return 0
        return self.data[k]

    def __setitem__(self, coor, value):
        i, j = coor
        if value and self[coor]:
            k = self.colounms.index(j, self.rows[i], self.rows[i+1])
            self.data[k] = value
        elif value and not self[coor]:
            try:
                k = self.colounms.index(j, self.rows[i], self.rows[i+1])
            except ValueError:
                self.data.insert(self.rows[i+1], value)
                self.colounms.insert(self.rows[i+1], j)
            else:
                self.data.insert(k, value)
                self.colounms.insert(k, j)
            for k in range(i+1, len(self.rows)):
                self.rows[k] += 1
            self.__nnz += 1
        elif self[coor]:
            k = self.colounms.index(j, self.rows[i], self.rows[i+1])
            self.data.pop(k)
            self.colounms.pop(k)
            for k in range(i+1, len(self.rows)):
                self.rows[k] -= 1
            self.__nnz -= 1

    def __calculator(self, value1, value2, oper):
        if oper == '+':
            return value1 + value2
        elif oper == '-':
            return value1 - value2

    def __calcul_add_or_sub(self, other, oper):
        num_of_rows = len(self.rows) - 1
        result = CSRMatrix.empty_matrix(num_of_rows)
        for i in range(1, len(self.rows)):
            for j in self.colounms[self.rows[i-1]:self.rows[i]]:
                result[i-1, j] = self[i-1, j]
        for i in range(1, len(other.rows)):
            for j in other.colounms[other.rows[i-1]:other.rows[i]]:
                result[i-1, j] = self.__calculator(result[i-1, j], other[i-1, j], oper)
        return result

    def __add__(self, other):
        return self.__calcul_add_or_sub(other, '+')

    def __sub__(self, other):
        return self.__calcul_add_or_sub(other, '-')

    def __mul__(self, other):
        num_of_rows = len(self.rows) - 1
        result = CSRMatrix.empty_matrix(num_of_rows)
        if isinstance(other, CSRMatrix):
            for i in range(1, len(self.rows)):
                for j in self.colounms[self.rows[i-1]:self.rows[i]]:
                    result[i-1, j] = self[i-1, j] * other[i-1, j]
        else:
            for i in range(1, len(self.rows)):
                for j in self.colounms[self.rows[i-1]:self.rows[i]]:
                    result[i-1, j] = self[i-1, j] * other
        return result

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        return self * (1/other)

    def __matmul__(self, other):
        return CSRMatrix(self.to_dense() @ other.to_dense())

    def to_dense(self):
        m, n = len(self.rows)-1, max(self.colounms)+1
        result = np.zeros((m, n))
        for i in range(m):
            for j in range(self.rows[i], self.rows[i+1]):
                result[i][self.colounms[j]] = self.data[j]
        return result
