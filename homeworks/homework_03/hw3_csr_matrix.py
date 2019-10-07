#!/usr/bin/env python
# coding: utf-8


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
        self.row_ind = []
        self.col_ind = []
        self.shapes = []
        self.data = []
        self._nnz = 0

        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.row_ind = init_matrix_representation[0]
            self.col_ind = init_matrix_representation[1]
            self.data = init_matrix_representation[2]

        elif isinstance(init_matrix_representation, np.ndarray):
            for i in range(init_matrix_representation.shape[0]):
                for j in range(init_matrix_representation.shape[1]):
                    if init_matrix_representation[i, j] != 0:
                        self.data.append(init_matrix_representation[i, j])
                        self.row_ind.append(i)
                        self.col_ind.append(j)
            self.shapes = init_matrix_representation.shape
        else:
            raise ValueError

        self._nnz = len(self.row_ind)

    nnz = property()

    @nnz.getter
    def nnz(self):
        return self._nnz

    def __getitem__(self, item):
        i_find, j_find = item
        for i, j, d in zip(self.row_ind, self.col_ind, self.data):
            if i == i_find and j == j_find:
                return d
        return 0

    def __setitem__(self, key, value):

        i_find, j_find = key

        if not len(self.row_ind):
            self.row_ind.append(i_find)
            self.col_ind.append(j_find)
            self.data.append(value)
            self._nnz += 1
            return

        for ind, mat_ind in enumerate(zip(self.row_ind, self.col_ind)):
            i, j = mat_ind
            if i_find == i and j_find == j:
                if not value:
                    self.row_ind.pop(ind)
                    self.col_ind.pop(ind)
                    self.data.pop(ind)
                    self._nnz -= 1
                self.data[ind] = value
                return

            if i_find < i or (i_find == i and j_find < j):
                self.row_ind = self.row_ind[:ind + 1] + [i_find] + self.row_ind[ind + 1:]
                self.col_ind = self.row_ind[:ind + 1] + [j_find] + self.row_ind[ind + 1:]
                self.data = self.row_ind[:ind + 1] + [value] + self.row_ind[ind + 1:]
                self._nnz += 1
                return

        self.row_ind.append(i_find)
        self.col_ind.append(j_find)
        self.data.append(value)
        self._nnz += 1
        return

    def mat_operation(self, other, func):
        n_row, n_col, n_data = [], [], []
        o_row, o_col, o_data = other.row_ind, other.col_ind, other.data
        frs_ind, sec_ind = 0, 0
        f = True

        while f:
            if frs_ind == len(self.row_ind):
                for i in range(sec_ind, len(o_row)):
                    r = func(0, o_data[i])
                    if not r:
                        continue
                    n_row.append(o_row[i])
                    n_col.append(o_col[i])
                    n_data.append(r)
                break
            if sec_ind == len(o_row):
                for i in range(frs_ind, len(self.row_ind)):
                    r = func(self.data[i], 0)
                    if not r:
                        continue
                    n_row.append(self.row_ind[i])
                    n_col.append(self.col_ind[i])
                    n_data.append(r)
                break

            if self.row_ind[frs_ind] == o_row[sec_ind]:
                if self.col_ind[frs_ind] == o_col[sec_ind]:
                    r = func(self.data[frs_ind], o_data[sec_ind])
                    if not r:
                        frs_ind += 1
                        sec_ind += 1
                        continue
                    n_row.append(o_row[sec_ind])
                    n_col.append(o_col[sec_ind])
                    n_data.append(r)
                    frs_ind += 1
                    sec_ind += 1
                elif self.col_ind[frs_ind] < o_col[sec_ind]:
                    r = func(self.data[frs_ind], 0)
                    if not r:
                        frs_ind += 1
                        continue
                    n_row.append(self.row_ind[frs_ind])
                    n_col.append(self.col_ind[frs_ind])
                    n_data.append(r)
                    frs_ind += 1
                else:
                    r = func(0, o_data[sec_ind])
                    if not r:
                        sec_ind += 1
                        continue
                    n_row.append(o_row[sec_ind])
                    n_col.append(o_col[sec_ind])
                    n_data.append(r)
                    sec_ind += 1
            elif self.row_ind[frs_ind] < o_row[sec_ind]:
                r = func(self.data[frs_ind], 0)
                if not r:
                    frs_ind += 1
                    continue
                n_row.append(self.row_ind[frs_ind])
                n_col.append(self.col_ind[frs_ind])
                n_data.append(r)
                frs_ind += 1
            else:
                r = func(self.data[frs_ind], 0)
                if not r:
                    sec_ind += 1
                    continue
                n_row.append(o_row[sec_ind])
                n_col.append(o_col[sec_ind])
                n_data.append(func(0, o_data[sec_ind]))
                sec_ind += 1
        return CSRMatrix(tuple([n_row, n_col, n_data]))

    def sc_operation(self, value, func):
        n_row, n_col, n_data = [], [], []

        for i, j, d in zip(self.row_ind, self.col_ind, self.data):
            n_row.append(i)
            n_col.append(j)
            n_data.append(func(d, value))

        return CSRMatrix(tuple([n_row, n_col, n_data]))

    def __add__(self, other):
        return self.mat_operation(other, lambda x, y: x + y)

    def __sub__(self, other):
        return self.mat_operation(other, lambda x, y: x - y)

    def __mul__(self, other):
        return self.mat_operation(other, lambda x, y: x * y)

    def __rmul__(self, value):
        if not value:
            return CSRMatrix(tuple([[], [], []]))
        return self.sc_operation(value, lambda x, y: x * y)

    def __truediv__(self, value):
        if not value:
            raise ZeroDivisionError
        return self.sc_operation(value, lambda x, y: x / y)

    def __matmul__(self, other):
        if self.shapes[-1] != other.shapes[0]:
            raise ValueError

        result = {}

        for f_i, f_j, f_d in zip(self.row_ind, self.col_ind, self.data):
            for s_i, s_j, s_d in zip(other.row_ind, other.col_ind, other.data):
                if f_j != s_i:
                    continue

                if (f_i, s_j) in result:
                    result[(f_i, s_j)] += f_d * s_d
                else:
                    result[(f_i, s_j)] = f_d * s_d

        n_r, n_c, n_d = [], [], []
        for item in result.items():
            if not item[1]:
                continue
            n_r.append(item[0][0])
            n_c.append(item[0][1])
            n_d.append(item[1])

        return CSRMatrix(tuple([n_r, n_c, n_d]))

    def to_dense(self):
        row, col = self.row_ind[-1], self.col_ind[-1]

        result = np.zeros(shape=(row + 1, col + 1))
        for i, j, d in zip(self.row_ind, self.col_ind, self.data):
            result[i][j] = d

        return result


np.random.seed(42)

shape_x, shape_y = 5, 5
matrix1 = np.random.randint(-1, 2, (shape_x, shape_y))
matrix2 = np.random.randint(-1, 2, (shape_x, shape_y))
alpha = 2.5
try:
    a = CSRMatrix(matrix1)
    b = CSRMatrix(matrix2)
except NotImplementedError:
    pass
