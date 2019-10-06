#!/usr/bin/env python
# coding: utf-8


import numpy as np
from copy import deepcopy


class CSRMatrix:
    """
    CSR (2D) matrix.
    Here you can read how CSR sparse matrix works:
    https://en.wikipedia.org/wiki/Sparse_matrix

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
        if isinstance(init_matrix_representation, tuple) and \
           len(init_matrix_representation) == 3:
            if len(init_matrix_representation[0]) == \
               len(init_matrix_representation[1]) == \
               len(init_matrix_representation[2]):
                for i in range(len(init_matrix_representation[0])):
                    self.A.append(init_matrix_representation[2][i])
                    self.JA.append(init_matrix_representation[1][i])
                for i in range(max(init_matrix_representation[0])+1):
                    self.IA.append(init_matrix_representation[0].
                                   count(i)+self.IA[-1])
            else:
                raise ValueError
        elif isinstance(init_matrix_representation, np.ndarray):
            for row in init_matrix_representation:
                nnz_in_row = 0
                for i, element in enumerate(row):
                    if element != 0:
                        self.A.append(element)
                        self.JA.append(i)
                        nnz_in_row += 1
                self.IA.append(self.IA[-1]+nnz_in_row)
        else:
            raise ValueError

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        lst_of_lst = [[] for i in range(len(self.IA)-1)]
        for i in range(len(self.IA)-1):
            for j in range(max(self.JA)+1):
                lst_of_lst[i].append(self[i, j])
        return np.array(lst_of_lst)

    def __getitem__(self, indexes):
        i, j = indexes
        ptr_1 = self.IA[i+1]
        ptr_0 = self.IA[i]
        if not ptr_1 - ptr_0:
            return 0
        try:
            offset = self.JA.index(j, ptr_0, ptr_1)
            return self.A[offset]
        except ValueError:
            return 0

    def __setitem__(self, indexes, val):
        i, j = indexes
        if self[i, j]:
            if val:
                ptr_0 = self.IA[i]
                ptr_1 = self.IA[i+1]
                offset = self.JA.index(j, ptr_0, ptr_1)
                self.A[offset] = val
            else:
                ptr_0 = self.IA[i]
                ptr_1 = self.IA[i+1]
                offset = self.JA.index(j, ptr_0, ptr_1)
                for k in range(i+1, len(self.IA)):
                    self.IA[k] -= 1
                del self.A[offset]
                del self.JA[offset]
        else:
            if not val:
                return
            else:
                for k in range(i+1, len(self.IA)):
                    self.IA[k] += 1
                ptr_0 = self.IA[i]
                ptr_1 = self.IA[i+1]
                tmp_ptr = self.IA[i]
                for el in self.JA[ptr_0:ptr_1]:
                    if el > j:
                        break
                    else:
                        tmp_ptr += 1
                if tmp_ptr == self.IA[i]:
                    self.JA.insert(tmp_ptr, j)
                    self.A.insert(tmp_ptr, val)
                    return
                self.JA.insert(tmp_ptr-1, j)
                self.A.insert(tmp_ptr-1, val)

    @property
    def nnz(self):
        return self.IA[-1]

    def __add__(self, other):
        if max(self.JA) != max(other.JA) or len(self.IA) != len(self.IA):
            raise ValueError
        result = deepcopy(self)
        string_num = []
        for i in range(len(other.IA) - 1):
            for j in range(other.IA[i+1] - other.IA[i]):
                string_num.append(i)
        for i in range(len(other.A)):
            result[string_num[i], other.JA[i]] += other.A[i]
        return result

    def __sub__(self, other):
        if max(self.JA) != max(other.JA) or len(self.IA) != len(self.IA):
            raise ValueError
        result = deepcopy(self)
        string_num = []
        for i in range(len(other.IA) - 1):
            for j in range(other.IA[i+1] - other.IA[i]):
                string_num.append(i)
        for i in range(len(other.A)):
            result[string_num[i], other.JA[i]] -= other.A[i]
        return result

    def __mul__(self, other):
        if max(self.JA) != max(other.JA) or len(self.IA) != len(self.IA):
            raise ValueError
        string_num = []
        result = CSRMatrix(np.zeros((len(self.IA)-1, max(self.JA) + 1)))
        for i in range(len(other.IA) - 1):
            for j in range(other.IA[i+1] - other.IA[i]):
                string_num.append(i)
        for i in range(len(other.A)):
            if other[string_num[i], other.JA[i]] and self[string_num[i],
                                                          other.JA[i]]:
                result[string_num[i], other.JA[i]] = other.A[i] * \
                                        self[string_num[i], other.JA[i]]
        return result

    def __rmul__(self, alpha):
        if alpha == 0:
            return CSRMatrix(np.zeros((len(self.IA)-1, max(self.JA) + 1)))
        result = deepcopy(self)
        for i in range(len(result.A)):
            result.A[i] *= alpha
        return result

    def __truediv__(self, alpha):
        if alpha == 0:
            raise ZeroDivisionError
        result = deepcopy(self)
        for i in range(len(result.A)):
            result.A[i] /= alpha
        return result

    def __matmul__(self, other):
        if (max(self.JA) + 1) != (len(other.IA) - 1):
            raise ValueError
        first_string_num = []
        second_string_num = []
        result = CSRMatrix(np.zeros((len(self.IA)-1, max(self.JA) + 1)))
        for i in range(len(self.IA) - 1):
            for j in range(self.IA[i+1] - self.IA[i]):
                first_string_num.append(i)
        for i in range(len(other.IA) - 1):
            for j in range(other.IA[i+1] - other.IA[i]):
                second_string_num.append(i)
        for i in range(len(self.IA)-1):
            for j in range(max(other.JA)+1):
                sum_ = 0
                for k in range(max(self.JA)+1):
                    if self[i, k] and other[k, j]:
                        sum_ += self[i, k] * other[k, j]
                if sum_ != 0:
                    result[i, j] = sum_
        return result
