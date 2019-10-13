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
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.a = init_matrix_representation[2]
            self.ja = init_matrix_representation[1]
            self.ia = [0]
            for i in range(max(init_matrix_representation[0]) + 1):
                self.ia += [self.ia[i]]
                self.ia[i + 1] += init_matrix_representation[0].count(i)
            self._nnz = len(self.a)
        elif isinstance(init_matrix_representation, np.ndarray):
            self.a = []
            self.ia = [0]
            self.ja = []
            for i in range(init_matrix_representation.shape[0]):
                self.ia += [self.ia[i]]
                for j in range(init_matrix_representation.shape[1]):
                    a = init_matrix_representation[i][j]
                    if a != 0:
                        self.a += [a]
                        self.ia[i + 1] += 1
                        self.ja += [j]
            self._nnz = len(self.a)
        else:
            raise ValueError

    @property
    def nnz(self):
        return self._nnz

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        mtrx = np.zeros((len(self.ia) - 1, max(self.ja) + 1))
        for i in range(len(self.ia) - 1):
            for j in range(self.ia[i], self.ia[i + 1]):
                mtrx[i][self.ja[j]] = self.a[j]
        return mtrx

    def __getitem__(self, tup):
        i, j = tup
        for ind in range(self.ia[i], self.ia[i + 1]):
            if self.ja[ind] == j:
                return self.a[ind]
        return 0.

    def __setitem__(self, tup, value):
        i, j = tup
        if value != 0:
            for ind in range(self.ia[i], self.ia[i + 1]):
                if self.ja[ind] == j:
                    self.a[ind] = value
                    return self.a[ind]
            self.a += [0]
            self.ja += [0]
            temp1 = j
            temp2 = value
            temp_ja = self.ja[self.ia[i + 1]:]
            for ind in range(self.ia[i], self.ia[i + 1]):
                if temp1 < self.ja[ind]:
                    self.ja[ind], temp1 = temp1, self.ja[ind]
            temp1, self.ja[self.ia[i + 1]] = self.ja[self.ia[i + 1]], temp1
            self.ja[self.ia[i + 1] + 1:] = temp_ja
            self.ja.pop()
            for k in range(i + 1, len(self.ia)):
                self.ia[k] += 1
            for ind in range(self.ia[i], self.ia[i + 1]):
                if self.ja[ind] == j:
                    break
            for idx in range(ind, len(self.a)):
                self.a[idx], temp2 = temp2, self.a[idx]
            self._nnz = len(self.a)
        else:
            on_nonzero_place = False
            for ind in range(self.ia[i], self.ia[i + 1]):
                if self.ja[ind] == j:
                    del self.ja[ind]
                    del self.a[ind]
                    on_nonzero_place = True
                    break
            if on_nonzero_place:
                for ind in range(i + 1, len(self.ia)):
                    self.ia[ind] -= 1
            self._nnz = len(self.a)
            return self

    def __add__(self, mtrx):
        res = copy.deepcopy(self)
        all_nnz_plc = []
        for i in range(len(mtrx.ia) - 1):
            for j in range(mtrx.ia[i], mtrx.ia[i + 1]):
                all_nnz_plc.append([i, mtrx.ja[j]])
        res.to_dense()
        for i, j in all_nnz_plc:
            value = mtrx[i, j]
            added = False
            for ind in range(res.ia[i], res.ia[i + 1]):
                if res.ja[ind] == j:
                    if res.a[ind] + value == 0:
                        res[i, j] = 0
                    else:
                        res.a[ind] += value
                    added = True
                    break
            if not added:
                res[i, j] = value
        res._nnz = len(res.a)
        return res

    def __sub__(self, mtrx):
        rev_mtrx = mtrx * (-1)
        res = self + rev_mtrx
        res._nnz = len(res.a)
        return res

    def __mul__(self, mtrx):
        if type(mtrx) != type(self):
            res = copy.deepcopy(self)
            if mtrx != 0:
                res.a = [i * mtrx for i in res.a]
            else:
                res.a = []
                res.ia = []
                res.ja = []
                res._nnz = 0
            return res
        else:
            if len(self.ia) == len(mtrx.ia):
                res = copy.deepcopy(self)
                all_nnz_plc_1 = []
                for i in range(len(mtrx.ia) - 1):
                    for j in range(mtrx.ia[i], mtrx.ia[i + 1]):
                        all_nnz_plc_1.append([i, mtrx.ja[j]])
                all_nnz_plc_2 = []
                all_z_plc = []
                for i in range(len(res.ia) - 1):
                    for j in range(res.ia[i], res.ia[i + 1]):
                        if [i, res.ja[j]] in all_nnz_plc_1:
                            all_nnz_plc_2.append([i, res.ja[j]])
                        else:
                            all_z_plc.append([i, res.ja[j]])
                for i, j in all_nnz_plc_2:
                    value = mtrx[i, j] * res[i, j]
                    res[i, j] = value
                for i, j in all_z_plc:
                    res[i, j] = 0
                res._nnz = len(res.a)
                return res
            else:
                return self

    def __rmul__(self, a):
        if a != 0:
            res = copy.deepcopy(self)
            res.a = [i * a for i in res.a]
        else:
            res.a = []
            res.ia = []
            res.ja = []
            res._nnz = 0
        return res

    def __truediv__(self, a):
        if a != 0:
            res = copy.deepcopy(self)
            res.a = [i / a for i in res.a]
            return res
        return self

    def __matmul__(self, mtrx):
        shape_left = (len(self.ia) - 1, max(self.ja) + 1)
        shape_right = (max(mtrx.ja) + 1, len(mtrx.ia) - 1)
        if shape_left != shape_right:
            raise ValueError
        else:
            res = np.zeros((shape_left[0], shape_left[0]))
            temp_mtrx = mtrx.to_dense()
            trans_mtrx = np.zeros((max(mtrx.ja) + 1, len(mtrx.ia) - 1))
            for i in range(max(mtrx.ja) + 1):
                for j in range(len(mtrx.ia) - 1):
                    trans_mtrx[i][j] = temp_mtrx[j, i]
            trans_mtrx = CSRMatrix(trans_mtrx)
            for k in range(shape_left[0]):
                for i in range(shape_left[0]):
                    r = 0
                    for ind in range(self.ia[k], self.ia[k + 1]):
                        r += self[k, self.ja[ind]] * trans_mtrx[i, self.ja[ind]]
                    res[k][i] = r
            res = CSRMatrix(res)
            return res
