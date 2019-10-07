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
        """
        :param init_matrix_representation: can be usual dense matrix
        or
        (row_ind, col, data) tuple with np.arrays,
            where data, row_ind and col_ind satisfy the relationship:
            a[row_ind[k], col_ind[k]] = data[k]
        """
        self.a = []
        self.ia = [0]
        self.ja = []
        self.nnz = 0
        self.cols_num = 0
        self.rows_num = 0
        flag = True
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            for i in range(2):
                flag *= (len(init_matrix_representation[i+1]) == len(init_matrix_representation[i]))
            if flag:
                for i in range(3):
                    for j in range(len(init_matrix_representation[0])):
                        if init_matrix_representation[i][j] != 0:
                            self.a.append(init_matrix_representation[i][j])
                            self.nnz += 1
                            self.ja.append(j)
                    self.ia.append(self.nnz)
                self.rows_num = 3
                self.cols_num = len(init_matrix_representation[0])
                del flag
            else:
                raise ValueError

        elif isinstance(init_matrix_representation, np.ndarray):
            init_matr = init_matrix_representation
            init_matr = init_matr.tolist()
            init_matr.sort(key=lambda i: (i[0], i[1]))
            self.rows_num = max(r[0] for r in init_matr)+1
            self.cols_num = max(c[1] for c in init_matr)+1
            nnz = 0
            tmp_str_num = 0
            for item in init_matr:
                if item[2] != 0:
                    if item[0] > tmp_str_num:
                        for i in range(item[0] - tmp_str_num):
                            self.ia.append(nnz)
                        tmp_str_num = item[0]
                    self.a.append(item[2])
                    self.ja.append(item[1])
                    nnz += 1
            self.ia.append(nnz)
        else:
            raise ValueError

    def __getitem__(self, item):
        row = item[0]
        col = item[1]
        rows_num = len(self.ia) -1
        cols_num = max(self.ja) + 1
        els_in_row = self.ia[row+1] - self.ia[row]
        if (0 <= row < rows_num) and (0 <= col < cols_num):
            if els_in_row == 0:
                return 0
            else:
                if col not in self.ja:
                    return 0
                else:
                    els_behind = self.ia[row]
                    for i in range(els_in_row):
                        if self.ja[els_behind + i] == col:
                            return self.a[els_behind + i]
                    return 0
        else:
            raise IndexError

    def to_dense(self):
        """
            Return dense representation of matrix (2D np.array).
        """
        mas = [[] for i in range(self.rows_num)]
        for i in range(self.rows_num):
            for j in range(self.cols_num):
                mas[i].append(0)
        els_passed = 0
        for i in range(1, len(self.ia)):
            while els_passed < self.ia[i]:
                mas[i-1][self.ja[els_passed]] = self.a[els_passed]
                els_passed += 1
        return mas


matr = CSRMatrix(np.array([(0, 1, 1), (0, 0, 2), (0, 2, 3),
                           (1, 0, 0), (1, 1, 0), (1, 2, 6),
                           (2, 0, 7), (2, 1, 8), (2, 2, 9)]))
