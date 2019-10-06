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

        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:

            row = init_matrix_representation[0]
            col = init_matrix_representation[1]
            data = init_matrix_representation[2]

            max_row = max(row) + 1
            max_col = max(col) + 1

            arr = [[0 for y in range(max_col)] for x in range(max_row)]

            for i in range(len(row)):
                arr[row[i]][col[i]] = data[i]
            self.init_from_dense(np.array(arr))

        elif isinstance(init_matrix_representation, np.ndarray):
            self.init_from_dense(init_matrix_representation)
        else:
            raise ValueError

    def init_from_dense(self, init_matrix_representation):
        self.data = []
        self.column = []
        self.row = [0]
        cnt = 0
        self.x = len(init_matrix_representation)
        self.y = len(init_matrix_representation[0])
        for i, line in enumerate(init_matrix_representation):
            for j, val in enumerate(line):
                if val != 0:
                    cnt += 1
                    self.data.append(val)
                    self.column.append(j)
            self.row.append(cnt)

    def __getitem__(self, key):
        cnt1 = self.row[key[0]]
        cnt2 = self.row[key[0] + 1]
        tmp = self.data[cnt1:cnt2]
        cols = self.column[cnt1:cnt2]
        for i, c in enumerate(cols):
            if c == key[1]:
                return tmp[i]
        return 0

    def __setitem__(self, key, value):
        index = 0
        count_st = self.row[key[0]]
        count_end = self.row[key[0] + 1]
        if count_end - count_st == 0:
            self.data.insert(sum(self.row[:count_st+1]), value)
            self.column.insert(sum(self.row[:count_st+1]), key[1])
            for i in range(count_st + 1, len(self.row)):
                self.row[i] += 1
        else:
            index = 0
            for i in range[sum(self.row[:count_st+1]): sum(self.row[:count_st+1]) + count_end - count_st]:
                if self.column[i] == key[1]:
                    index = i
                    break


        # cnt2 = self.row[key[0]]
        # for i in self.row[1:key[0]]:
        #     index += i
        # for i in




        # # tmp = self.data[cnt1:cnt2]
        # cols = self.column[cnt1:cnt2]
        # print(cnt1)
        # print(cnt2)
        # print(cols)
        # for i, c in enumerate(cols):
        #     if c == key[1]:
        #         self.data[cnt1 + i] = value
        #         return
        #
        # is_set = False
        # idx = -1
        # self.row[key[0] + 1] += 1
        # for i in range(cnt1, cnt2):
        #     if key[1] < self.column[i]:
        #         self.column.insert(i, key[1])
        #         is_set = True
        #         idx = cnt2 - i
        # if not is_set:
        #     self.column.insert(cnt2, key[1])
        #     idx = cnt2
        # self.data.insert(idx, value)
        # # print(self.data)

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        raise NotImplementedError


a = CSRMatrix(np.array([[0, 0, 0, 0], [5, 8, 0, 0], [0, 0, 3, 0], [0, 6, 0, 0]]))

b = CSRMatrix(([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3], [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
               [0, 0, 0, 0, 5, 8, 0, 0, 0, 0, 3, 0, 0, 6, 0, 0]))
print(a.data, a.row, a.column)
print(b.data, b.row, b.column)
a[0, 3] = 1
print(a.data, a.row, a.column)
# print(a[0,0])
# print(a[1,0])
# print(a[1,1])
# print(a[2,2])
# print(a[3,1])
# print(a[3,3])

# print(a.data)
# print(a.row)
# print(a.column)

# a[1,0] = 1
# a[1,1] = 2
# a[1,0] = 1
# a[0,0] = 1
# print("")
# print(a.data)
# print(a.row)
# print(a.column)
print(a)
print(a[1, 0])
# print("")
# print(a.data)
# print(a.row)
# print(a.column)