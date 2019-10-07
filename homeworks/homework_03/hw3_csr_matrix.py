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

        self.A = []
        self.IA = [0]
        self.JA = []
        self.n_row = 0
        self.n_col = 0

        bl = len(init_matrix_representation) == 3
        if isinstance(init_matrix_representation, tuple) and bl:  # не работает
            rw = 0
            for i in range(len(init_matrix_representation[0])):
                # возможно придется самому сортировать
                self.A.append(init_matrix_representation[2][i])
                self.JA.append(init_matrix_representation[1][i])
                self.n_col = max(self.n_col, init_matrix_representation[1][i])
                self.n_row = max(self.n_row, init_matrix_representation[0][i])
                k = rw
                rw = init_matrix_representation[0][i] + 1
                ln = rw - len(self.IA) + 1
                if len(self.IA) - 1 < rw:
                    self.IA.extend([0] * ln)
                self.IA[rw] += 1
                if k != rw:
                    self.IA[rw] += self.IA[k]
            bl = False
            for i in range(len(self.IA)):
                if self.IA[i] != 0:
                    bl = True
                if self.IA[i] == 0 and bl:
                    self.IA[i] = self.IA[i - 1]
        elif isinstance(init_matrix_representation, np.ndarray):
            self.n_row = len(init_matrix_representation)
            self.n_col = len(init_matrix_representation[0])
            for ind in range(len(init_matrix_representation)):
                self.IA.append(self.IA[-1])
                for i in range(len(init_matrix_representation[ind])):
                    if init_matrix_representation[ind][i] != 0:
                        self.A.append(init_matrix_representation[ind][i])
                        self.IA[-1] += 1
                        self.JA.append(i)
        else:
            raise ValueError

        self._nnz = len(self.A)

    @property
    def nnz(self):
        return self._nnz

    @nnz.setter
    def nnz(self, value):
        raise AttributeError

    def to_dense(self):
        lst = []
        n = -1
        for i in range(1, len(self.IA)):
            row = []
            for j in range(self.n_col):
                if j in self.JA[self.IA[i - 1]:self.IA[i]]:
                    n += 1
                    row.append(self.A[n])
                else:
                    row.append(0)
            lst.append(row)
        return np.array(lst)

    def __getitem__(self, tpl):
        x = self.IA[tpl[0]]
        y = self.IA[tpl[0] + 1]
        if y - x == 0:
            return 0
        for i in range(x, y):
            if self.JA[i] == tpl[1]:
                return self.A[i]
        return 0

    def __setitem__(self, tpl, value):
        if value == 0:
            x = self.IA[tpl[0]]
            y = self.IA[tpl[0] + 1]
            if y - x == 0:
                return
            for i in range(x, y):
                if self.JA[i] == tpl[1]:
                    self.A.pop(i)
                    self.JA.pop(i)
                    break
            for i in range((tpl[0] + 1), len(self.IA)):
                self.IA[i] -= 1
        else:
            x = self.IA[tpl[0]]
            y = self.IA[tpl[0] + 1]
            jpos = None
            if self[tpl[0], tpl[1]] == 0:
                if x - y == 0:
                    jpos = y
                for i in range(x, y):
                    if tpl[1] < self.JA[i]:
                        jpos = i
                        break
                    elif i == y-1 and not jpos:
                        jpos = y
                for i in range((tpl[0] + 1), len(self.IA)):
                    self.IA[i] += 1
                self.A.insert(jpos, value)
                self.JA.insert(jpos, tpl[1])
            else:
                for i in range(x, y):
                    if self.JA[i] == tpl[1]:
                        self.A[i] = value
                        break
        self._nnz = len(self.A)

    def __add__(self, other):
        res = deepcopy(self)
        if res.n_col == other.n_col and res.n_row == other.n_row:
            j = -1
            for i in range(1, len(other.IA)):
                sub = other.IA[i] - other.IA[i - 1]
                if sub != 0:
                    for k in range(sub):
                        j += 1
                        value = self[i - 1, other.JA[j]] + other.A[j]
                        res[i - 1, other.JA[j]] = value
            return res
        else:
            raise ValueError
        self._nnz = len(self.A)

    def __sub__(self, other):
        res = deepcopy(self)
        if res.n_col == other.n_col and res.n_row == other.n_row:
            j = -1
            for i in range(1, len(other.IA)):
                sub = other.IA[i] - other.IA[i - 1]
                if sub != 0:
                    for k in range(sub):
                        j += 1
                        value = self[i - 1, other.JA[j]] - other.A[j]
                        res[i - 1, other.JA[j]] = value
            return res
        else:
            raise ValueError
        self._nnz = len(self.A)

    def __mul__(self, other):
        if isinstance(other, CSRMatrix):
            res = deepcopy(self)
            if res.n_col == other.n_col and res.n_row == other.n_row:
                j = -1
                for i in range(1, len(self.IA)):
                    sub = self.IA[i] - self.IA[i - 1]
                    if sub != 0:
                        for k in range(sub):
                            j += 1
                            value = other[i - 1, self.JA[j]] * self.A[j]
                            res[i - 1, self.JA[j]] = value
                return res
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            res = deepcopy(self)
            for i in range(len(res.A)):
                res.A[i] *= other
            return res
        else:
            raise ValueError
        self._nnz = len(self.A)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            res = deepcopy(self)
            if other == 0:
                raise ZeroDivisionError
            else:
                for i in range(len(res.A)):
                    res.A[i] /= other
            return res
        else:
            raise ValueError

    def __matmul__(self, other):

        raise NotImplementedError
