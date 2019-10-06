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

    @classmethod
    def create(cls, size):
        num_of_elements = 1
        for s in size:
            num_of_elements *= s
        empty_matrix = [0 for i in range(num_of_elements)]
        for i in range(1, len(size)):
            help_list = []
            for j in range(len(empty_matrix)):
                help_list.append(empty_matrix.pop(0))
                if (j + 1) % size[-i] == 0:
                    empty_matrix.append(help_list)
                    help_list = []
        return cls(empty_matrix)

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

    def size(self):
        size = [len(self.tensor)]
        el = self.matrix
        while isinstance(el[0], list):
            size.append(len(el[0]))
            el = el[0]
        return size

    def __getitem__(self, coordinates):
        if (self.dim == 1) or isinstance(coordinates, int):
            return coordinates
        el = self.tensor
        for i in coordinates:
            el = el[i]
        return el

    def __setitem__(self, coordinates, value):
        if self.dim == 1:
            self.tensor[coordinates] = value
            return
        el = self.tensor
        for i in range(len(coordinates) - 1):
            el = el[coordinates[i]]
        el[coordinates[-1]] = value

    def __add__(self, other):
        size = self.size()
        coordinates = [range(idx) for idx in size]
        res = Tensor.create(size)
        if isinstance(other, Tensor):
            if (self.dim != other.dim) or (self.sizes != self.sizes):
                raise ValueError('different tensors')
            for i in product(*coordinates):
                res[i] = self[i] + other[i]
            return res
        elif isinstance(other, int) or isinstance(other, float):
            for i in product(*coordinates):
                res[i] = self[i] + other
            return res

    def __sub__(self, other):
        size = self.size()
        coordinates = [range(idx) for idx in size]
        res = Tensor.create(size)
        if isinstance(other, Tensor):
            if (self.dim != other.dim) or (self.sizes != self.sizes):
                raise ValueError('different tensors')
            for i in product(*coordinates):
                res[i] = self[i] - other[i]
            return res
        elif isinstance(other, int) or isinstance(other, float):
            for i in product(*coordinates):
                res[i] = self[i] - other
            return res

    def __mul__(self, other):
        size = self.size()
        coordinates = [range(idx) for idx in size]
        res = Tensor.create(size)
        if isinstance(other, Tensor):
            if (self.dim != other.dim) or (self.sizes != self.sizes):
                raise ValueError('different tensors')
            for i in product(*coordinates):
                res[i] = self[i] * other[i]
            return res
        elif isinstance(other, int) or isinstance(other, float):
            for i in product(*coordinates):
                res[i] = self[i] * other
            return res

    def __radd__(self, other):
        return self + other

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        size = self.size()
        coordinates = [range(idx) for idx in size]
        res = Tensor.create(size)
        if isinstance(other, Tensor):
            raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            for i in product(*coordinates):
                res[i] = self[i] / other
            return res

    def __pow__(self, other):
        size = self.size()
        coordinates = [range(idx) for idx in size]
        res = Tensor.create(size)
        if isinstance(other, Tensor):
            if (self.dim != other.dim) or (self.sizes != self.sizes):
                raise ValueError('different tensors')
            for i in product(*coordinates):
                res[i] = self[i] ** other[i]
            return res
        elif isinstance(other, int) or isinstance(other, float):
            for i in product(*coordinates):
                res[i] = self[i] ** other
            return res

    def sum(self, axis=None):
        size = self.size()
        if axis is None:
            res = []
            coordinates = [range(idx) for idx in size]
            for i in product(*coordinates):
                res.append(self[i])
            return sum(res)
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            res = Tensor.create(size)
            for i in product(*coordinates):
                lst = []
                i = list(i)
                for j in range(idx):
                    i.insert(axis, j)
                    lst.append(self[i])
                    i.pop(axis)
                res[i] = sum(lst)
            return res

    def mean(self, axis=None):
        size = self.size()
        if axis is None:
            res = []
            coordinates = [range(idx) for idx in size]
            for i in product(*coordinates):
                res.append(self[i])
            return sum(res)/len(res)
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            res = Tensor.create(size)
            for i in product(*coordinates):
                lst = []
                i = list(i)
                for j in range(idx):
                    i.insert(axis, j)
                    lst.append(self[i])
                    i.pop(axis)
                res[i] = sum(lst)/len(lst)
            return res

    def max(self, axis=None):
        size = self.size()
        if axis is None:
            res = []
            coordinates = [range(idx) for idx in size]
            for i in product(*coordinates):
                res.append(self[i])
            max_e = max(res)
            return max_e
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            res = Tensor.create(size)
            for i in product(*coordinates):
                lst = []
                i = list(i)
                for j in range(idx):
                    i.insert(axis, j)
                    lst.append(self[i])
                    i.pop(axis)
                res[i] = max(lst)
            return res 

    def min(self, axis=None):
        size = self.size()
        if axis is None:
            res = []
            coordinates = [range(idx) for idx in size]
            for i in product(*coordinates):
                res.append(self[i])
            min_e = min(res)
            return min_e
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            res = Tensor.create(size)
            for i in product(*coordinates):
                lst = []
                i = list(i)
                for j in range(idx):
                    i.insert(axis, j)
                    lst.append(self[i])
                    i.pop(axis)
                res[i] = min(lst)
            return res

    def argmax(self, axis=None):
        size = self.size()
        if axis is None:
            res = []
            coordinates = [range(idx) for idx in size]
            for i in product(*coordinates):
                res.append(self[i])
            max_e = max(res)
            return res.insex(max_e)
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            res = Tensor.create(size)
            for i in product(*coordinates):
                lst = []
                i = list(i)
                for j in range(idx):
                    i.insert(axis, j)
                    lst.append(self[i])
                    i.pop(axis)
                res[i] = lst.index(res[i])
            return res

    def argmin(self, axis=None):
        size = self.size()
        if axis is None:
            res = []
            coordinates = [range(idx) for idx in size]
            for i in product(*coordinates):
                res.append(self[i])
            min_e = min(res)
            return res.index(min_e)
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            res = Tensor.create(size)
            for i in product(*coordinates):
                lst = []
                i = list(i)
                for j in range(idx):
                    i.insert(axis, j)
                    lst.append(self[i])
                    i.pop(axis)
                res[i] = lst.index(res[i])
            return res

    def transpose(self, *axis):
        size = self.size()
        new_size = [size[d] for d in axis]
        res = Tensor.create(new_size)
        coordinates = [range(s) for s in size]
        for i in product(*coordinates):
            new_i = [i[d] for d in axis]
            res[new_i] = self[i]
        return res

    def swapaxes(self, ax1, ax2):
        new_dim = list(range(len(self.size())))
        new_dim[ax1], new_dim[ax2] = new_dim[ax2], new_dim[ax1]
        return self.transpose(*new_dim)

    def __matmul__(self, other):
        l1, l2 = len(self.size()), len(other.size())
        tensor1 = Tensor([self.matrix]) if l1 == 1 else self
        tensor2 = Tensor([[el] for el in other.matrix]) if l2 == 1 else other
        num1_of_rows, num1_of_columns = tensor1.size()
        num2_of_rows, num2_of_columns = tensor2.size()
        if num1_of_columns != num2_of_rows:
            raise ValueError
        n = num1_of_columns
        tensor2 = tensor2.transpose(1, 0)
        result = Tensor.create_empty_tensor((num1_of_rows, num2_of_columns))
        for i, row1 in enumerate(tensor1.matrix):
            for j, row2 in enumerate(tensor2.matrix):
                result[i, j] = sum([row1[k]*row2[k] for k in range(n)])
        result = Tensor(result.matrix[0]) if l1 == 1 else result
        result = Tensor([el[0] for el in result.matrix]) if l2 == 1 else result
        return result
