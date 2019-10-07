#!/usr/bin/env python
# coding: utf-8


from numbers import Number
from functools import reduce
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

    def getError():
        raise TypeError

    def get_data(tensor, array):
        if len(tensor) == 0:
            return
        if issubclass(type(tensor[0]), Number):
            array += tensor
        else:
            for item in tensor:
                Tensor.get_data(item, array)

    def get_ranges(tensor, ranges):
        if len(tensor) == 0:
            return
        if issubclass(type(tensor[0]), Number):
            ranges.append(len(tensor))
        else:
            ranges.append(len(tensor))
            Tensor.get_ranges(tensor[0], ranges)

    def new_tensor(array, shape):
        tensor = Tensor([])
        tensor._data = array
        tensor._ranges = shape
        return tensor

    def __init__(self, matrix):
        """
        :param init_matrix_representation: list of lists
        """
        self._data = []
        self._ranges = []
        Tensor.get_data(matrix, self._data)
        Tensor.get_ranges(matrix, self._ranges)
        if len(self._ranges) == 1:
            self._ranges.append(1)
        self._ranges = tuple(self._ranges)
        self.base_operator = {"add": lambda a, b: a + b,
                              "sub": lambda a, b: a - b,
                              "mul": lambda a, b: a * b,
                              "div": lambda a, b: a/b,
                              "pow": lambda a, b: a ** b}

        self.tensor_operator = {"add": lambda a, b: a + b,
                                "sub": lambda a, b: a - b,
                                "mul": lambda a, b: a * b,
                                "div": Tensor.getError,
                                "pow": Tensor.getError}

    def apply_operator(self, operator, other):
        if isinstance(other, Tensor):
            if self._ranges != other._ranges:
                raise ValueError
            array = [self.tensor_operator[operator](a, b) for a, b in zip(self._data, other._data)]
        elif isinstance(other, Number):
            array = [self.base_operator[operator](a, other) for a in self._data]
        else:
            raise TypeError
        return Tensor.new_tensor(array, self._ranges)

    def _get_index(self, keys):
        index = 0
        t = reduce(lambda x, y: x * y, self._ranges, 1)
        for i, key in enumerate(keys):
            t = int(t/self._ranges[i])
            index += key * t
        return index

    def toList(self, index, axs):
        if len(self._ranges) - axs == 1:
            return self._data[index:index + self._ranges[-1]]
        else:
            res = []
            n = self._ranges[axs]
            length = 1
            for i in range(axs + 1, len(self._ranges)):
                length *= self._ranges[i]
            for i in range(n):
                res.append(self.toList(index + i * length, axs + 1))
            return res

    def __getitem__(self, keys):
        if type(keys) == int:
            keys = [keys]
        if len(keys) == len(self._ranges):
            return self._data[self._get_index(keys)]
        elif len(keys) < len(self._ranges):
            res = self.toList(self._get_index(keys), len(keys))
            if len(res) == 1 and isinstance(res[0], Number):
                return res[0]
            return res
        else:
            print(self._ranges, "!=", keys)
            raise IndexError

    def __setitem__(self, keys, value):
        index = self._get_index(keys)
        if len(keys) == len(self._ranges):
            self._data[index] = value
        else:
            raise ValueError

    def __add__(self, other):
        return self.apply_operator("add", other)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return self.apply_operator("mul", other)

    def __rmul__(self, other):
        return self * other

    def __sub__(self, other):
        return self.apply_operator("sub", other)

    def __rsub__(self, other):
        return self - other

    def __truediv__(self, alpha):
        if not isinstance(alpha, Number):
            raise TypeError
        if abs(alpha) < 10e-10:
            raise ZeroDivisionError
        return self.apply_operator("div", alpha)

    def __matmul__(self, other):
        if not isinstance(other, Tensor):
            raise TypeError
        if not (len(self._ranges) <= 2 and len(other._ranges) <= 2):
            raise ValueError

        l = self._ranges[0]
        m1 = self._ranges[1]
        m2 = other._ranges[0]
        n = other._ranges[1]

        if m1 == 1:
            # mul vector on matrix
            array = [0 for _ in range(n)]
            for i in range(l):
                for j in range(n):
                    array[j] += self[i] * other[i, j]
            return Tensor(array)

        if m1 != m2:
            raise ValueError
        else:
            m = m1

        array = [0 for _ in range(l * n)]
        tensor = Tensor.new_tensor(array, (l, n))

        for i in range(l):
            for j in range(n):
                for r in range(m):
                    tensor[i, j] += self[i, r] * other[r, j]
        return tensor

    def __pow__(self, other):
        return self.apply_operator("pow", other)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return str(self._data)

    def transpose(self, *axis):
        matrix = self.toList(0, 0)
        if len(axis) == 0:
            axis = None
        matrix = np.array(matrix)
        return matrix.transpose(axis)

    def sum(self, axis=None):
        # В случае axis is None я могу реализовать sum,min,max,mean,argmax,argmin,
        #   во всех остальных приходиться использовать numpy
        if axis is None:
            return sum(self._data)
        matrix = self.toList(0, 0)
        matrix = np.array(matrix)
        return matrix.sum(axis)

    def min(self, axis=None):
        if axis is None:
            return min(self._data)
        matrix = self.toList(0, 0)
        matrix = np.array(matrix)
        return matrix.min(axis)

    def max(self, axis=None):
        if axis is None:
            return max(self._data)
        matrix = self.toList(0, 0)
        matrix = np.array(matrix)
        return matrix.max(axis)

    def mean(self, axis=None):
        if axis is None:
            return self.sum()/len(self._data)
        matrix = self.toList(0, 0)
        matrix = np.array(matrix)
        return matrix.mean(axis)

    def argmax(self, axis=None):
        matrix = self.toList(0, 0)
        matrix = np.array(matrix)
        return matrix.argmax(axis)

    def argmin(self, axis=None):
        matrix = self.toList(0, 0)
        matrix = np.array(matrix)
        return matrix.argmin(axis)

    def swapaxes(self, first, second):
        matrix = self.toList(0, 0)
        matrix = np.array(matrix)
        return matrix.swapaxes(first, second)
