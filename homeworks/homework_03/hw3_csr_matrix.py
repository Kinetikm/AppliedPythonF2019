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
    operation = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
        "**": lambda x, y: x ** y
    }

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: can be usual dense matrix
        or
        (row_ind, col, data) tuple with np.arrays,
            where data, row_ind and col_ind satisfy the relationship:
            a[row_ind[k], col_ind[k]] = data[k]
        """
        if isinstance(init_matrix_representation, tuple) and len(
                init_matrix_representation) == 3:
            self.ia = [0 for i in range(
                max(min(init_matrix_representation[0]), 1))]
            cur_line = 0
            cnt = 0
            for i in init_matrix_representation[0]:
                if i == cur_line:
                    cnt += 1
                    continue
                self.ia += [cnt for _ in range(cur_line, i)]
                cur_line = i
                cnt += 1
            self.ia += [cnt]
            self.ja = deepcopy(init_matrix_representation[1])
            self.a = deepcopy(init_matrix_representation[2])
            self.rn = len(self.ia) - 1
            self.cn = max(self.ja) + 1
        elif isinstance(init_matrix_representation, np.ndarray):
            self.ia = [0]
            self.ja = []
            self.a = []
            cnt = 0
            for row in init_matrix_representation:
                for cn, val in enumerate(row):
                    if val != 0:
                        cnt += 1
                        self.ja += [cn]
                        self.a += [val]
                self.ia += [cnt]
            self.rn = len(init_matrix_representation)
            self.cn = len(init_matrix_representation[0])
        elif isinstance(init_matrix_representation, list):
            self.a = deepcopy(init_matrix_representation[0])
            self.ia = deepcopy(init_matrix_representation[1])
            self.ja = deepcopy(init_matrix_representation[2])
            self.rn = len(self.ia) - 1
            self.cn = max(self.ja) + 1
        else:
            raise ValueError
        self._nnz = len(self.a)

    nnz = property()

    @nnz.setter
    def nnz(self, value):
        if value != len(self.a):
            raise AttributeError
        self._nnz = value

    @nnz.getter
    def nnz(self):
        return self._nnz

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        result = np.zeros((self.rn, self.cn))
        num_nz_el = 0
        for i in range(self.rn):
            num = self.ia[i + 1]
            while num_nz_el < num:
                result[i, self.ja[num_nz_el]] = self.a[num_nz_el]
                num_nz_el += 1
        return result

    def __getitem__(self, index):
        print(index)
        num_els = self.ia[index[0] + 1] - self.ia[index[0]]
        for cur_el in range(num_els):
            if self.ja[self.ia[index[0]] + cur_el] == index[1]:
                return self.a[self.ia[index[0]] + cur_el]
        return 0

    def __setitem__(self, index, value):
        print(index)
        num_els = self.ia[index[0] + 1] - self.ia[index[0]]
        cur_el = 0
        while cur_el < num_els:
            if self.ja[self.ia[index[0]] + cur_el] < index[1]:
                cur_el += 1
                continue
            if self.ja[self.ia[index[0]] + cur_el] == index[1]:
                if value != 0:
                    self.a[self.ia[index[0]] + cur_el] = value
                    return
                self.a.pop(self.ia[index[0]] + cur_el)
                self.ja.pop(self.ia[index[0]] + cur_el)
                for i in range(index[0] + 1, self.rn + 1):
                    self.ia -= 1
                return
        if value == 0:
            return
        self.a.insert(self.ia[index[0]] + cur_el, value)
        self.ja.insert(self.ia[index[0]] + cur_el, index[1])
        for i in range(index[0] + 1, self.rn + 1):
            self.ia[i] += 1

    def __add__(self, other):
        if isinstance(other, CSRMatrix):
            return self.get_sum(other, "+")

    def get_sum(self, other, sign):
        if len(other.a) == 0:
            return CSRMatrix(self)
        if len(self.a) == 0:
            return CSRMatrix(other)
        row = []
        col = []
        data = []
        for r in range(self.rn):
            cur_ind_a, cur_ind_b = self.ia[r], other.ia[r]
            line_els_1, line_els_2 = self.ia[r + 1], other.ia[r + 1]
            while cur_ind_a < line_els_1 and cur_ind_b < line_els_2:
                if self.ja[cur_ind_a] < other.ja[cur_ind_b]:
                    row += [r]
                    col += [self.ja[cur_ind_a]]
                    data += [self.operation[sign](self.a[cur_ind_a], 0)]
                    cur_ind_a += 1
                elif self.ja[cur_ind_a] > other.ja[cur_ind_b]:
                    row += [r]
                    col += [other.ja[cur_ind_b]]
                    data += [self.operation[sign](0, other.a[cur_ind_b])]
                    cur_ind_b += 1
                elif self.ja[cur_ind_a] == other.ja[cur_ind_b]:
                    val = self.operation[sign](
                        self.a[cur_ind_a], other.a[cur_ind_b])
                    if val != 0:
                        data += [val]
                        row += [r]
                        col += [other.ja[cur_ind_b]]
                    cur_ind_a += 1
                    cur_ind_b += 1

            while cur_ind_a < line_els_1:
                row += [r]
                col += [self.ja[cur_ind_a]]
                data += [self.operation[sign](self.a[cur_ind_a], 0)]
                cur_ind_a += 1

            while cur_ind_b < line_els_2:
                row += [r]
                col += [other.ja[cur_ind_b]]
                data += [self.operation[sign](0, other.a[cur_ind_b])]
                cur_ind_b += 1
        print(data)
        print(row)
        print(col)

        return CSRMatrix((row, col, data))

    def __sub__(self, other):
        if isinstance(other, CSRMatrix):
            return self.get_sum(other, "-")

        return self.alpha_result(other, "-")

    def __mul__(self, other):
        if isinstance(other, CSRMatrix):
            return self.get_sum(other, "*")
        result = CSRMatrix([
            deepcopy(self.a),
            deepcopy(self.ia),
            deepcopy(self.ja),
        ])
        result.alpha_result(other, "*")
        return result

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, CSRMatrix):
            return
        if other == 0:
            raise ZeroDivisionError
        result = CSRMatrix([
            deepcopy(self.a),
            deepcopy(self.ia),
            deepcopy(self.ja),
        ])
        result.alpha_result(other, "/")
        return result

    def __pow__(self, other):
        if isinstance(other, CSRMatrix):
            return
        return self.alpha_result(other, "*")

    def alpha_result(self, alpha, sign):
        for i, val in enumerate(self.a):
            self.a[i] = self.operation[sign](val, alpha)

    def __matmul__(self, other):
        data1, data2 = {}, {}
        if self.cn != other.rn:
            raise ValueError
        ind = 0
        for row in range(self.rn):
            while ind < self.ia[row + 1]:
                if row in data1:
                    data1[row][self.ja[ind]] = self.a[ind]
                else:
                    data1[row] = {self.ja[ind]: self.a[ind]}
                ind += 1
        ind = 0
        for row in range(other.rn):
            while ind < other.ia[row + 1]:
                if other.ja[ind] in data2:
                    data2[other.ja[ind]][row] = other.a[ind]
                else:
                    data2[other.ja[ind]] = {row: other.a[ind]}
                ind += 1
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
