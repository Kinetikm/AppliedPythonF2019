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
            self.rows = deepcopy(init_matrix_representation[0])
            self.columns = deepcopy(init_matrix_representation[1])
            self.d = deepcopy(init_matrix_representation[2])
            self.rn = max(self.rows) + 1
            self.cn = max(self.columns) + 1
        elif isinstance(init_matrix_representation, np.ndarray):
            self.rows = []
            self.columns = []
            self.d = []
            for rn, rows in enumerate(init_matrix_representation):
                for cn, val in enumerate(rows):
                    if val != 0:
                        self.rows += [rn]
                        self.columns += [cn]
                        self.d += [val]
            self.rn = len(init_matrix_representation)
            self.cn = len(init_matrix_representation[0])
        elif isinstance(init_matrix_representation, CSRMatrix):
            self.rows = init_matrix_representation.rows
            self.columns = init_matrix_representation.columns
            self.d = init_matrix_representation.d
            self.rn = init_matrix_representation.rn
            self.cn = init_matrix_representation.cn
        else:
            raise ValueError
        self._nnz = len(self.d)

    nnz = property()

    @nnz.setter
    def nnz(self, value):
        if value != len(self.d):
            raise AttributeError
        self._nnz = value

    @nnz.getter
    def nnz(self):
        return self._nnz

    def to_dense(self):
        result = np.zeros((self.rn, self.cn))
        for i, j, val in zip(self.rows, self.columns, self.d):
            result[i, j] = val
        return result

    def __getitem__(self, index):
        for i, val in enumerate(self.rows):
            if val == index[0] and self.columns[i] == index[1]:
                return self.d[i]
        return 0

    def __setitem__(self, index, value):
        k = 0
        if len(self.d) == 0 or self.rows[k] > index[0] and self.columns[k] > index[1]:
            if value != 0:
                self.rows = [index[0]] + self.rows
                self.columns = [index[1]] + self.columns
                self.d = [value] + self.d
            return
        while k < len(self.d) - 1 and \
         self.rows[k] < index[0] and self.columns[k] < index[1]:
            k += 1
        if self.rows[k] == index[0] and self.columns[k] == index[1]:
            if value == 0:
                self.rows = self.rows[:k] + self.rows[k + 1:]
                self.columns = self.columns[:k] + self.columns[k + 1:]
                return
            self.d[k] = value
        if value != 0:
            self.rows = self.rows[:k] + [index[0]] + self.rows[k:]
            self.columns = self.columns[:k] + [index[1]] + self.columns[k:]
            self.d = self.d[:k] + [value] + self.d[k:]

    def __add__(self, other):
        if isinstance(other, CSRMatrix):
            return self.get_sum(other, "+")

    def get_sum(self, other, sign):
        if len(other.d) == 0:
            return CSRMatrix(self)
        if len(self.d) == 0:
            return CSRMatrix(other)
        r = []
        c = []
        d = []
        a_ind, b_ind = 0, 0
        while a_ind < self.nnz and b_ind < other.nnz:
            if self.rows[a_ind] < other.rows[b_ind] or \
                    self.rows[a_ind] == other.rows[b_ind] \
                    and self.columns[a_ind] < other.columns[b_ind]:
                r += [self.rows[a_ind]]
                c += [self.columns[a_ind]]
                d += [self.operation[sign](self.d[a_ind], 0)]
                a_ind += 1
            elif self.rows[a_ind] > other.rows[b_ind] or \
                    self.rows[a_ind] == other.rows[b_ind] and \
                    self.columns[a_ind] > other.columns[b_ind]:
                r += [other.rows[b_ind]]
                c += [other.columns[b_ind]]
                d += [self.operation[sign](0, other.d[b_ind])]
                b_ind += 1
            elif self.rows[a_ind] == other.rows[b_ind] \
                    and self.columns[a_ind] == other.columns[b_ind]:
                val = self.operation[sign](
                    self.d[a_ind], other.d[b_ind])
                if val != 0:
                    d += [val]
                    r += [other.rows[b_ind]]
                    c += [other.columns[b_ind]]
                a_ind += 1
                b_ind += 1

        while a_ind < self.nnz:
            r += [self.rows[a_ind]]
            c += [self.columns[a_ind]]
            d += [self.operation[sign](self.d[a_ind], 0)]
            a_ind += 1

        while b_ind < other.nnz:
            r += [other.rows[b_ind]]
            c += [other.columns[b_ind]]
            d += [self.operation[sign](0, other.d[b_ind])]
            b_ind += 1

        return CSRMatrix((r, c, d))

    def __sub__(self, other):
        if isinstance(other, CSRMatrix):
            return self.get_sum(other, "-")

        return self.alpha_result(other, "-")

    def __mul__(self, other):
        if isinstance(other, CSRMatrix):
            return self.get_sum(other, "*")
        result = CSRMatrix((
            deepcopy(self.rows),
            deepcopy(self.columns),
            deepcopy(self.d),
        ))
        result.alpha_result(other, "*")
        return result

    __rmul__ = __mul__

    def __pow__(self, other):
        if isinstance(other, CSRMatrix):
            return
        return self.alpha_result(other, "*")

    def __truediv__(self, other):
        if isinstance(other, CSRMatrix):
            return
        if other == 0:
            raise ZeroDivisionError
        result = CSRMatrix((
            deepcopy(self.rows),
            deepcopy(self.columns),
            deepcopy(self.d),
        ))
        result.alpha_result(other,  "/")
        return result

    def __matmul__(self, other):
        dict_num_1, dict_num_2 = {}, {}
        if self.cn != other.rn:
            raise ValueError
        for ind, val in enumerate(self.rows):
            if val in dict_num_1:
                dict_num_1[val][self.columns[ind]] = self.d[ind]
            else:
                dict_num_1[val] = {self.columns[ind]: self.d[ind]}

        for ind, val in enumerate(other.columns):
            if val in dict_num_2:
                dict_num_2[val][other.rows[ind]] = other.d[ind]
            else:
                dict_num_2[val] = {other.rows[ind]: other.d[ind]}
        r = []
        c = []
        d = []
        for i, val_frs in dict_num_1.items():
            for j, val_sec in dict_num_2.items():
                cell = sum(
                    {key: val * val_sec[key] for key, val in val_frs.items() if key in val_sec}.values())

                if cell != 0:
                    r += [i]
                    c += [j]
                    d += [cell]
        res = CSRMatrix((r, c, d))
        return res

    def alpha_result(self, alpha, sign):
        for i, val in enumerate(self.d):
            self.d[i] = self.operation[sign](val, alpha)
