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
        self._values = []
        self._cols = []
        self._pointer = [0]
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self._values = init_matrix_representation[2]
            self._cols = init_matrix_representation[1]
            row_ind = init_matrix_representation[0]
            self.shape = (max(row_ind)+1, max(self._cols)+1)
            t = 0
            for i in range(len(row_ind)):
                if row_ind[i] != t:
                    for _ in range(row_ind[i]-t):
                        self._pointer.append(i)
                    t = row_ind[i]
        elif isinstance(init_matrix_representation, np.ndarray):
            count = 0
            t = 0
            for i in range(init_matrix_representation.shape[0]):
                for j in range(init_matrix_representation.shape[1]):
                    element = init_matrix_representation[i, j]
                    if element != 0:
                        self._values.append(element)
                        self._cols.append(j)
                        if i != t:
                            self._pointer.append(count)
                            t = i
                        count += 1
            self.shape = init_matrix_representation.shape
        else:
            raise ValueError

    @property
    def values(self):
        return self._values

    @property
    def cols(self):
        return self._cols

    @property
    def pointer(self):
        return self._pointer

    def __getitem__(self, item):
        if len(item) < 2:
            raise IndexError
        i, j = item
        if i >= self.shape[0] or j >= self.shape[1]:
            return 0
        index = self._pointer[i]
        try:
            next_row = self._pointer[i+1]
        except IndexError:
            if index > len(self._cols)-1:
                return 0
            next_row = index + (self.shape[1] - self._cols[index])
        while self._cols[index] != j:
            if self._cols[index] > j:
                return 0
            index += 1
            if index == next_row or index == len(self._cols):
                return 0
        return self._values[index]

    def __setitem__(self, key, value):
        if len(key) < 2:
            raise IndexError
        i, j = key
        if value == 0:
            if i >= len(self._pointer):
                self._pointer.append(len(self._values))
            return
        if i >= self.shape[0] or j >= self.shape[1]:
            raise IndexError
        try:
            index = self._pointer[i]
            try:
                while self._cols[index] < j:
                    index += 1
                if self._cols[index] == j:
                    self._values[index] = value
                    return
                self._values.insert(index, value)
                self._cols.insert(index, j)
                self._pointer[index+1:] = [k+1 for k in self._pointer[index+1:]]
            except IndexError:
                self._cols.append(j)
                self._values.append(value)
        except IndexError:
            self._cols.append(j)
            self._values.append(value)
            if i > len(self._pointer)-1:
                self._pointer.append(len(self._values)-1)

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        result = np.zeros(self.shape)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                result[i, j] = self.__getitem__([i, j])
        return result

    @property
    def nnz(self):
        return len(self._values)

    def __add__(self, other: 'CSRMatrix'):
        if self.shape != other.shape:
            raise ValueError('Dimension mismatch')
        result = CSRMatrix(np.zeros(self.shape))
        for i in range(self.shape[0]):
            for j in list(set(self.get_row(i)) | set(other.get_row(i))):
                result[i, j] = self.__getitem__([i, j]) + other[i, j]
        return result

    def __sub__(self, other):
        if self.shape != other.shape:
            raise ValueError('Dimension mismatch')
        result = CSRMatrix(np.zeros(self.shape))
        for i in range(self.shape[0]):
            for j in list(set(self.get_row(i)) | set(other.get_row(i))):
                result[i, j] = self.__getitem__([i, j]) - other[i, j]
        return result

    def __mul__(self, other):
        if self.shape != other.shape:
            raise ValueError('Dimension mismatch')
        result = CSRMatrix(np.zeros(self.shape))
        for i in range(self.shape[0]):
            for j in list(set(self.get_row(i)) | set(other.get_row(i))):
                result[i, j] = self.__getitem__([i, j]) * other[i, j]
        return result

    def __rmul__(self, other):
        result = CSRMatrix(np.zeros(self.shape))
        for i in range(self.shape[0]):
            for j in self.get_row(i):
                result[i, j] = self.__getitem__([i, j]) * other
        return result

    def __truediv__(self, other):
        result = CSRMatrix(np.zeros(self.shape))
        for i in range(self.shape[0]):
            for j in self.get_row(i):
                result[i, j] = self.__getitem__([i, j]) / other
        return result

    def __matmul__(self, other):
        if self.shape[0] != other.shape[1]:
            raise ValueError
        result = CSRMatrix(np.zeros((self.shape[0], other.shape[1])))
        other_t = other.transpose()  # чтобы обходить тоже по строкам
        for i in range(self.shape[0]):
            for j in range(other_t.shape[0]):
                element = 0
                row_a = self.get_row(i)
                row_b = other_t.get_row(j)
                p1 = 0
                p2 = 0
                while p1 < len(row_a) and p2 < len(row_b):
                    if row_a[p1] == row_b[p2]:
                        element += self.__getitem__([i, row_a[p1]]) * other_t[j, row_b[p2]]
                        p1 += 1
                        p2 += 1
                    else:
                        if row_a[p1] > row_b[p2]:
                            p2 += 1
                        else:
                            p1 += 1
                result[i, j] = element
        return result

    def get_row(self, i):
        if i == self.shape[0] - 1:
            first = self._pointer[i]
            last = len(self._cols)
        else:
            first = self._pointer[i]
            last = self._pointer[i+1]
        return self._cols[first:last]

    def transpose(self):
        result = CSRMatrix(np.zeros((1, 1)))
        vect1 = [[] for _ in range(self.shape[1])]
        vect2 = [[] for _ in range(self.shape[1])]
        for i in range(self.shape[0]):
            for j in self.get_row(i):
                vect1[j].append(i)
                vect2[j].append(self.__getitem__([i, j]))
        result._values = [i for j in vect2 for i in j]
        result._cols = [i for j in vect1 for i in j]
        result._pointer = [0 for _ in range(len(vect1))]
        for i in range(1, len(vect1)):
            result._pointer[i] = result._pointer[i-1] + len(vect1[i-1])
        result.shape = self.shape[1], self.shape[0]
        return result
