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
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            row_ind = init_matrix_representation[0]
            col_ind = init_matrix_representation[1]
            data = init_matrix_representation[2]
            self.A = list(data)
            self.JA = list(col_ind)
            self.IA = [0]
            for i in range(max(row_ind) + 1):
                nnz_i = row_ind.count(i)
                self.IA.append(nnz_i + self.IA[i])
            self.rows = len(self.IA) - 1
            self.cols = max(col_ind) + 1
            self._nnz = len(self.A)

        elif isinstance(init_matrix_representation, np.ndarray):
            M = init_matrix_representation
            self.cols = len(init_matrix_representation[0])
            self.A, self.IA, self.JA = self.get_csr_from_dense(M)
            self.rows = len(self.IA) - 1
            self._nnz = len(self.A)
        else:
            raise ValueError

    @property
    def nnz(self):
        return self._nnz

    @nnz.setter
    def nnz(self, value):
        raise AttributeError

    def get_csr_from_dense(self, m: list) -> tuple:
        a = []
        ia = [0]
        ja = []
        for i, row in enumerate(m):
            nnz = 0
            for j, val in enumerate(row):
                if val != 0:
                    nnz += 1
                    a.append(val)
                    ja.append(j)

            ia.append(ia[i] + nnz)

        return a, ia, ja

    def to_dense(self):
        A = self.A
        IA = self.IA
        JA = self.JA
        dense_m = np.zeros((self.rows, self.cols))
        for i in range(self.rows):
            nz_indexes_i = [ind for ind in range(IA[i], IA[i + 1])]
            # индексы элементов в A, которые в данной строке не нуль
            # ja[index] - колонка, в которой находится ненулевой элемент a[index]
            for index in nz_indexes_i:
                column = JA[index]
                dense_m[i][column] = A[index]
        return dense_m

    def __getitem__(self, indexes):
        i = indexes[0]
        j = indexes[1]
        if j > self.cols - 1 or j < 0:
            raise IndexError
        # если i > количество строк, то вылетит уже на строчке ниже
        # если на данной строке все нули
        nnz_i = self.IA[i + 1] - self.IA[i]
        if nnz_i == 0:
            return 0

        i_nz_indexes = [ind for ind in range(self.IA[i], self.IA[i + 1])]
        for ind in i_nz_indexes:
            if j == self.JA[ind]:
                return self.A[ind]
        return 0

    def __setitem__(self, indexes, value):
        i = indexes[0]
        j = indexes[1]
        nnz_i = self.IA[i + 1] - self.IA[i]

        if j > self.cols - 1 or j < 0:
            raise IndexError

        i_nz_indexes = [ind for ind in range(self.IA[i], self.IA[i + 1])]
        if value == 0:
            # все нули были
            if nnz_i == 0:
                return

            was_zero = True
            for ind in i_nz_indexes:
                if j == self.JA[ind]:
                    # значит был не ноль!
                    was_zero = False
                    self.A.pop(ind)
                    self.JA.pop(ind)
                    break
            # начиная с i+1 поправляем значение nnz в i строке(уменьшилось на 1)
            if not was_zero:
                for c in range(i + 1, len(self.IA)):
                    self.IA[c] -= 1
                self._nnz = len(self.A)
        else:
            j_insert = j
            for ind in i_nz_indexes:
                if j < self.JA[ind]:
                    j_insert = ind
                    break
                # заменяем старое значение
                if j == self.JA[ind]:
                    self.A[j] = value
                    return

            self.A.insert(j_insert, value)
            self.JA.insert(j_insert, j)
            for ind in range(i + 1, len(self.IA)):
                self.IA[ind] += 1
            self._nnz = len(self.A)

    def __add__(self, other):
        if self.cols == other.cols and self.rows == other.rows:
            row_ind = []
            column_ind = []
            data = []
            for i in range(other.rows):
                row_sum = {}
                for ind in range(self.IA[i], self.IA[i + 1]):
                    column = self.JA[ind]
                    value = self.A[ind]
                    row_sum[column] = value

                for ind in range(other.IA[i], other.IA[i + 1]):
                    o_column = other.JA[ind]
                    o_value = other.A[ind]

                    if o_column in row_sum:
                        row_sum[o_column] += o_value
                    else:
                        row_sum[o_column] = o_value
                for column, value in row_sum.items():
                    if value != 0:
                        data.append(value)
                        column_ind.append(column)
                        row_ind.append(i)
            return CSRMatrix((row_ind, column_ind, data))

        raise ValueError

    def __sub__(self, other):
        if self.cols == other.cols and self.rows == other.rows:
            row_ind = []
            column_ind = []
            data = []
            for i in range(other.rows):
                row_sum = {}
                for ind in range(self.IA[i], self.IA[i + 1]):
                    column = self.JA[ind]
                    value = self.A[ind]
                    row_sum[column] = value

                for ind in range(other.IA[i], other.IA[i + 1]):
                    o_column = other.JA[ind]
                    o_value = other.A[ind]

                    if o_column in row_sum:
                        row_sum[o_column] -= o_value
                    else:
                        row_sum[o_column] = -o_value

                for column, value in row_sum.items():
                    if value != 0:
                        data.append(value)
                        column_ind.append(column)
                        row_ind.append(i)

            return CSRMatrix((row_ind, column_ind, data))

        raise ValueError

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            csr_c = deepcopy(self)
            if other == 0:
                raise ZeroDivisionError
            else:
                for i in range(len(csr_c.A)):
                    csr_c.A[i] /= other
            return csr_c
        else:
            raise ValueError

    def __mul__(self, other):
        row_ind = []
        column_ind = []
        data = []

        if isinstance(other, int) or isinstance(other, float):

            for i in range(self.rows):

                for ind in range(self.IA[i], self.IA[i + 1]):
                    column = self.JA[ind]
                    value = self.A[ind] * other
                    if value != 0:
                        column_ind.append(column)
                        data.append(value)
                        row_ind.append(i)

            return CSRMatrix((row_ind, column_ind, data))

        elif isinstance(other, CSRMatrix):
            if self.cols == other.cols and self.rows == other.rows:

                for i in range(other.rows):

                    row_s = {}
                    for ind in range(self.IA[i], self.IA[i + 1]):
                        column = self.JA[ind]
                        value = self.A[ind]
                        row_s[column] = value

                    row_o = {}
                    for ind in range(other.IA[i], other.IA[i + 1]):
                        o_column = other.JA[ind]
                        o_value = other.A[ind]
                        row_o[o_column] = o_value

                    for column in row_s:
                        if column in row_o:
                            row_ind.append(i)
                            column_ind.append(column)
                            value = row_s[column] * row_o[column]
                            data.append(value)

                return CSRMatrix((row_ind, column_ind, data))

        raise ValueError

    def __rmul__(self, other):
        return self * other

    def __matmul__(self, other):
        # Чтобы осуществить умножение матриц(строка на столбец), транспонируем other
        # Теперь умножаем строка на строку
        if isinstance(other, CSRMatrix):
            if self.cols != other.rows:
                raise ValueError

            densed_other_transposed = other.to_dense().transpose()
            other = CSRMatrix(densed_other_transposed)

            row_ind = []
            column_ind = []
            data = []

            for i in range(self.rows):
                for j in range(other.rows):
                    row_s = {}
                    for ind in range(self.IA[i], self.IA[i + 1]):
                        s_column = self.JA[ind]
                        s_value = self.A[ind]
                        row_s[s_column] = s_value

                    row_o = {}
                    for ind in range(other.IA[j], other.IA[j + 1]):
                        o_column = other.JA[ind]
                        o_value = other.A[ind]
                        row_o[o_column] = o_value

                    row_ans = 0
                    for column in row_s:
                        if column in row_o:
                            row_ans += row_s[column] * row_o[column]
                    if row_ans != 0:
                        row_ind.append(i)
                        column_ind.append(j)
                        data.append(row_ans)

            return CSRMatrix((row_ind, column_ind, data))

        raise ValueError

    def dot(self, other):
        self.__matmul__(other)
