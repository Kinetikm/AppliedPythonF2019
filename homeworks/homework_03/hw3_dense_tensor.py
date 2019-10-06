#!/usr/bin/env python
# coding: utf-8

from copy import deepcopy
from itertools import product
import numpy as np


class Tensor:
    """
    Your realisation of numpy tensor.

    Must be implemented:
    1. Getting and setting element by indexes of row and col.
    a[i, j] = v -- set value in i-th row and j-th column to value.
    b = a[i, j] -- get value from i-th row and j-th column.
    2. Pointwise operations.
    c = a + b -- sum of two Tensors of the same shape or sum with scalar.
    c = a - b -- difference --//--.
    c = a * b -- product --//--.
    c = a / alpha -- divide Tensor a by nonzero scalar alpha.
    c = a ** b -- raises each element of a to the power b.
    3. Sum, mean, max, min, argmax, argmin by axis.
    if axis is None then operation over all elements.
    4. Transpose by given axes (by default reverse dimensions).
    5. Swap two axes.
    6. Matrix multiplication for tensors with dimension <= 2.
    """

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: list of lists
        """
        self.tensor = init_matrix_representation
        self.sizes = []
        self.dim = self.def_dim(init_matrix_representation)

    def def_dim(self, matrix, dim=0):
        if isinstance(matrix, list):
            if not matrix:
                return dim
            dim += 1
            self.sizes.append(len(matrix))
            dim = self.def_dim(matrix[0], dim)
            return dim
        else:
            # нужно ли возвращать None, если dim == 0?
            return dim

    def __getitem__(self, coordinates):
        if (self.dim == 1) or isinstance(coordinates, int):
            return coordinates
        el = self.tensor
        for i in coordinates:
            el = el[i]
        return el

    def __setitem__(self, coordinates, value):
        if (self.dim == 1) or isinstance(coordinates, int):
            self.tensor[coordinates] = value
            return
        el = self.tensor
        for i in range(len(coordinates) - 1):
            el = el[coordinates[i]]
        el[coordinates[-1]] = value

    def __add__(self, other):
        coordinates = [range(size) for size in self.sizes]
        res = deepcopy(self)
        if isinstance(other, Tensor):
            if (self.dim != other.dim) or (self.sizes != other.sizes):
                raise ValueError('different tensors')
            for i in product(*coordinates):
                res[i] = self[i] + other[i]
            return res
        if isinstance(other, int) or isinstance(other, float):
            for i in product(*coordinates):
                res[i] = self[i] + other
            return res

    def __sub__(self, other):
        coordinates = [range(size) for size in self.sizes]
        res = deepcopy(self)
        if isinstance(other, Tensor):
            if (self.dim != other.dim) or (self.sizes != other.sizes):
                raise ValueError('different tensors')
            for i in product(*coordinates):
                res[i] = self[i] - other[i]
            return res
        if isinstance(other, int) or isinstance(other, float):
            for i in product(*coordinates):
                res[i] = self[i] - other
            return res

    def __mul__(self, other):
        coordinates = [range(size) for size in self.sizes]
        res = deepcopy(self)
        if isinstance(other, Tensor):
            if (self.dim != other.dim) or (self.sizes != other.sizes):
                raise ValueError('different tensors')
            for i in product(*coordinates):
                res[i] = self[i] * other[i]
            return res
        if isinstance(other, int) or isinstance(other, float):
            for i in product(*coordinates):
                res[i] = self[i] * other
            return res

    def __radd__(self, other):
        res = deepcopy(self)
        res = self + other
        return res

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        res = deepcopy(self)
        res = self * (1/other)
        return res

    def __pow__(self, other):
        coordinates = [range(size) for size in self.sizes]
        res = deepcopy(self)
        if isinstance(other, Tensor):
            if (self.dim != other.dim) or (self.sizes != other.sizes):
                raise ValueError('different tensors')
            for i in product(*coordinates):
                res[i] = self[i] ** other[i]
            return res
        if isinstance(other, int) or isinstance(other, float):
            for i in product(*coordinates):
                res[i] = self[i] ** other
            return res

    def sum(self, axis=None):
        if axis is None:
            res = []
            coordinates = [range(size) for size in self.sizes]
            for i in product(*coordinates):
                res.append(self[i])
            return sum(res)
        else:
            s = self.sizes
            size = s.pop(axis)
            coordinates = [range(size) for size in s]
            res = deepcopy(self)
            for i in product(*coordinates):
                lst = []
                i = list(i)
                for j in range(size):
                    i.insert(axis, j)
                    lst.append(self[i])
                    i.pop(axis)
                res[i] = sum(lst)
            return res.tensor

    def mean(self, axis=None):
        if axis is None:
            res = []
            coordinates = [range(size) for size in self.sizes]
            for i in product(*coordinates):
                res.append(self[i])
            return sum(res)/len(res)
        else:
            s = self.sizes
            size = s.pop(axis)
            coordinates = [range(size) for size in s]
            res = deepcopy(self)
            for i in product(*coordinates):
                lst = []
                i = list(i)
                for j in range(size):
                    i.insert(axis, j)
                    lst.append(self[i])
                    i.pop(axis)
                res[i] = sum(lst)/len(lst)
            return res.tensor

    def max(self, axis=None):
        if axis is None:
            res = []
            coordinates = [range(size) for size in self.sizes]
            for i in product(*coordinates):
                res.append(self[i])
            max_value = max(res)
            return max_value
        else:
            s = self.sizes
            size = s.pop(axis)
            coordinates = [range(size) for size in s]
            res = deepcopy(self)
            for i in product(*coordinates):
                lst = []
                i = list(i)
                for j in range(size):
                    i.insert(axis, j)
                    lst.append(self[i])
                    i.pop(axis)
                res[i] = max(lst)
            return res.tensor

    def min(self, axis=None):
        if axis is None:
            res = []
            coordinates = [range(size) for size in self.sizes]
            for i in product(*coordinates):
                res.append(self[i])
            min_value = min(res)
            return min_value
        else:
            s = self.sizes
            size = s.pop(axis)
            coordinates = [range(size) for size in s]
            res = deepcopy(self)
            for i in product(*coordinates):
                lst = []
                i = list(i)
                for j in range(size):
                    i.insert(axis, j)
                    lst.append(self[i])
                    i.pop(axis)
                res[i] = min(lst)
            return res.tensor

    def argmax(self, axis=None):
        if axis is None:
            res = []
            coordinates = [range(size) for size in self.sizes]
            for i in product(*coordinates):
                res.append(self[i])
            max_value = max(res)
            return res.index(max_value)
        else:
            s = self.sizes
            size = s.pop(axis)
            coordinates = [range(size) for size in s]
            res = deepcopy(self)
            for i in product(*coordinates):
                lst = []
                i = list(i)
                for j in range(size):
                    i.insert(axis, j)
                    lst.append(self[i])
                    i.pop(axis)
                res[i] = lst.index(res[i])
            return res.tensor

    def argmin(self, axis=None):
        if axis is None:
            res = []
            coordinates = [range(size) for size in self.sizes]
            for i in product(*coordinates):
                res.append(self[i])
            min_value = min(res)
            return res.index(min_value)
        else:
            s = self.sizes
            size = s.pop(axis)
            coordinates = [range(size) for size in s]
            res = deepcopy(self)
            for i in product(*coordinates):
                lst = []
                i = list(i)
                for j in range(size):
                    i.insert(axis, j)
                    lst.append(self[i])
                    i.pop(axis)
                res[i] = lst.index(res[i])
            return res.tensor

    def transpose(self, *axis):
        axis = list(axis)
        if len(axis) < self.dim:
            raise ValueError("axes don't match array")
        res = deepcopy(self)
        res.sizes = list(np.array(self.sizes)[axis])
        coordinates = [range(size) for size in self.sizes]
        for i in product(*coordinates):
            index = np.array(i)
            index = index[axis]
            res[index] = self[i]
        return res

    def swapaxes(self, ax1, ax2):
        new_dim = list(range(len(self.sizes)))
        new_dim[ax1], new_dim[ax2] = new_dim[ax2], new_dim[ax1]
        return self.transpose(*new_dim)

    def __matmul__(self, other: 'Tensor'):
        if not self.dim <= 2 and other.dim <= 2:
            raise ValueError("Tensor rang greater then 2")
        if self.dim == 1:
            # vector * matrix
            if self.sizes[0] != other.sizes[0]:
                raise ValueError("Dimension mismatch")
            res = np.zeros((other.sizes[1]))
            for y in range(res.shape[0]):
                res[y] = sum((self.__getitem__(j) * other[j, y] for j in range(other.sizes[0])))
            return Tensor(res.tolist())
        if other.dim == 1:
            # matrix * vector
            if self.sizes[1] != other.sizes[0]:
                raise ValueError("Dimension mismatch")
            res = np.zeros((self.sizes[0]))
            for x in range(res.shape[0]):
                res[x] = sum((self.__getitem__([x, j]) * other[j] for j in range(other.sizes[0])))
            return Tensor(res.tolist())
        if self.sizes[1] != other.sizes[0]:
            raise ValueError("Dimension mismatch")
        else:
            res = np.zeros((self.sizes[0], other.sizes[1]))
        for x in range(res.shape[0]):
            for y in range(res.shape[1]):
                res[x, y] = sum((self.__getitem__([x, j]) * other[j, y] for j in range(other.sizes[0])))
        return Tensor(res.tolist())
