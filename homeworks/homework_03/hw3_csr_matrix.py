#!/usr/bin/env python
# coding: utf-8


import numpy as np


class CSRMatrix:

    def __init__(self, init_matrix_representation):
        self.row_ind = []
        self.column_ind = []
        self.data = []
        self._nnz = 0
        self.shape = []

        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.row_ind, self.column_ind, self.data = init_matrix_representation[0],\
                                                       init_matrix_representation[1],\
                                                       init_matrix_representation[2]
        elif isinstance(init_matrix_representation, np.ndarray):
            for i in range(init_matrix_representation.shape[0]):
                for j in range(init_matrix_representation.shape[1]):
                    if init_matrix_representation[i, j] != 0:
                        self.data.append(init_matrix_representation[i, j])
                        self.row_ind.append(i)
                        self.column_ind.append(j)
            self.shape = init_matrix_representation.shape
        else:
            raise ValueError
        self._nnz = len(self.data)

    nnz = property()

    @nnz.getter
    def nnz(self):
        return self._nnz

    def __getitem__(self, item):
        for i, j, data in zip(self.row_ind, self.column_ind, self.data):
            if item[0] == i and item[1] == j:
                return data
        return 0

    def __setitem__(self, key, value):
        for i, j, k in zip(self.row_ind, self.column_ind, range(len(self.data) + 1)):
            if key[0] == i and key[1] == j:
                if value == 0:
                    self.data.pop(k)
                    self.row_ind.pop(k)
                    self.column_ind.pop(k)
                    self._nnz -= 1
                else:
                    self.data[k] = value
                return
            elif key[0] == i and key[1] > j or key[0] > i:
                if k != len(self.data):
                    self.row_ind = self.row_ind[:k] + [key[0]] + self.row_ind[k:]
                    self.column_ind = self.column_ind[:k] + [key[1]] + self.column_ind[k:]
                    self.data = self.data[:k] + [value] + self.data[k:]
                self._nnz += 1
                return

        self.row_ind.append(key[0])
        self.column_ind.append(key[1])
        self.data.append(value)

    def __add__(self, other):
        return CSRMatrix(self._walk(other, action='add'))

    def __sub__(self, other):
        return CSRMatrix(self._walk(other, action='sub'))

    def __mul__(self, other):
        return CSRMatrix(self._walk(other, action='mul'))

    def _walk(self, other, action):
        i, j = 0, 0
        _len = len(self.row_ind)
        res_row, res_clmn, res_data = [], [], []

        while i < _len:
            if j == len(other.data):
                if action != 'mul':
                    res_row += self.row_ind[i:]
                    res_clmn += self.column_ind[i:]
                    res_data += self.data[i:]
                break
            if (other.row_ind[j] < self.row_ind[i]) or (other.row_ind[j] == self.row_ind[i] and
                                                        other.column_ind[j] < self.column_ind[i]):
                if action != 'mul':
                    res_row.append(other.row_ind[j])
                    res_clmn.append(other.column_ind[j])
                if action == 'add':
                    res_data.append(other.data[j])
                elif action == 'sub':
                    res_data.append(-other.data[j])
                j += 1
            elif other.row_ind[j] == self.row_ind[i] and other.column_ind[j] == self.column_ind[i]:
                if action == 'add':
                    if other.data[j] + self.data[i] == 0:
                        i, j = i + 1, j + 1
                        continue
                    res_data.append(other.data[j] + self.data[i])
                elif action == 'sub':
                    if self.data[i] - other.data[j] == 0:
                        i, j = i + 1, j + 1
                        continue
                    res_data.append(self.data[i] - other.data[j])
                else:
                    res_data.append(other.data[j] * self.data[i])
                res_row.append(other.row_ind[j])
                res_clmn.append(other.column_ind[j])
                i, j = i + 1, j + 1
            elif (other.row_ind[j] > self.row_ind[i]) or (other.row_ind[j] == self.row_ind[i] and
                                                          other.column_ind[j] > self.column_ind[i]):
                if action != 'mul':
                    res_row.append(self.row_ind[i])
                    res_clmn.append(self.column_ind[i])
                    res_data.append(self.data[i])
                i += 1

        if j < len(other.data) and action != 'mul':
            res_row += other.row_ind[j:]
            res_clmn += other.column_ind[j:]
            if action == 'add':
                res_data += other.data[j:]
            else:
                for i in other.data[j:]:
                    res_data.append(-i)
        return res_row, res_clmn, res_data

    def __rmul__(self, other):
        if other == 0:
            return CSRMatrix(tuple([[], [], []]))
        return CSRMatrix(tuple([self.row_ind, self.column_ind, [i * other for i in self.data]]))

    def __truediv__(self, other):
        if other == 0:
            return
        return CSRMatrix(tuple([self.row_ind, self.column_ind, [i / other for i in self.data]]))

    def __matmul__(self, other):
        if self.shape[1] != other.shape[0]:
            raise ValueError
        rows = {}
        columns = {}
        for i, v in enumerate(self.row_ind):
            if v in rows:
                rows[v][self.column_ind[i]] = self.data[i]
            else:
                rows[v] = {self.column_ind[i]: self.data[i]}

        for i, v in enumerate(other.column_ind):
            if v in columns:
                columns[v][other.row_ind[i]] = other.data[i]
            else:
                columns[v] = {other.row_ind[i]: other.data[i]}

        res_rows, res_columns, res_data = [], [], []
        for row, data_1 in rows.items():
            for col, data_2 in columns.items():
                res = sum({k: v * data_2[k] for k, v in data_1.items() if k in data_2}.values())
                if res:
                    res_rows.append(row)
                    res_columns.append(col)
                    res_data.append(res)
        return CSRMatrix((res_rows, res_columns, res_data))

    def to_dense(self):
        dense_matrix = np.zeros((self.row_ind[-1] + 1, self.column_ind[-1] + 1))
        for i, j, data in zip(self.row_ind, self.column_ind, self.data):
            dense_matrix[i, j] = data
        return dense_matrix
