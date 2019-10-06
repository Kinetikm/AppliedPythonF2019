#!/usr/bin/env python
# coding: utf-8
import numpy as np
from copy import deepcopy


class CSRMatrix:

    operation = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
        "**": lambda x, y: x ** y
    }

    def __init__(self, init_matrix_representation):
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.row = deepcopy(init_matrix_representation[0])
            self.col = deepcopy(init_matrix_representation[1])
            self.data = deepcopy(init_matrix_representation[2])
            self.rn = max(self.row) + 1
            self.cn = max(self.col) + 1
        elif isinstance(init_matrix_representation, np.ndarray):
            self.row = []
            self.col = []
            self.data = []
            for rn, row in enumerate(init_matrix_representation):
                for cn, val in enumerate(row):
                    if val != 0:
                        self.row += [rn]
                        self.col += [cn]
                        self.data += [val]
            self.rn = len(init_matrix_representation)
            self.cn = len(init_matrix_representation[0])
        elif isinstance(init_matrix_representation, CSRMatrix):
            self.row = init_matrix_representation.row
            self.col = init_matrix_representation.col
            self.data = init_matrix_representation.data
            self.rn = init_matrix_representation.rn
            self.cn = init_matrix_representation.cn
        else:
            raise ValueError
        self._nnz = len(self.data)

    nnz = property()

    @nnz.setter
    def nnz(self, value):
        if value != len(self.data):
            raise AttributeError
        self._nnz = value

    @nnz.getter
    def nnz(self):
        return self._nnz

    def to_dense(self):
        result = np.zeros((self.rn, self.cn))
        for i, j, v in zip(self.row, self.col, self.data):
            result[i, j] = v
        return result

    def __getitem__(self, index):
        for ind, val in enumerate(self.row):
            if val == index[0] and self.col[ind] == index[1]:
                return self.data[ind]
        return 0

    def __setitem__(self, index, value):
        fi = 0
        if len(
                self.data) == 0 or self.row[fi] > index[0] and self.col[fi] > index[1]:
            if value != 0:
                self.row = [index[0]] + self.row
                self.col = [index[1]] + self.col
                self.data = [value] + self.data
            return
        while fi < len(self.data) - \
                1 and self.row[fi] < index[0] and self.col[fi] < index[1]:
            fi += 1
        if self.row[fi] == index[0] and self.col[fi] == index[1]:
            if value == 0:
                self.row = self.row[:fi] + self.row[fi + 1:]
                self.col = self.col[:fi] + self.col[fi + 1:]
                return
            self.data[fi] = value
        if value != 0:
            self.row = self.row[:fi] + [index[0]] + self.row[fi:]
            self.col = self.col[:fi] + [index[1]] + self.col[fi:]
            self.data = self.data[:fi] + [value] + self.data[fi:]

    def __add__(self, other):
        if isinstance(other, CSRMatrix):
            return self.get_sum(other, "+")

    def get_sum(self, other, sign):
        if len(other.data) == 0:
            return CSRMatrix(self)
        if len(self.data) == 0:
            return CSRMatrix(other)
        row = []
        col = []
        data = []
        cur_ind_a, cur_ind_b = 0, 0
        while cur_ind_a < self.nnz and cur_ind_b < other.nnz:
            if self.row[cur_ind_a] < other.row[cur_ind_b] or \
                    self.row[cur_ind_a] == other.row[cur_ind_b] \
                    and self.col[cur_ind_a] < other.col[cur_ind_b]:
                row += [self.row[cur_ind_a]]
                col += [self.col[cur_ind_a]]
                data += [self.operation[sign](self.data[cur_ind_a], 0)]
                cur_ind_a += 1
            elif self.row[cur_ind_a] > other.row[cur_ind_b] or \
                    self.row[cur_ind_a] == other.row[cur_ind_b] and \
                    self.col[cur_ind_a] > other.col[cur_ind_b]:
                row += [other.row[cur_ind_b]]
                col += [other.col[cur_ind_b]]
                data += [self.operation[sign](0, other.data[cur_ind_b])]
                cur_ind_b += 1
            elif self.row[cur_ind_a] == other.row[cur_ind_b] \
                    and self.col[cur_ind_a] == other.col[cur_ind_b]:
                val = self.operation[sign](
                    self.data[cur_ind_a], other.data[cur_ind_b])
                if val != 0:
                    data += [val]
                    row += [other.row[cur_ind_b]]
                    col += [other.col[cur_ind_b]]
                cur_ind_a += 1
                cur_ind_b += 1

        while cur_ind_a < self.nnz:
            row += [self.row[cur_ind_a]]
            col += [self.col[cur_ind_a]]
            data += [self.operation[sign](self.data[cur_ind_a], 0)]
            cur_ind_a += 1

        while cur_ind_b < other.nnz:
            row += [other.row[cur_ind_b]]
            col += [other.col[cur_ind_b]]
            data += [self.operation[sign](0, other.data[cur_ind_b])]
            cur_ind_b += 1

        return CSRMatrix((row, col, data))

    def __sub__(self, other):
        if isinstance(other, CSRMatrix):
            return self.get_sum(other, "-")

        return self.alpha_result(other, "-")

    def __mul__(self, other):
        if isinstance(other, CSRMatrix):
            return self.get_sum(other, "*")
        result = CSRMatrix((
            deepcopy(self.row),
            deepcopy(self.col),
            deepcopy(self.data),
        ))
        result.alpha_result(other, "*")
        return result

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, CSRMatrix):
            return
        if other == 0:
            raise ZeroDivisionError
        result = CSRMatrix((
            deepcopy(self.row),
            deepcopy(self.col),
            deepcopy(self.data),
        ))
        result.alpha_result(other, "/")
        return result

    def __pow__(self, other):
        if isinstance(other, CSRMatrix):
            return
        return self.alpha_result(other, "*")

    def __matmul__(self, other):
        data1, data2 = {}, {}
        if self.cn != other.rn:
            raise ValueError
        for ind, val in enumerate(self.row):
            if val in data1:
                data1[val][self.col[ind]] = self.data[ind]
            else:
                data1[val] = {self.col[ind]: self.data[ind]}

        for ind, val in enumerate(other.col):
            if val in data2:
                data2[val][other.row[ind]] = other.data[ind]
            else:
                data2[val] = {other.row[ind]: other.data[ind]}
        row = []
        col = []
        data = []
        for i, val_frs in data1.items():
            for j, val_sec in data2.items():
                cell = sum(
                    {key: val * val_sec[key] for key, val in val_frs.items() if key in val_sec}.values())

                if cell != 0:
                    row += [i]
                    col += [j]
                    data += [cell]
        res = CSRMatrix((row, col, data))
        return res

    def alpha_result(self, alpha, sign):
        for i, val in enumerate(self.data):
            self.data[i] = self.operation[sign](val, alpha)
