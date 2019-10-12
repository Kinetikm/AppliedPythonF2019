#!/usr/bin/env python
# coding: utf-8


import numpy as np
from copy import deepcopy


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
        self.a = []
        self.ai = [0]
        self.aj = []
        self._nnz = 0
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.size = (max(init_matrix_representation[0]) + 1, max(init_matrix_representation[1]) + 1)
            tmp = 0
            flag = False
            for i in range(init_matrix_representation[0][0]):
                self.ai.append(0)
            for i in init_matrix_representation[0]:
                if i - tmp == 0:
                    tmp = i
                    self._nnz += 1
                    flag = True
                elif i - tmp == 1:
                    if flag:
                        flag = False
                        self.ai.append(self._nnz)
                        tmp = i
                        self._nnz += 1
                    else:
                        tmp = i
                        self._nnz += 1
                        self.ai.append(self._nnz)
                else:
                    if flag:
                        flag = False
                        self.ai.append(self._nnz)
                    for _ in range(i - tmp - 1):
                        self.ai.append(self._nnz)
                    tmp = i
                    self._nnz += 1
                    self.ai.append(self._nnz)

            self.ai.append(self._nnz)
            self.aj = deepcopy(init_matrix_representation[1])
            self.a = deepcopy(init_matrix_representation[2])

        elif isinstance(init_matrix_representation, np.ndarray):
            if len(init_matrix_representation.shape) == 2:
                self.size = init_matrix_representation.shape
                for i in range(self.size[0]):
                    for j in range(self.size[1]):
                        if init_matrix_representation[i, j] != 0:
                            self.aj.append(j)
                            self.a.append(init_matrix_representation[i, j])
                            self._nnz += 1
                    self.ai.append(self._nnz)
            else:
                raise ValueError
        else:
            raise ValueError

    def __getitem__(self, ids):
        if ids[0] > self.size[0] and ids[1] > self.size[1]:
            raise IndexError
        if self.ai[ids[0]] == self.ai[ids[0] + 1]:
            return 0
        temp_col = self.aj[self.ai[ids[0]]:self.ai[ids[0] + 1]]
        if ids[1] in temp_col:
            ind = temp_col.index(ids[1])
            return self.a[self.ai[ids[0]]:self.ai[ids[0] + 1]][ind]
        return 0

    @property
    def nnz(self):
        return self._nnz

    def __setitem__(self, ids, value):
        if ids[0] > self.size[0] and ids[1] > self.size[1]:
            raise IndexError

        if ids[0] > self.size[0] and ids[1] > self.size[1]:
            raise IndexError
        ind = 0
        flag = False
        if value:
            if not self.aj:
                self.aj.append(ids[1])
                self.a.append(value)
                self._nnz += 1
            else:
                if not self.aj[self.ai[ids[0]]:self.ai[ids[0] + 1]]:
                    self.aj.insert(self.ai[ids[0]], ids[1])
                    self.a.insert(self.ai[ids[0]], value)
                    self._nnz += 1
                else:
                    if self.ai[ids[0]] + 1 in self.aj:
                        a = deepcopy(self.aj[self.ai[ids[0]]:self.ai[ids[0] + 1]])
                        if ids[1] in a:
                            ind = self.ai[ids[0]] + a.index(ids[1])
                            self.a[ind] = value
                            return
                        else:
                            a.append(ids[1])
                            a.sort()
                            ind = a.index(ids[1])
                            b = deepcopy(self.a[self.ai[ids[0]]:self.ai[ids[0] + 1]])
                            b.insert(ind, value)
                            del self.a[self.ai[ids[0]]:self.ai[ids[0] + 1]]
                            del self.aj[self.ai[ids[0]]:self.ai[ids[0] + 1]]
                            for i, j, v in zip(range(self.ai[ids[0]], self.ai[ids[0]] + len(a)), a, b):
                                self.aj.insert(i, j)
                                self.a.insert(i, v)
                            self._nnz += 1
                    else:
                        tmp = self.aj[self.ai[ids[0]]]
                        if ids[1] > tmp:
                            self.aj.insert(self.ai[ids[0]] + 1, ids[1])
                            self.a.insert(self.ai[ids[0]] + 1, value)
                        else:
                            self.aj.insert(self.ai[ids[0]], ids[1])
                            self.a.insert(self.ai[ids[0]], value)
                        self._nnz += 1

            for i in range(1, len(self.ai)):
                if flag:
                    self.ai[i] += 1
                else:
                    if i == ids[0] + 1:
                        self.ai[i] += 1
                        flag = True
                        continue

        return

    def to_dense(self):
        dense = np.zeros(self.size)
        tmp = 0
        for i, k in enumerate(self.ai[1:]):
            for j in self.aj[self.ai[i]:self.ai[i + 1]]:
                dense[i, j] = self.a[tmp]
                tmp += 1
        return dense

    def get_data(self, other):
        rows = []
        colomns = []
        values = []
        tmp = 0
        for i, k in enumerate(other.ai[1:]):
            for j in other.aj[other.ai[i]:other.ai[i + 1]]:
                rows.append(i)
                colomns.append(j)
                values.append(other.a[tmp])
                tmp += 1
        return rows, colomns, values

    def operations(self, other, func):
        if self.size != other.size:
            raise IndexError
        rows = []
        colomns = []
        values = []
        self_rows, self_colonms, self_values = self.get_data(self)
        other_rows, other_colonms, other_values = self.get_data(other)
        apos = 0
        bpos = 0

        while apos < self.nnz and bpos < other.nnz:
            if self_rows[apos] > other_rows[bpos] or self_rows[apos] == other_rows[bpos] and self_colonms[apos] > \
                    other_colonms[bpos]:
                res = func(0, other_values[bpos])
                if res:
                    rows.append(other_rows[bpos])
                    colomns.append(other_colonms[bpos])
                    values.append(res)
                bpos += 1

            elif self_rows[apos] < other_rows[bpos] or self_rows[apos] == other_rows[bpos] and self_colonms[apos] < \
                    other_colonms[bpos]:
                res = func(self_values[apos], 0)
                if res:
                    rows.append(self_rows[apos])
                    colomns.append(self_colonms[apos])
                    values.append(res)
                apos += 1

            else:
                res = func(self_values[apos], other_values[bpos])
                if res:
                    rows.append(self_rows[apos])
                    colomns.append(self_colonms[apos])
                    values.append(res)
                apos += 1
                bpos += 1

        while apos < self.nnz:
            res = func(self_values[apos], 0)
            if res:
                rows.append(self_rows[apos])
                colomns.append(self_colonms[apos])
                values.append(res)
            apos += 1

        while bpos < other.nnz:
            res = func(0, other_values[bpos])
            if res:
                rows.append(other_rows[bpos])
                colomns.append(other_colonms[bpos])
                values.append(res)
            bpos += 1
        return CSRMatrix((rows, colomns, values))

    def __add__(self, other):
        return self.operations(other, lambda x, y: x + y)

    __radd__ = __add__

    def __sub__(self, other):
        return self.operations(other, lambda x, y: x - y)

    __rsub__ = __sub__

    def __mul__(self, other):
        if isinstance(other, CSRMatrix):
            return self.operations(other, lambda x, y: x * y)

        elif isinstance(other, int) or isinstance(other, float):
            res = deepcopy(self)
            res.a = [i * other for i in self.a]
            return res
        raise TypeError

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            if other:
                res = deepcopy(self)
                res.a = [i / other for i in self.a]
                return res
            raise ZeroDivisionError
        raise TypeError

    def __matmul__(self, other):
        if self.size[1] != other.size[0]:
            raise ValueError
        self_rows, self_colonms, self_values = self.get_data(self)
        other_rows, other_colonms, other_values = self.get_data(other)
        rows = {}
        col = {}
        for i, v in enumerate(self_rows):
            try:
                rows[v][self_colonms[i]] = self_values[i]
            except:
                rows[v] = {self_colonms[i]: self_values[i]}

        for i, v in enumerate(other_colonms):
            try:
                col[v][other_rows[i]] = other_values[i]

            except:
                col[v] = {other_rows[i]: other_values[i]}

        row_res = []
        col_res = []
        val_res = []
        for i, v1 in rows.items():
            for j, v2 in col.items():
                res = sum({k: v * v2[k] for k, v in v1.items() if k in v2}.values())
                if res:
                    row_res.append(i)
                    col_res.append(j)
                    val_res.append(res)
        temp = zip(row_res, col_res, val_res)
        xs = sorted(temp, key=lambda i: (i[0], i[1]))
        return CSRMatrix(([x[0] for x in xs], [x[1] for x in xs], [x[2] for x in xs]))

    __rmatmul__ = __matmul__

    dot = __matmul__
