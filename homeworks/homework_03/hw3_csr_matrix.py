#!/usr/bin/env python
# coding: utf-8

from copy import deepcopy
import numpy as np


class CSRMatrix:
    operation = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
            "**": lambda x, y: x ** y
        }

    def __init__(self, init_matrix_representation):
        if (isinstance(init_matrix_representation, tuple) and
                len(init_matrix_representation) == 3):
            self.r = deepcopy(init_matrix_representation[0])
            self.c = deepcopy(init_matrix_representation[1])
            self.d = deepcopy(init_matrix_representation[2])
            self.rn = max(self.r) + 1
            self.cn = max(self.c) + 1
        elif isinstance(init_matrix_representation, np.ndarray):
            self.r = []
            self.c = []
            self.d = []
            for rn, r in enumerate(init_matrix_representation):
                for cn, val in enumerate(r):
                    if val != 0:
                        self.r += [rn]
                        self.c += [cn]
                        self.d += [val]
            self.rn = len(init_matrix_representation)
            self.cn = len(init_matrix_representation[0])
        elif isinstance(init_matrix_representation, CSRMatrix):
            self.r = init_matrix_representation.r
            self.c = init_matrix_representation.c
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
        for i, j, val in zip(self.r, self.c, self.d):
            result[i, j] = val
        return result

    def __getitem__(self, index):
        for i, val in enumerate(self.r):
            if val == index[0] and self.c[i] == index[1]:
                return self.d[i]
        return 0

    def __setitem__(self, index, value):
        k = 0
        if len(self.d) == 0 or self.r[k] > index[0] and self.c[k] > index[1]:
            if value != 0:
                self.r = [index[0]] + self.r
                self.c = [index[1]] + self.c
                self.d = [value] + self.d
            return
        while k < len(self.d) - \
                1 and self.r[k] < index[0] and self.c[k] < index[1]:
            k += 1
        if self.r[k] == index[0] and self.c[k] == index[1]:
            if value == 0:
                self.r = self.r[:k] + self.r[k + 1:]
                self.c = self.c[:k] + self.c[k + 1:]
                return
            self.d[k] = value
        if value != 0:
            self.r = self.r[:k] + [index[0]] + self.r[k:]
            self.c = self.c[:k] + [index[1]] + self.c[k:]
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
            if self.r[a_ind] < other.r[b_ind] or \
                    self.r[a_ind] == other.r[b_ind] \
                    and self.c[a_ind] < other.c[b_ind]:
                r += [self.r[a_ind]]
                c += [self.c[a_ind]]
                d += [self.operation[sign](self.d[a_ind], 0)]
                a_ind += 1
            elif self.r[a_ind] > other.r[b_ind] or \
                    self.r[a_ind] == other.r[b_ind] and \
                    self.c[a_ind] > other.c[b_ind]:
                r += [other.r[b_ind]]
                c += [other.c[b_ind]]
                d += [self.operation[sign](0, other.d[b_ind])]
                b_ind += 1
            elif self.r[a_ind] == other.r[b_ind] \
                    and self.c[a_ind] == other.c[b_ind]:
                val = self.operation[sign](
                    self.d[a_ind], other.d[b_ind])
                if val != 0:
                    d += [val]
                    r += [other.r[b_ind]]
                    c += [other.c[b_ind]]
                a_ind += 1
                b_ind += 1

        while a_ind < self.nnz:
            r += [self.r[a_ind]]
            c += [self.c[a_ind]]
            d += [self.operation[sign](self.d[a_ind], 0)]
            a_ind += 1

        while b_ind < other.nnz:
            r += [other.r[b_ind]]
            c += [other.c[b_ind]]
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
            deepcopy(self.r),
            deepcopy(self.c),
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
            deepcopy(self.r),
            deepcopy(self.c),
            deepcopy(self.d),
        ))
        result.alpha_result(other, "/")
        return result

    def __matmul__(self, other):
        dict_num_1, dict_num_2 = {}, {}
        if self.cn != other.rn:
            raise ValueError
        for ind, val in enumerate(self.r):
            if val in dict_num_1:
                dict_num_1[val][self.c[ind]] = self.d[ind]
            else:
                dict_num_1[val] = {self.c[ind]: self.d[ind]}

        for ind, val in enumerate(other.c):
            if val in dict_num_2:
                dict_num_2[val][other.r[ind]] = other.d[ind]
            else:
                dict_num_2[val] = {other.r[ind]: other.d[ind]}
        r = []
        c = []
        d = []
        for i, val_frs in dict_num_1.items():
            for j, val_sec in dict_num_2.items():
                tmp_dict = {}
                for key, val in val_frs.items():
                    if key in val_sec:
                        tmp_dict[key] = val * val_sec[key]
                cell = sum(tmp_dict.values())
                if cell != 0:
                    r += [i]
                    c += [j]
                    d += [cell]
        res = CSRMatrix((r, c, d))
        return res

    def alpha_result(self, alpha, sign):
        for i, val in enumerate(self.d):
            self.d[i] = self.operation[sign](val, alpha)
