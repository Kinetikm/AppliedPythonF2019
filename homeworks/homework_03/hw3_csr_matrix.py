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
        (row_ind, col_ind, data) tuple with np.arrays,
            where data, row_ind and col_ind satisfy the relationship:
            a[row_ind[k], col_ind[k]] = data[k]
        """
        self._a: list
        self._ia: list
        self._ja: list

        self._a = []
        self._ia = []
        self._ja = []

        self._nnz = 0

        self.shape = None

        # print("init_matrix_representation", init_matrix_representation)

        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            for i in range(1, 3):
                assert len(init_matrix_representation[0]) == len(init_matrix_representation[i])

            self._set_shape(max(init_matrix_representation[0])+1, max(init_matrix_representation[1])+1)

            for idx, data_el in enumerate(init_matrix_representation[2]):
                if data_el == 0:
                    continue
                i = init_matrix_representation[0][idx]
                j = init_matrix_representation[1][idx]
                self[i, j] = data_el
        elif isinstance(init_matrix_representation, np.ndarray):
            # print("init:", init_matrix_representation)
            # print("size:", init_matrix_representation.shape)
            self._set_shape(*init_matrix_representation.shape)

            for i in range(init_matrix_representation.shape[0]):
                for j in range(init_matrix_representation.shape[1]):
                    self[i, j] = init_matrix_representation[i][j]
        else:
            raise ValueError

        return

    def _set_shape(self, n, m):
        self.shape = (n,m)
        self._ia = [0] * (self.shape[0] + 1)
        return

    @property
    def nnz(self):
        # print("setting nnz", len(self._a))
        return self._nnz

    @nnz.setter
    def nnz(self, val):
        if val == len(self._a):
            self._nnz = val

    def __repr__(self):
        return f"shape: {self.shape}. a ({len(self._a)}): {self._a}, ja: {self._ja}, ia: {self._ia}"

    def is_zero_row(self, i):
        return self._ia[i+1] - self._ia[i] == 0

    def is_zero_col(self, j):
        return j not in self._ja

    def __matmul__(self, other):
        if not isinstance(other, CSRMatrix):
            raise ValueError()

        if self.shape[0] != other.shape[1]:
            raise ValueError()

        res_shape = (self.shape[0], other.shape[1])
        res = CSRMatrix(np.zeros(res_shape))

        # print(self)
        for i in range(res_shape[0]):
            # ну, в принципе, можно было бы сделать проверки на то, что в данной строчке все значения нулевые,
            # но много профита это не даст, потмоу что в тестах все равно не такие уж разреженые
            if self.is_zero_row(i):
                continue
            for j in range(res_shape[1]):
                if other.is_zero_col(j):
                    continue
                for k in range(self.shape[1]):
                    if self[i, k] == 0 or other[k, j] == 0:
                        continue
                    res[i, j] += self[i, k] * other[k, j]
        return res


    def _base_operation(self, other, operation: callable):
        res = copy.deepcopy(self)
        if self.shape != other.shape:
            raise ValueError()
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                res[i, j] = operation(self[i, j], other[i, j])
        return res

    def _base_operation_with_a(self, other, operation: callable):
        res = copy.deepcopy(self)
        for i in range(len(self._a)):
            res._a[i] = operation(self._a[i], other)
        return res

    def _base_operation_with_any_type(self, other, operation:callable):
        if isinstance(other, CSRMatrix):
            return self._base_operation(other, operation)
        return self._base_operation_with_a(other, operation)

    def __add__(self, other):
        res =  self._base_operation_with_any_type(other, np.add)
        return res

    def __sub__(self, other):
        return self._base_operation_with_any_type(other, np.subtract)

    def __mul__(self, other):
        return self._base_operation_with_any_type(other, np.multiply)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self._base_operation_with_any_type(other, np.divide)

    def __getitem__(self, key):
        idx = self._get_key_a_idx(*key)
        if idx is None:
            return 0

        return self._a[idx]

    def _get_key_a_idx(self, i, j):
        """
        Получаем индекс элемента в _a
        """
        ja_start_range = self._ia[i]
        ja_stop_range = self._ia[i+1]

        for i in range(ja_start_range, ja_stop_range):
            if self._ja[i] == j:
                return i
        return

    def __setitem__(self, key, value):
        i, j = key
        # print("\nsetting", key, value)
        # print("current self[i, j]", self[i, j])
        # print("filan nnz", len(self._a))
        if i > self.shape[0] - 1 or j > self.shape[1] - 1:
            raise KeyError

        if value == self[i, j]:
            return


        if self[i, j] != 0:
            idx = self._get_key_a_idx(i, j)
            if value != 0:
                self._a[idx] = value
                return
            # print((i,j))
            # print(self)
            # print("deleting elemtny in index:", idx)
            self._a.pop(idx)
            self._ja.pop(idx)
            for ia_idx in range(i + 1, self.shape[0] + 1):
                self._ia[ia_idx] -= 1
            self.nnz = self.nnz - 1
            # print("deleted", self)
            # print("filan nnz", self.nnz)
            return

        for ia_idx in range(i+1, self.shape[0]+1):
            self._ia[ia_idx] += 1

        ja_start_range = self._ia[i]
        ja_stop_range = self._ia[i + 1]

        insert_val_idx = ja_start_range
        for ja_idx in range(ja_start_range, ja_stop_range):
            if ja_idx >= len(self._ja):
                insert_val_idx = ja_idx
                break
            if self._ja[ja_idx] > j:
                insert_val_idx = ja_idx
                break

        # print(self)
        # print(f"insert_val_idx {insert_val_idx}")
        self._a.insert(insert_val_idx, value)
        self._ja.insert(insert_val_idx, j)
        self.nnz = self.nnz + 1

        # print("filan nnz", len(self._a))
        # print("result:", self[key])
        return

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        res = np.zeros(self.shape)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                res[i][j] = self[i, j]

        return res