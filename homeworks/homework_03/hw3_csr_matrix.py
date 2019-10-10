# !/usr/bin/env python
# coding: utf-8


import numpy as np
import copy


class CSRMatrix:

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
            n = 0
            for i in range(max(init_matrix_representation[0]) + 1):
                n += list(init_matrix_representation[0]).count(i)
                self.IA.append(n)
            self.A = list(init_matrix_representation[2])
            self.JA = list(init_matrix_representation[1])
            self.max_column = max(init_matrix_representation[1]) + 1

        elif isinstance(init_matrix_representation, np.ndarray):
            n = 0
            for i, line in enumerate(init_matrix_representation):
                for j, item in enumerate(line):
                    if item:
                        self.A.append(item)
                        self.JA.append(j)
                        n += 1
                self.IA.append(n)
            self.max_column = len(init_matrix_representation[0])

        else:
            raise ValueError

        self._NNZ = self.IA[-1]

    @property
    def nnz(self):
        return self._NNZ

    def __getitem__(self, ind):
        try:
            i = ind[0]
            j = ind[1]
            k = self.JA[self.IA[i]:self.IA[i + 1]].index(j) + self.IA[i]
            return self.A[k]
        except ValueError:
            return 0

    def __setitem__(self, ind, value):
        i = ind[0]
        j = ind[1]
        if self[i, j]:
            k = self.JA[self.IA[i]:self.IA[i + 1]].index(j) + self.IA[i]
            self.A[k] = value
        else:
            if (self.IA[i] - self.IA[i + 1]) != 0:
                for l, item in enumerate(self.JA[self.IA[i]:self.IA[i + 1]]):
                    if item > j:
                        index = l + self.IA[i]
                        self.JA.insert(index, j)
                        self.A.insert(index, value)
                        self.IA[i + 1:] = [k + 1 for k in self.IA[i + 1:]]
                        break
            else:
                self.JA.insert(self.IA[i], j)
                self.A.insert(self.IA[i], value)
                self.IA[i + 1:] = [k + 1 for k in self.IA[i + 1:]]

    def __add__(self, other):
        if (self.max_column != other.max_column) or (len(self.IA) != len(other.IA)):
            raise ValueError
        else:
            row = []
            column = []
            data = []
            for i in range(len(self.IA) - 1):
                d = {}
                for k in range(self.IA[i], self.IA[i + 1]):
                    d[self.JA[k]] = self.A[k]
                for l in range(other.IA[i], other.IA[i + 1]):
                    if other.JA[l] in d:
                        d[other.JA[l]] += other.A[l]
                    else:
                        d[other.JA[l]] = other.A[l]

                for j, item in d.items():
                    if item:
                        row.append(i)
                        column.append(j)
                        data.append(item)
            return CSRMatrix((row, column, data))

    def __sub__(self, other):
        if (self.max_column != other.max_column) or (len(self.IA) != len(other.IA)):
            raise ValueError
        else:
            row = []
            column = []
            data = []
            for i in range(len(self.IA) - 1):
                d = {}
                for k in range(self.IA[i], self.IA[i + 1]):
                    d[self.JA[k]] = self.A[k]
                for l in range(other.IA[i], other.IA[i + 1]):
                    if other.JA[l] in d:
                        d[other.JA[l]] -= other.A[l]
                    else:
                        d[other.JA[l]] = -other.A[l]

                for j, item in d.items():
                    if item:
                        row.append(i)
                        column.append(j)
                        data.append(item)
            return CSRMatrix((row, column, data))

    def __mul__(self, other):
        row = []
        column = []
        data = []
        if isinstance(other, (float, int)):
            for i in range(len(self.IA) - 1):
                for k in range(self.IA[i], self.IA[i + 1]):
                    row.append(i)
                    column.append(self.JA[k])
                    data.append(self.A[k] * 2.5)
            return CSRMatrix((row, column, data))
        else:
            if (self.max_column != other.max_column) or (len(self.IA) != len(other.IA)):
                raise ValueError
            else:
                for i in range(len(self.IA) - 1):
                    d1 = {}
                    d2 = {}
                    for k in range(self.IA[i], self.IA[i + 1]):
                        d1[self.JA[k]] = self.A[k]
                    for l in range(other.IA[i], other.IA[i + 1]):
                        d2[other.JA[l]] = other.A[l]
                    for j in d1:
                        if j in d2:
                            row.append(i)
                            column.append(j)
                            data.append(d2[j] * d1[j])
                return CSRMatrix((row, column, data))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, a):
        if isinstance(a, (float, int)):
            row = []
            col = []
            data = []
            for i in range(len(self.IA) - 1):
                for k in range(self.IA[i], self.IA[i + 1]):
                    row.append(i)
                    col.append(self.JA[k])
                    data.append(self.A[k] / a)
            return CSRMatrix((row, col, data))

    def dot(self, other):
        other = CSRMatrix(other.to_dense().transpose())
        if max(other.JA) != max(self.JA):
            raise ValueError
        else:
            row = []
            col = []
            data = []
            for i in range(len(self.IA) - 1):
                for l in range(len(other.IA) - 1):
                    dic = {}
                    dic1 = {}
                    s = 0
                    for k in range(self.IA[i], self.IA[i + 1]):
                        dic[self.JA[k]] = self.A[k]
                    for k in range(other.IA[l], other.IA[l + 1]):
                        dic1[other.JA[k]] = other.A[k]

                    for j in dic1:
                        if j in dic:
                            s += dic[j] * dic1[j]
                    if s:
                        row.append(i)
                        col.append(l)
                        data.append(s)
            return CSRMatrix((row, col, data))

    def __matmul__(self, other):

        other = CSRMatrix(other.to_dense().transpose())
        if max(other.JA) != max(self.JA):
            raise ValueError
        else:
            row = []
            col = []
            data = []
            for i in range(len(self.IA) - 1):
                for l in range(len(other.IA) - 1):
                    d = {}
                    d1 = {}
                    s = 0
                    for k in range(self.IA[i], self.IA[i + 1]):
                        d[self.JA[k]] = self.A[k]
                    for k in range(other.IA[l], other.IA[l + 1]):
                        d1[other.JA[k]] = other.A[k]

                    for j in d1:
                        if j in d:
                            s += d[j] * d1[j]
                    if s:
                        row.append(i)
                        col.append(l)
                        data.append(s)
            return CSRMatrix((row, col, data))

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        dense_matrix = np.zeros((len(self.IA) - 1, self.max_column))
        for i in range(len(self.IA) - 1):
            for k in range(self.IA[i], self.IA[i + 1]):
                dense_matrix[i, self.JA[k]] = self.A[k]
        return dense_matrix
