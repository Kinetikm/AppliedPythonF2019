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
        self.A = []
        self.IA = [0]
        self.JA = []
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            for i in range(len(init_matrix_representation[2])):
                self.A.append(init_matrix_representation[2][i])
                self.JA.append(init_matrix_representation[1][i])
            for i in range(max(init_matrix_representation[0]) + 1):
                self.IA.append(init_matrix_representation[0].count(i) + self.IA[-1])
        elif isinstance(init_matrix_representation, np.ndarray):
            for i in range(len(init_matrix_representation)):
                num = 0
                for j in range(len(init_matrix_representation[i])):
                    if init_matrix_representation[i][j] != 0:
                        num += 1
                        self.A.append(init_matrix_representation[i][j])
                        self.JA.append(j)
                self.IA.append(num + self.IA[-1])
        else:
            raise ValueError

    @property
    def nnz(self):
        return int(self.IA[-1])

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        list_of_lists = [[] for _ in range(len(self.IA) - 1)]
        for i in range(len(self.IA) - 1):
            for j in range(max(self.JA) + 1):
                list_of_lists[i].append(self.__getitem__((i, j)))
        return np.array(list_of_lists)

    def __getitem__(self, item):
        for i in range(self.IA[item[0]], self.IA[item[0]+1]):
            if self.JA[i] == item[1]:
                return self.A[i]
        return 0

    def __setitem__(self, key, value):
        if self.__getitem__(key) != 0:
            for i in range(self.IA[key[0]], self.IA[key[0] + 1]):
                if self.JA[i] == key[1]:
                    break
            if value != 0:
                self.A[i] = value
            else:
                self.A.pop(i)
                self.JA.pop(i)
                for j in range(key[0]+1, len(self.IA)):
                    self.IA[j] -= 1
        else:
            if value != 0:
                for k in range(key[0] + 1, len(self.IA)):
                    self.IA[k] += 1
                tmp_ptr = self.IA[key[0]]
                for el in self.JA[self.IA[key[0]]:self.IA[key[0] + 1]]:
                    if el > key[1]:
                        break
                    else:
                        tmp_ptr += 1
                if tmp_ptr == self.IA[key[0]]:
                    self.JA.insert(tmp_ptr, key[1])
                    self.A.insert(tmp_ptr, value)
                    return
                self.JA.insert(tmp_ptr - 1, key[1])
                self.A.insert(tmp_ptr - 1, value)

    def multiset(self, other):
        """
        :param other: другая матрица тех же размеров
        :return: Мультимножество, значение - строка  other где есть ненулевой
        элемент, количество вхождений - число ненулевых элементов в строке
        """
        multiset = []
        for i in range(len(other.IA) - 1):
            for k in range(other.IA[i + 1] - other.IA[i]):
                multiset.append(i)
        return multiset

    def __add__(self, other):
        matrix_sum = copy.deepcopy(self)
        multiset = self.multiset(other)
        for i in range(len(multiset)):
            matrix_sum[multiset[i], other.JA[i]] += other.A[i]
        return matrix_sum

    def __sub__(self, other):
        m_sub = copy.deepcopy(self)
        multiset = self.multiset(other)
        for i in range(len(multiset)):
            m_sub[multiset[i], other.JA[i]] -= other.A[i]
        return m_sub

    def __mul__(self, other):
        product_matrix = CSRMatrix(np.zeros((len(self.IA)-1, max(self.JA) + 1)))
        multiset = self.multiset(other)
        for i in range(len(multiset)):
            if other[multiset[i], other.JA[i]] != 0 and self[multiset[i], other.JA[i]] != 0:
                product_matrix[multiset[i], other.JA[i]] = self[multiset[i], other.JA[i]] * other.A[i]
        return product_matrix

    def __rmul__(self, other):
        product_matrix = copy.deepcopy(self)
        product_matrix.A = np.multiply(self.A, other, casting="unsafe")
        return product_matrix

    def __truediv__(self, other):
        product_matrix = copy.deepcopy(self)
        product_matrix.A = np.true_divide(self.A, other, casting="unsafe")
        return product_matrix

    def __matmul__(self, other):
        if max(other.JA) + 1 != len(self.IA) - 1:
            raise ValueError
        product_matrix = CSRMatrix(np.zeros((len(self.IA) - 1, max(other.JA) + 1)))
        temp = 0
        for i in range(len(self.IA) - 1):
            for j in range(max(other.JA) + 1):
                for k in range(len(other.IA) - 1):
                    if self[i, k] & other[k, j]:
                        temp += self[i, k] * other[k, j]
                if temp != 0:
                    product_matrix[i, j] = temp
                    temp = 0
        return product_matrix
