#!/usr/bin/env python
# coding: utf-8


import numpy as np
import copy


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
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.A = init_matrix_representation[2]
            self.JA = init_matrix_representation[1]
            self.IA = [0]
            for i in range(max(init_matrix_representation[0]) + 1):
                self.IA += [self.IA[i]]
                self.IA[i + 1] += init_matrix_representation[0].count(i)
            self._nnz = len(self.A)
        elif isinstance(init_matrix_representation, np.ndarray):
            self.A = []
            self.IA = [0]
            self.JA = []
            for i in range(init_matrix_representation.shape[0]):
                self.IA += [self.IA[i]]
                for j in range(init_matrix_representation.shape[1]):
                    a = init_matrix_representation[i][j]
                    if a != 0:
                        self.A += [a]
                        self.IA[i + 1] += 1
                        self.JA += [j]
            self._nnz = len(self.A)
        else:
            raise ValueError

    @property
    def nnz(self):
        return self._nnz

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        mtrx = np.zeros((len(self.IA) - 1, max(self.JA) + 1))
        for i in range(len(self.IA) - 1):
            for j in range(self.IA[i], self.IA[i + 1]):
                mtrx[i][self.JA[j]] = self.A[j]
        print(mtrx)
        return mtrx

    def __getitem__(self, tup):
        i, j = tup
        for ind in range(self.IA[i], self.IA[i + 1]):
            if self.JA[ind] == j:
                return self.A[ind]
        return 0.

    def __setitem__(self, tup, value):
        i, j = tup
        if value != 0:
            for ind in range(self.IA[i], self.IA[i + 1]):
                if self.JA[ind] == j:
                    self.A[ind] = value
                    return self.A[ind]
            self.A += [0]
            self.JA += [0]
            temp1 = j
            temp2 = value
            tempJA = self.JA[self.IA[i + 1]:]
            for ind in range(self.IA[i], self.IA[i + 1]):
                if temp1 < self.JA[ind]:
                    self.JA[ind], temp1 = temp1, self.JA[ind]
            temp1, self.JA[self.IA[i + 1]] = self.JA[self.IA[i + 1]], temp1
            self.JA[self.IA[i + 1] + 1:] = tempJA
            self.JA.pop()
            tempA = self.A[self.IA[i + 1]:]
            for k in range(i + 1, len(self.IA)):
                self.IA[k] += 1
            for ind in range(self.IA[i], self.IA[i + 1]):
                if self.JA[ind] == j:
                    break
            for idx in range(ind, len(self.A)):
                self.A[idx], temp2 = temp2, self.A[idx]
            self._nnz = len(self.A)
        else:
            on_nonzero_place = False
            for ind in range(self.IA[i], self.IA[i + 1]):
                if self.JA[ind] == j:
                    del self.JA[ind]
                    del self.A[ind]
                    on_nonzero_place = True
                    break
            if on_nonzero_place:
                for ind in range(i + 1, len(self.IA)):
                    self.IA[ind] -= 1
            self._nnz = len(self.A)
            return self

    def __add__(self, mtrx):
        res = copy.deepcopy(self)
        all_nnz_plc = []
        for i in range(len(mtrx.IA) - 1):
            for j in range(mtrx.IA[i], mtrx.IA[i + 1]):
                all_nnz_plc.append([i, mtrx.JA[j]])
        res.to_dense()
        for i, j in all_nnz_plc:
            value = mtrx[i, j]
            added = False
            for ind in range(res.IA[i], res.IA[i + 1]):
                if res.JA[ind] == j:
                    if res.A[ind] + value == 0:
                        res[i, j] = 0
                    else:
                        res.A[ind] += value
                    added = True
                    break
            if not added:
                res[i, j] = value
        res._nnz = len(res.A)
        return res

    def __sub__(self, mtrx):
        rev_mtrx = mtrx * (-1)
        res = self + rev_mtrx
        res._nnz = len(res.A)
        return res

    def __mul__(self, mtrx):
        if type(mtrx) != type(self):
            res = copy.deepcopy(self)
            if mtrx != 0:
                res.A = [i * mtrx for i in res.A]
            else:
                res.A = []
                res.IA = []
                res.JA = []
                res._nnz = 0
            return res
        else:
            if len(self.IA) == len(mtrx.IA):
                res = copy.deepcopy(self)
                all_nnz_plc_1 = []
                for i in range(len(mtrx.IA) - 1):
                    for j in range(mtrx.IA[i], mtrx.IA[i + 1]):
                        all_nnz_plc_1.append([i, mtrx.JA[j]])
                all_nnz_plc_2 = []
                all_z_plc = []
                for i in range(len(res.IA) - 1):
                    for j in range(res.IA[i], res.IA[i + 1]):
                        if [i, res.JA[j]] in all_nnz_plc_1:
                            all_nnz_plc_2.append([i, res.JA[j]])
                        else:
                            all_z_plc.append([i, res.JA[j]])
                for i, j in all_nnz_plc_2:
                    value = mtrx[i, j] * res[i, j]
                    res[i, j] = value
                for i, j in all_z_plc:
                    res[i, j] = 0
                res._nnz = len(res.A)
                return res
            else:
                print('Shapes dont match')
                return self

    def __rmul__(self, a):
        if a != 0:
            res = copy.deepcopy(self)
            res.A = [i * a for i in res.A]
        else:
            res.A = []
            res.IA = []
            res.JA = []
            res._nnz = 0
        return res

    def __truediv__(self, a):
        if a != 0:
            res = copy.deepcopy(self)
            res.A = [i / a for i in res.A]
            return res
        print('Divide CSR matrix a by zero scalar alpha')
        return self

    def __matmul__(self, mtrx):
        shape_left = (len(self.IA) - 1, max(self.JA) + 1)
        shape_right = (max(mtrx.JA) + 1, len(mtrx.IA) - 1)
        if shape_left != shape_right:
            raise ValueError
        else:
            res = np.zeros((shape_left[0], shape_left[0]))
            temp_mtrx = mtrx.to_dense()
            trans_mtrx = np.zeros((max(mtrx.JA) + 1, len(mtrx.IA) - 1))
            for i in range(max(mtrx.JA) + 1):
                for j in range(len(mtrx.IA) - 1):
                    trans_mtrx[i][j] = temp_mtrx[j, i]
            trans_mtrx = CSRMatrix(trans_mtrx)
            for k in range(shape_left[0]):
                for i in range(shape_left[0]):
                    r = 0
                    for ind in range(self.IA[k], self.IA[k + 1]):
                        r += self[k, self.JA[ind]] * trans_mtrx[i, self.JA[ind]]
                    res[k][i] = r
            res = CSRMatrix(res)
            return res
