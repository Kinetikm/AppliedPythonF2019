#!/usr/bin/env python
# coding: utf-8


import numpy as np
from copy import deepcopy


class CSRMatrix:
    """
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

        self.A = []
        self.IA = [0]
        self.JA = []
        self.n_row = 0
        self.n_col = 0

        bl = len(init_matrix_representation) == 3
        if isinstance(init_matrix_representation, tuple) and bl:
            num_of_elem = 0
            rw = 0
            for i in range(len(init_matrix_representation[0])):
                self.A.append(init_matrix_representation[2][i])
                self.JA.append(init_matrix_representation[1][i])
                if init_matrix_representation[0][i] != rw:
                    num_of_row = rw - len(self.IA) + 1
                    self.IA.extend([num_of_elem - 1] * num_of_row)
                    if num_of_row >= 0:
                        self.IA.append(num_of_elem)
                    rw = init_matrix_representation[0][i]
                num_of_elem += 1
            self.IA.append(num_of_elem)
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
        if tpl[0] + 1 >= len(self.IA):
            return 0
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


def test_csr_matrix_base_operations():
    np.random.seed(42)

    shape_x, shape_y = 200, 200
    matrix1 = np.random.randint(-1, 2, (shape_x, shape_y))
    matrix2 = np.random.randint(-1, 2, (shape_x, shape_y))
    alpha = 2.5
    try:
        a = CSRMatrix(matrix1)
        b = CSRMatrix(matrix2)
    except NotImplementedError:
        return True

    addition = a + b
    addition_true = matrix1 + matrix2
    diff = a - b
    product = a * b
    scalar = alpha * a
    division = a / alpha

    diff_true = matrix1 - matrix2
    product_true = matrix1 * matrix2
    scalar_true = alpha * matrix1
    division_true = matrix1 / alpha

    # assert (addition_true != 0).sum() == addition.nnz
    # assert (diff_true != 0).sum() == diff.nnz

    for i, j in zip(range(shape_x), range(shape_y)):
        assert np.isclose(addition[i, j], addition_true[i, j])
        assert np.isclose(diff[i, j], diff_true[i, j])
        assert np.isclose(product[i, j], product_true[i, j])
        assert np.isclose(scalar[i, j], scalar_true[i, j])
        assert np.isclose(division[i, j], division_true[i, j])


test_csr_matrix_base_operations()
