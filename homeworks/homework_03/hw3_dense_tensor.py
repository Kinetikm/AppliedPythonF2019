#!/usr/bin/env python
# coding: utf-8
import copy
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

    def __init__(self, init_matrix_representation=None):
        """
        :param init_matrix_representation: list of lists
        """
        self.dimensions = {}
        self.data = []
        self.dim_offset = {}
        if init_matrix_representation is not None:
            if not isinstance(init_matrix_representation, list):
                raise ValueError
            self._roll(init_matrix_representation, 0)
            self._calculate_offsets()

    def _calculate_offsets(self):
        self.dim_offset[len(self.dimensions) - 1] = 1
        for i in range(len(self.dimensions) - 2, -1, -1):
            self.dim_offset[i] = self.dim_offset[i + 1] * self.dimensions[i + 1]

    def from_tensor(self):
        ret = Tensor()
        ret.dimensions = copy.deepcopy(self.dimensions)
        ret.dim_offset = copy.deepcopy(self.dim_offset)
        ret.data = copy.deepcopy(self.data)
        return ret

    def _roll(self, obj, dim):
        if dim in self.dimensions:
            if self.dimensions[dim] != len(obj):
                raise ValueError
        else:
            self.dimensions[dim] = len(obj)
        if all(isinstance(el, list) for el in obj):
            for el in obj:
                self._roll(el, dim + 1)
        elif all(isinstance(el, (float, int)) for el in obj):
            for el in obj:
                self.data.append(el)
        else:
            raise ValueError

    def __getitem__(self, key):
        if not isinstance(key, (tuple, int)):
            raise IndexError
        if isinstance(key, tuple) and len(key) != len(self.dimensions):
            raise IndexError
        if isinstance(key, int):
            if 0 <= key < len(self.data):
                return self.data[key]
            else:
                raise IndexError
        for i, ind in enumerate(key):
            if ind < 0 or ind >= self.dimensions[i]:
                raise IndexError
        index = 0
        for i, ind in enumerate(key):
            index += ind * self.dim_offset[i]
        return self.data[index]

    def __setitem__(self, key, value):
        if not isinstance(key, tuple):
            raise IndexError
        if not isinstance(value, (int, float, np.int, np.float, np.int64)):
            raise ValueError
        if len(key) != len(self.dimensions):
            raise IndexError
        for i, ind in enumerate(key):
            if ind < 0 or ind >= self.dimensions[i]:
                raise IndexError
        index = 0
        for i, ind in enumerate(key[:len(key):]):
            index += ind * self.dim_offset[i]
        self.data[index] = value

    def __add__(self, other):
        res = self.from_tensor()
        if isinstance(other, Tensor):
            if self.dimensions == other.dimensions:
                for i, val in enumerate(self.data):
                    res.data[i] = val + other.data[i]
            else:
                raise ValueError
        elif isinstance(other, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                res.data[i] = val + other
        return res

    def __radd__(self, other):
        res = self.from_tensor()
        if isinstance(other, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                res.data[i] = val + other
        return res

    def __sub__(self, other):
        res = self.from_tensor()
        if isinstance(other, Tensor):
            if self.dimensions == other.dimensions:
                for i, val in enumerate(self.data):
                    res.data[i] = val - other.data[i]
            else:
                raise ValueError
        elif isinstance(other, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                res.data[i] = val - other
        return res

    def __mul__(self, other):
        res = self.from_tensor()
        if isinstance(other, Tensor):
            if self.dimensions == other.dimensions:
                for i, val in enumerate(self.data):
                    res.data[i] = val * other.data[i]
            else:
                raise ValueError
        elif isinstance(other, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                res.data[i] = val * other
        return res

    def __truediv__(self, other):
        res = self.from_tensor()
        if isinstance(other, (int, float, np.int, np.float, np.int64)):
            if other == 0:
                raise ZeroDivisionError
            for i, val in enumerate(self.data):
                res.data[i] = val / other
        return res

    def __pow__(self, power, modulo=None):
        res = self.from_tensor()
        if isinstance(power, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                res.data[i] = val ** power
        return res

    def _create_smaller(self, axis):
        res = Tensor()
        for k in self.dimensions:
            if k > axis:
                res.dimensions[k - 1] = self.dimensions[k]
            elif k == axis:
                continue
            else:
                res.dimensions[k] = self.dimensions[k]
        res._calculate_offsets()
        return res

    def sum(self, axis=None):
        if axis is None:
            res = 0
            for i in self.data:
                res += i
            return res
        else:
            res = self._create_smaller(axis)
            n_el = len(self.data) // self.dimensions[axis]
            res.data = [0] * n_el
            dims = []
            for i in range(len(self.dimensions)):
                dims.append(self.dimensions[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                i.pop(axis)
                res[tuple(i)] += self[index]
            return res

    def to_list(self):
        if len(self.dimensions) == 1:
            return self.data
        return self._get_as_list(self.data, len(self.dimensions) - 1)

    def _get_as_list(self, arr,  dim):
        if dim == (len(self.dimensions) - 1):
            dims = []
            v = []
            for i in range(len(self.dimensions)):
                dims.append(self.dimensions[i])
            for index in product(*[range(k) for k in dims]):
                v.append(self[index])
            arr = v
        if dim > 0:
            l1 = list()
            l2 = list()
            n = self.dimensions[dim]
            for i, item in enumerate(arr):
                l2.append(copy.deepcopy(item))
                if i >= 0 and (i + 1) % n == 0:
                    l1.append(copy.deepcopy(l2))
                    l2.clear()
            return self._get_as_list(l1, dim - 1)
        else:
            return arr

    def mean(self, axis=None):
        if axis is None:
            ret = 0
            for i in self.data:
                ret += i
            return ret / len(self.data)
        else:
            t = self.sum(axis)
            for i, it in enumerate(t.data):
                t.data[i] = it / self.dimensions[axis]
            return t

    def min(self, axis=None):
        if axis is None:
            return min(self.data)
        else:
            res = self._create_smaller(axis)
            n_el = len(self.data) // self.dimensions[axis]
            res.data = [max(self.data)] * n_el
            dims = []
            for i in range(len(self.dimensions)):
                dims.append(self.dimensions[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                i.pop(axis)
                if self[index] < res[tuple(i)]:
                    res[tuple(i)] = self[index]
            return res

    def max(self, axis=None):
        if axis is None:
            return max(self.data)
        else:
            res = self._create_smaller(axis)
            n_el = len(self.data) // self.dimensions[axis]
            res.data = [min(self.data)] * n_el
            dims = []
            for i in range(len(self.dimensions)):
                dims.append(self.dimensions[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                i.pop(axis)
                if self[index] > res[tuple(i)]:
                    res[tuple(i)] = self[index]
            return res

    def argmax(self, axis=None):
        max_val = max(self.data)
        if axis is None:
            return self.data.index(max_val)
        else:
            res = self._create_smaller(axis)
            n_el = len(self.data) // self.dimensions[axis]
            res.data = [0] * n_el
            dims = []
            for i in range(len(self.dimensions)):
                dims.append(self.dimensions[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                k = i.pop(axis)
                j = copy.deepcopy(i)
                j.insert(axis, res[tuple(i)])
                if self[index] > self[tuple(j)]:
                    res[tuple(i)] = k
            return res

    def argmin(self, axis=None):
        min_val = min(self.data)
        if axis is None:
            return self.data.index(min_val)
        else:
            res = self._create_smaller(axis)
            n_el = len(self.data) // self.dimensions[axis]
            res.data = [0] * n_el
            dims = []
            for i in range(len(self.dimensions)):
                dims.append(self.dimensions[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                k = i.pop(axis)
                j = copy.deepcopy(i)
                j.insert(axis, res[tuple(i)])
                if self[index] < self[tuple(j)]:
                    res[tuple(i)] = k
            return res

    def swapaxes(self, first, second):
        if first < 0 or first >= len(self.dimensions) or second < 0 or second >= len(self.dimensions):
            raise ValueError
        res = Tensor()
        res.dimensions = copy.deepcopy(self.dimensions)
        res.data = self.data
        res.dim_offset = copy.deepcopy(self.dim_offset)
        v = res.dimensions[first]
        res.dimensions[first] = res.dimensions[second]
        res.dimensions[second] = v
        v = res.dim_offset[first]
        res.dim_offset[first] = res.dim_offset[second]
        res.dim_offset[second] = v
        return res

    def transpose(self, *axis):
        res = Tensor()
        res.data = self.data
        if axis is None:
            res.dimensions = copy.deepcopy(self.dimensions)
            res.dim_offset = copy.deepcopy(self.dim_offset)
            for i in range(len(res.dimensions) // 2):
                v = res.dimensions[i]
                res.dimensions[i] = res.dimensions[len(res.dimensions) - 1 - i]
                res.dimensions[len(res.dimensions) - 1 - i] = v
                v = res.dim_offset[i]
                res.dim_offset[i] = res.dim_offset[len(res.dimensions) - 1 - i]
                res.dim_offset[len(res.dimensions) - 1 - i] = v
        else:
            if not isinstance(axis, tuple):
                raise ValueError
            if len(axis) != len(self.dimensions):
                raise ValueError
            for i, new_i in enumerate(axis):
                res.dimensions[i] = copy.copy(self.dimensions[new_i])
                res.dim_offset[i] = copy.copy(self.dim_offset[new_i])
        return res

    def __matmul__(self, other):
        if len(self.dimensions) == len(other.dimensions) == 1:
            if len(self.dimensions[0]) == len(other.dimensions[0]):
                res = 1
                for i in range(self.dimensions[0]):
                    res *= self.data[i] * other.data[i]
                return res
            else:
                raise ValueError
        if len(self.dimensions) == len(other.dimensions) == 2:
            if self.dimensions[1] == other.dimensions[0]:
                res = Tensor()
                m = self.dimensions[0]
                k = other.dimensions[1]
                res.dimensions[0] = m
                res.dimensions[1] = k
                res.dim_offset = {}
                res._calculate_offsets()
                res.data = [0] * (m * k)
                for i, j in [(x, y) for x in range(m) for y in range(k)]:
                    for p in range(self.dimensions[1]):
                        res[i, j] += self[i, p] * other[p, j]
                return res
            else:
                raise ValueError
        if len(self.dimensions) == 1 and len(other.dimensions) == 2:
            if self.dimensions[0] == other.dimensions[0]:
                res = Tensor()
                res.dimensions[0] = other.dimensions[1]
                res.data = [0] * other.dimensions[1]
                for i, j in [(x, y) for x in range(1) for y in range(other.dimensions[1])]:
                    for p in range(other.dimensions[0]):
                        res.data[j] += self.data[p] * other[p, j]
                return res
            else:
                raise ValueError
        if len(self.dimensions) == 2 and len(other.dimensions) == 1:
            if self.dimensions[1] == other.dimensions[0]:
                res = Tensor()
                res.dimensions[0] = self.dimensions[0]
                res.data = [0] * self.dimensions[0]
                for i, j in [(x, y) for x in range(self.dimensions[0]) for y in range(1)]:
                    for p in range(other.dimensions[0]):
                        res.data[i] += self[i, p] * other.data[p]
                return res
            else:
                raise ValueError
