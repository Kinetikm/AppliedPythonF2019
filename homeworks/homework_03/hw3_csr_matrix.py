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

        print(self)

        return

    def _set_shape(self, n, m):
        self.shape = (n,m)
        self._ia = [0] * (self.shape[0] + 1)
        return

    def __repr__(self):
        return f"shape: {self.shape}. a: {self._a}, ja: {self._ja}, ia: {self._ia}"

    def __matmul__(self, other):
        pass

    def __add__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __getitem__(self, key):
        # print("a", self._a)
        # print("ja", self._ja)
        # print("ia", self._ia)
        print("getting:", key)
        idx = self._get_key_a_idx(*key)
        # print("idx", idx)
        if idx is None:
            return 0

        # print("len a", len(self._a))
        # print("len ja", len(self._ja))
        return self._a[idx]


    def _get_key_a_idx(self, i, j):
        """
        Получаем индекс элемента в _a
        :param i:
        :param j:
        :return:
        """
        ja_start_range = self._ia[i]
        ja_stop_range = self._ia[i+1]

        for i in range(ja_start_range, ja_stop_range):
            if self._ja[i] == j:
                return i
        return

    def __setitem__(self, key, value):
        print("assigment:", key, value)

        i, j = key

        if i > self.shape[0] - 1 or j > self.shape[1]:
            raise KeyError
        if value == 0 and self[i, j] == 0:
            return

        if self[i, j] != 0:
            idx = self._get_key_a_idx()
            self._a[idx] = value
            return

        for ia_idx in range(i+1, self.shape[0]+1):
            self._ia[ia_idx] += 1

        ja_start_range = self._ia[i]
        ja_stop_range = self._ia[i + 1]

        # print(f"ja_start_range {ja_start_range}, ja_stop_range {ja_stop_range}")
        # print(f"{self._ja}")

        insert_val_idx = ja_stop_range
        for ja_idx in range(ja_start_range, ja_stop_range):
            if ja_idx >= len(self._ja) or self._ja[ja_idx] > j:
                insert_val_idx = ja_idx
                break

        # print(f"insert_val_idx {insert_val_idx}")
        self._a.insert(insert_val_idx, value)
        self._ja.insert(insert_val_idx, j)

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