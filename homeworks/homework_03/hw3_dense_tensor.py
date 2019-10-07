#!/usr/bin/env python
# coding: utf-8
import copy
from itertools import product
import numpy as numpy


class Tensor:

    def __init__(self, init_matrix_represultentation=None):
        self.dimensions = {}
        self.data = []
        self.dim_offset = {}
        if init_matrix_represultentation is not None:
            if not isinstance(init_matrix_represultentation, list):
                raise ValueError
            self._roll(init_matrix_represultentation, 0)
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
        if not isinstance(value, (int, float, numpy.int, numpy.float, numpy.int64)):
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
        result = self.from_tensor()
        if isinstance(other, Tensor):
            if self.dimensions == other.dimensions:
                for i, val in enumerate(self.data):
                    result.data[i] = val + other.data[i]
            else:
                raise ValueError
        elif isinstance(other, (int, float, numpy.int, numpy.float, numpy.int64)):
            for i, val in enumerate(self.data):
                result.data[i] = val + other
        return result

    def __radd__(self, other):
        result = self.from_tensor()
        if isinstance(other, (int, float, numpy.int, numpy.float, numpy.int64)):
            for i, val in enumerate(self.data):
                result.data[i] = val + other
        return result

    def __sub__(self, other):
        result = self.from_tensor()
        if isinstance(other, Tensor):
            if self.dimensions == other.dimensions:
                for i, val in enumerate(self.data):
                    result.data[i] = val - other.data[i]
            else:
                raise ValueError
        elif isinstance(other, (int, float, numpy.int, numpy.float, numpy.int64)):
            for i, val in enumerate(self.data):
                result.data[i] = val - other
        return result

    def __mul__(self, other):
        result = self.from_tensor()
        if isinstance(other, Tensor):
            if self.dimensions == other.dimensions:
                for i, val in enumerate(self.data):
                    result.data[i] = val * other.data[i]
            else:
                raise ValueError
        elif isinstance(other, (int, float, numpy.int, numpy.float, numpy.int64)):
            for i, val in enumerate(self.data):
                result.data[i] = val * other
        return result

    def __truediv__(self, other):
        result = self.from_tensor()
        if isinstance(other, (int, float, numpy.int, numpy.float, numpy.int64)):
            if other == 0:
                raise ZeroDivisionError
            for i, val in enumerate(self.data):
                result.data[i] = val / other
        return result

    def __pow__(self, power, modulo=None):
        result = self.from_tensor()
        if isinstance(power, (int, float, numpy.int, numpy.float, numpy.int64)):
            for i, val in enumerate(self.data):
                result.data[i] = val ** power
        return result

    def _create_smaller(self, axis):
        result = Tensor()
        for k in self.dimensions:
            if k > axis:
                result.dimensions[k - 1] = self.dimensions[k]
            elif k == axis:
                continue
            else:
                result.dimensions[k] = self.dimensions[k]
        result._calculate_offsets()
        return result

    def sum(self, axis=None):
        if axis is None:
            result = 0
            for i in self.data:
                result += i
            return result
        else:
            result = self._create_smaller(axis)
            n_el = len(self.data) // self.dimensions[axis]
            result.data = [0] * n_el
            dims = []
            for i in range(len(self.dimensions)):
                dims.append(self.dimensions[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                i.pop(axis)
                result[tuple(i)] += self[index]
            return result

    def to_list(self):
        if len(self.dimensions) == 1:
            return self.data
        return self._get_as_list(self.data, len(self.dimensions) - 1)

    def _get_as_list(self, arr, dim):
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
            result = self._create_smaller(axis)
            n_el = len(self.data) // self.dimensions[axis]
            result.data = [max(self.data)] * n_el
            dims = []
            for i in range(len(self.dimensions)):
                dims.append(self.dimensions[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                i.pop(axis)
                if self[index] < result[tuple(i)]:
                    result[tuple(i)] = self[index]
            return result

    def max(self, axis=None):
        if axis is None:
            return max(self.data)
        else:
            result = self._create_smaller(axis)
            n_el = len(self.data) // self.dimensions[axis]
            result.data = [min(self.data)] * n_el
            dims = []
            for i in range(len(self.dimensions)):
                dims.append(self.dimensions[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                i.pop(axis)
                if self[index] > result[tuple(i)]:
                    result[tuple(i)] = self[index]
            return result

    def argmax(self, axis=None):
        max_val = max(self.data)
        if axis is None:
            return self.data.index(max_val)
        else:
            result = self._create_smaller(axis)
            n_el = len(self.data) // self.dimensions[axis]
            result.data = [0] * n_el
            dims = []
            for i in range(len(self.dimensions)):
                dims.append(self.dimensions[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                k = i.pop(axis)
                j = copy.deepcopy(i)
                j.insert(axis, result[tuple(i)])
                if self[index] > self[tuple(j)]:
                    result[tuple(i)] = k
            return result

    def argmin(self, axis=None):
        min_val = min(self.data)
        if axis is None:
            return self.data.index(min_val)
        else:
            result = self._create_smaller(axis)
            n_el = len(self.data) // self.dimensions[axis]
            result.data = [0] * n_el
            dims = []
            for i in range(len(self.dimensions)):
                dims.append(self.dimensions[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                k = i.pop(axis)
                j = copy.deepcopy(i)
                j.insert(axis, result[tuple(i)])
                if self[index] < self[tuple(j)]:
                    result[tuple(i)] = k
            return result

    def swapaxes(self, first, second):
        if first < 0 or first >= len(self.dimensions) or second < 0 or second >= len(self.dimensions):
            raise ValueError
        result = Tensor()
        result.dimensions = copy.deepcopy(self.dimensions)
        result.data = self.data
        result.dim_offset = copy.deepcopy(self.dim_offset)
        v = result.dimensions[first]
        result.dimensions[first] = result.dimensions[second]
        result.dimensions[second] = v
        v = result.dim_offset[first]
        result.dim_offset[first] = result.dim_offset[second]
        result.dim_offset[second] = v
        return result

    def transpose(self, *axis):
        result = Tensor()
        result.data = self.data
        if axis is None:
            result.dimensions = copy.deepcopy(self.dimensions)
            result.dim_offset = copy.deepcopy(self.dim_offset)
            for i in range(len(result.dimensions) // 2):
                v = result.dimensions[i]
                result.dimensions[i] = result.dimensions[len(result.dimensions) - 1 - i]
                result.dimensions[len(result.dimensions) - 1 - i] = v
                v = result.dim_offset[i]
                result.dim_offset[i] = result.dim_offset[len(result.dimensions) - 1 - i]
                result.dim_offset[len(result.dimensions) - 1 - i] = v
        else:
            if not isinstance(axis, tuple):
                raise ValueError
            if len(axis) != len(self.dimensions):
                raise ValueError
            for i, new_i in enumerate(axis):
                result.dimensions[i] = copy.copy(self.dimensions[new_i])
                result.dim_offset[i] = copy.copy(self.dim_offset[new_i])
        return result

    def __matmul__(self, other):
        if len(self.dimensions) == len(other.dimensions) == 1:
            if len(self.dimensions[0]) == len(other.dimensions[0]):
                result = 1
                for i in range(self.dimensions[0]):
                    result *= self.data[i] * other.data[i]
                return result
            else:
                raise ValueError
        if len(self.dimensions) == len(other.dimensions) == 2:
            if self.dimensions[1] == other.dimensions[0]:
                result = Tensor()
                m = self.dimensions[0]
                k = other.dimensions[1]
                result.dimensions[0] = m
                result.dimensions[1] = k
                result.dim_offset = {}
                result._calculate_offsets()
                result.data = [0] * (m * k)
                for i, j in [(x, y) for x in range(m) for y in range(k)]:
                    for p in range(self.dimensions[1]):
                        result[i, j] += self[i, p] * other[p, j]
                return result
            else:
                raise ValueError
        if len(self.dimensions) == 1 and len(other.dimensions) == 2:
            if self.dimensions[0] == other.dimensions[0]:
                result = Tensor()
                result.dimensions[0] = other.dimensions[1]
                result.data = [0] * other.dimensions[1]
                for i, j in [(x, y) for x in range(1) for y in range(other.dimensions[1])]:
                    for p in range(other.dimensions[0]):
                        result.data[j] += self.data[p] * other[p, j]
                return result
            else:
                raise ValueError
        if len(self.dimensions) == 2 and len(other.dimensions) == 1:
            if self.dimensions[1] == other.dimensions[0]:
                result = Tensor()
                result.dimensions[0] = self.dimensions[0]
                result.data = [0] * self.dimensions[0]
                for i, j in [(x, y) for x in range(self.dimensions[0]) for y in range(1)]:
                    for p in range(other.dimensions[0]):
                        result.data[i] += self[i, p] * other.data[p]
                return result
            else:
                raise ValueError
