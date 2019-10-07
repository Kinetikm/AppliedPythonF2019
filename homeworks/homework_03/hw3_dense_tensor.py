#!/usr/bin/env python
# coding: utf-8
import itertools
import copy
import numpy


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
        self.shape = []
        self.d = self._dimension(init_matrix_representation)
        if self.d is not None:
            self.items = init_matrix_representation
            for i in range(self.d - 1):
                self.items = [el for el in itertools.chain.from_iterable(self.items)]
            if self._multiply(self.shape) != len(self.items):
                raise ValueError
        else:
            raise ValueError

    def _multiply(self, shape):
        result = 1
        for i in shape:
            result *= i
        return result

    def _dimension(self, test, d=0):
        if not isinstance(test, list):
            return None if d == 0 else d
        else:
            d += 1
            self.shape.append(len(test))
            d = self._dimension(test[0], d)
            return d

    def __getitem__(self, indexes):
        ptr = 0
        if self.d == 1:
            return self.items[indexes]
        for i in range(len(indexes)):
            if indexes[i] >= self.shape[i]:
                raise IndexError
            ptr += int(self._multiply(self.shape[i + 1:])) * indexes[i]
        return self.items[ptr]

    def __setitem__(self, indexes, value):
        ptr = 0
        if self.d == 1:
            self.items[indexes] = value
        for i in range(len(indexes)):
            if indexes[i] >= self.shape[i]:
                raise IndexError
            ptr += int(self._multiply(self.shape[i + 1:])) * indexes[i]
        self.items[ptr] = value

    def _operations(self, other, sign):
        new_items = copy.deepcopy(self)
        if sign == "+":
            for i in range(len(self.items)):
                new_items.items[i] = self.items[i] + other
            return new_items
        if sign == "-":
            for i in range(len(self.items)):
                new_items.items[i] = self.items[i] - other
            return new_items
        if sign == "*":
            for i in range(len(self.items)):
                new_items.items[i] = self.items[i] * other
            return new_items
        if sign == "/":
            for i in range(len(self.items)):
                new_items.items[i] /= other
            return new_items
        if sign == "^":
            for i in range(len(self.items)):
                new_items.items[i] = pow(new_items.items[i], other)
            return new_items

    def __add__(self, other):
        if not isinstance(other, Tensor):
            return self._operations(other, "+")
        if self.shape != other.shape:
            raise ValueError
        new_items = copy.deepcopy(other)
        for i in range(len(self.items)):
            new_items.items[i] = self.items[i] + other.items[i]
        return new_items

    def __sub__(self, other):
        if not isinstance(other, Tensor):
            return self._operations(other, "-")
        if self.shape != other.shape:
            raise ValueError
        new_items = copy.deepcopy(other)
        for i in range(len(self.items)):
            new_items.items[i] = self.items[i] - other.items[i]
        return new_items

    def __mul__(self, other):
        if not isinstance(other, Tensor):
            return self._operations(other, "*")
        if self.shape != other.shape:
            raise ValueError
        new_items = copy.deepcopy(other)
        for i in range(len(self.items)):
            new_items.items[i] = self.items[i] * other.items[i]
        return new_items

    def __radd__(self, other):
        return self._operations(other, "+")

    def __rsub__(self, other):
        return self._operations(other, "-")

    def __rmul__(self, other):
        return self._operations(other, "*")

    def __truediv__(self, other):
        return self._operations(other, "/")

    def __pow__(self, other, modulo=None):
        return self._operations(other, "^")

    def _getindex(self, pos):
        if pos >= len(self.items):
            raise IndexError
        if self.d == 1:
            return pos
        ixs = [0 for _ in range(self.d)]
        for i in range(self.d):
            ixs[i] = int(pos // (self._multiply(self.shape[i + 1:])))
            pos = int(pos % (self._multiply(self.shape[i + 1:])))
        return ixs

    def sum(self, axis=None):
        if axis is None:
            return sum(self.items)
        new_shape = [self.shape[i] for i in range(self.d) if i != axis]
        res = numpy.zeros(new_shape)
        selected_index = [i for i in range(self.d) if i != axis]
        for i in range(len(self.items)):
            index = self._getindex(i)
            index = [index[j] for j in selected_index]
            res[tuple(index)] += self.items[i]
        return res

    def mean(self, axis=None):
        if axis is None:
            return sum(self.items) / len(self.items)
        new_shape = [self.shape[i] for i in range(self.d) if i != axis]
        res = numpy.zeros(new_shape)
        selected_index = [i for i in range(self.d) if i != axis]
        for i in range(len(self.items)):
            index = self._getindex(i)
            index = [index[j] for j in selected_index]
            res[tuple(index)] += self.items[i]
        return res / self.shape[axis]

    def max(self, axis=None):
        if axis is None:
            return max(self.items)
        new_shape = [self.shape[i] for i in range(self.d) if i != axis]
        res = numpy.zeros(new_shape)
        selected_index = [i for i in range(self.d) if i != axis]
        for i in range(len(self.items)):
            index = self._getindex(i)
            index = [index[j] for j in selected_index]
            if res[tuple(index)] < self.items[i]:
                res[tuple(index)] = self.items[i]
        return res

    def min(self, axis=None):
        if axis is None:
            return min(self.items)
        new_shape = [self.shape[i] for i in range(self.d) if i != axis]
        res = numpy.zeros(new_shape)
        selected_index = [i for i in range(self.d) if i != axis]
        for i in range(len(self.items)):
            index = self._getindex(i)
            index = [index[j] for j in selected_index]
            if res[tuple(index)] > self.items[i]:
                res[tuple(index)] = self.items[i]
        return res

    def argmax(self, axis=None):
        if axis is None:
            return self.items.index(max(self.items))
        new_shape = [self.shape[i] for i in range(self.d) if i != axis]
        res = numpy.zeros(new_shape)
        res_indexes = numpy.zeros(new_shape)
        selected_index = [i for i in range(self.d) if i != axis]
        for i in range(len(self.items)):
            index = self._getindex(i)
            index_sel = [index[j] for j in selected_index]
            if res[tuple(index_sel)] < self.items[i]:
                res[tuple(index_sel)] = self.items[i]
                res_indexes[tuple(index_sel)] = index[axis]
        return res_indexes.astype(int)

    def argmin(self, axis=None):
        if axis is None:
            return self.items.index(min(self.items))
        new_shape = [self.shape[i] for i in range(self.d) if i != axis]
        res = numpy.zeros(new_shape)
        res_indexes = numpy.zeros(new_shape)
        selected_index = [i for i in range(self.d) if i != axis]
        for i in range(len(self.items)):
            index = self._getindex(i)
            index_sel = [index[j] for j in selected_index]
            if res[tuple(index_sel)] > self.items[i]:
                res[tuple(index_sel)] = self.items[i]
                res_indexes[tuple(index_sel)] = index[axis]
        return res_indexes.astype(int)

    def transpose(self, *axis):
        axis = list(axis)
        if len(axis) < self.d:
            raise ValueError
        res = copy.deepcopy(self)
        res.shape = list(numpy.array(self.shape)[axis])
        for i in range(len(self.items)):
            index = numpy.array(self._getindex(i))
            index = index[axis]
            res[index] = self.items[i]
        return res

    def swapaxes(self, axis_1, axis_2):
        shape2 = copy.copy(self.shape)
        shape2[axis_1], shape2[axis_2] = shape2[axis_2], shape2[axis_1]
        res = copy.deepcopy(self)
        res.shape = shape2
        for i in range(len(self.items)):
            index = numpy.array(self._getindex(i))
            index[axis_1], index[axis_2] = index[axis_2], index[axis_1]
            res[index] = self.items[i]
        return res

    def __matmul__(self, other: 'Tensor'):
        if not self.d <= 2 and other.d <= 2:
            raise ValueError
        if self.d == 1:
            if self.shape[0] != other.shape[0]:
                raise ValueError
            res = numpy.zeros((other.shape[1]))
            for y in range(res.shape[0]):
                res[y] = sum((self.__getitem__(j) * other[j, y] for j in range(other.shape[0])))
            return Tensor(res.tolist())
        if other.d == 1:
            if self.shape[1] != other.shape[0]:
                raise ValueError
            res = numpy.zeros((self.shape[0]))
            for x in range(res.shape[0]):
                res[x] = sum((self.__getitem__([x, j]) * other[j] for j in range(other.shape[0])))
            return Tensor(res.tolist())
        if self.shape[1] != other.shape[0]:
            raise ValueError
        else:
            res = numpy.zeros((self.shape[0], other.shape[1]))
        for x in range(res.shape[0]):
            for y in range(res.shape[1]):
                res[x, y] = sum((self.__getitem__([x, j]) * other[j, y] for j in range(other.shape[0])))
        return Tensor(res.tolist())
