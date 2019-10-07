#!/usr/bin/env python
# coding: utf-8


import copy
from itertools import product
import numpy as np


class Tensor:
    def __init__(self, init_matrix_representation=None):
        self.dim = {}
        self.data = []
        self.size_offset = {}
        if init_matrix_representation is not None:
            if not isinstance(init_matrix_representation, list):
                raise ValueError
            self._roll(init_matrix_representation, 0)
            self._calculate_offsets()

    def _calculate_offsets(self):
        self.size_offset[len(self.dim) - 1] = 1
        for i in range(len(self.dim) - 2, -1, -1):
            self.size_offset[i] = self.size_offset[i + 1] * self.dim[i + 1]

    def from_tensor(self):
        r = Tensor()
        r.dim = copy.deepcopy(self.dim)
        r.size_offset = copy.deepcopy(self.size_offset)
        r.data = copy.deepcopy(self.data)
        return r

    def _roll(self, obj, dim):
        if dim in self.dim:
            if self.dim[dim] != len(obj):
                raise ValueError
        else:
            self.dim[dim] = len(obj)
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
        if isinstance(key, tuple) and len(key) != len(self.dim):
            raise IndexError
        if isinstance(key, int):
            if 0 <= key < len(self.data):
                return self.data[key]
            else:
                raise IndexError
        for i, ind in enumerate(key):
            if ind < 0 or ind >= self.dim[i]:
                raise IndexError
        index = 0
        for i, ind in enumerate(key):
            index += ind * self.size_offset[i]
        return self.data[index]

    def __setitem__(self, key, value):
        if not isinstance(key, tuple):
            raise IndexError
        if not isinstance(value, (int, float, np.int, np.float, np.int64)):
            raise ValueError
        if len(key) != len(self.dim):
            raise IndexError
        for i, ind in enumerate(key):
            if ind < 0 or ind >= self.dim[i]:
                raise IndexError
        index = 0
        for i, ind in enumerate(key[:len(key):]):
            index += ind * self.size_offset[i]
        self.data[index] = value

    def __add__(self, other):
        output_ = self.from_tensor()
        if isinstance(other, Tensor):
            if self.dim == other.dim:
                for i, val in enumerate(self.data):
                    output_.data[i] = val + other.data[i]
            else:
                raise ValueError
        elif isinstance(other, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                output_.data[i] = val + other
        return output_

    def __radd__(self, other):
        output_ = self.from_tensor()
        if isinstance(other, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                output_.data[i] = val + other
        return output_

    def __sub__(self, other):
        output_ = self.from_tensor()
        if isinstance(other, Tensor):
            if self.dim == other.dim:
                for i, val in enumerate(self.data):
                    output_.data[i] = val - other.data[i]
            else:
                raise ValueError
        elif isinstance(other, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                output_.data[i] = val - other
        return output_

    def __mul__(self, other):
        output_ = self.from_tensor()
        if isinstance(other, Tensor):
            if self.dim == other.dim:
                for i, val in enumerate(self.data):
                    output_.data[i] = val * other.data[i]
            else:
                raise ValueError
        elif isinstance(other, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                output_.data[i] = val * other
        return output_

    def __truediv__(self, other):
        output_ = self.from_tensor()
        if isinstance(other, (int, float, np.int, np.float, np.int64)):
            if other == 0:
                raise ZeroDivisionError
            for i, val in enumerate(self.data):
                output_.data[i] = val / other
        return output_

    def __pow__(self, power, modulo=None):
        output_ = self.from_tensor()
        if isinstance(power, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                output_.data[i] = val ** power
        return output_

    def _create_smaller(self, axis):
        output_ = Tensor()
        for k in self.dim:
            if k > axis:
                output_.dim[k - 1] = self.dim[k]
            elif k == axis:
                continue
            else:
                output_.dim[k] = self.dim[k]
        output_._calculate_offsets()
        return output_

    def sum(self, axis=None):
        if axis is None:
            output_ = 0
            for i in self.data:
                output_ += i
            return output_
        else:
            output_ = self._create_smaller(axis)
            n_el = len(self.data) // self.dim[axis]
            output_.data = [0] * n_el
            dims = []
            for i in range(len(self.dim)):
                dims.append(self.dim[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                i.pop(axis)
                output_[tuple(i)] += self[index]
            return output_

    def to_list(self):
        if len(self.dim) == 1:
            return self.data
        return self._get_as_list(self.data, len(self.dim) - 1)

    def _get_as_list(self, arr, dim):
        if dim == (len(self.dim) - 1):
            dims = []
            v = []
            for i in range(len(self.dim)):
                dims.append(self.dim[i])
            for index in product(*[range(k) for k in dims]):
                v.append(self[index])
            arr = v
        if dim > 0:
            l1 = list()
            l2 = list()
            n = self.dim[dim]
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
            r = 0
            for i in self.data:
                r += i
            return r / len(self.data)
        else:
            t = self.sum(axis)
            for i, it in enumerate(t.data):
                t.data[i] = it / self.dim[axis]
            return t

    def min(self, axis=None):
        if axis is None:
            return min(self.data)
        else:
            output_ = self._create_smaller(axis)
            n_el = len(self.data) // self.dim[axis]
            output_.data = [max(self.data)] * n_el
            dims = []
            for i in range(len(self.dim)):
                dims.append(self.dim[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                i.pop(axis)
                if self[index] < output_[tuple(i)]:
                    output_[tuple(i)] = self[index]
            return output_

    def max(self, axis=None):
        if axis is None:
            return max(self.data)
        else:
            output_ = self._create_smaller(axis)
            n_el = len(self.data) // self.dim[axis]
            output_.data = [min(self.data)] * n_el
            dims = []
            for i in range(len(self.dim)):
                dims.append(self.dim[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                i.pop(axis)
                if self[index] > output_[tuple(i)]:
                    output_[tuple(i)] = self[index]
            return output_

    def argmax(self, axis=None):
        max_val = max(self.data)
        if axis is None:
            return self.data.index(max_val)
        else:
            output_ = self._create_smaller(axis)
            n_el = len(self.data) // self.dim[axis]
            output_.data = [0] * n_el
            dims = []
            for i in range(len(self.dim)):
                dims.append(self.dim[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                k = i.pop(axis)
                j = copy.deepcopy(i)
                j.insert(axis, output_[tuple(i)])
                if self[index] > self[tuple(j)]:
                    output_[tuple(i)] = k
            return output_

    def argmin(self, axis=None):
        min_val = min(self.data)
        if axis is None:
            return self.data.index(min_val)
        else:
            output_ = self._create_smaller(axis)
            n_el = len(self.data) // self.dim[axis]
            output_.data = [0] * n_el
            dims = []
            for i in range(len(self.dim)):
                dims.append(self.dim[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                k = i.pop(axis)
                j = copy.deepcopy(i)
                j.insert(axis, output_[tuple(i)])
                if self[index] < self[tuple(j)]:
                    output_[tuple(i)] = k
            return output_

    def swapaxes(self, first, second):
        if first < 0 or first >= len(self.dim) or second < 0 or second >= len(self.dim):
            raise ValueError
        output_ = Tensor()
        output_.dim = copy.deepcopy(self.dim)
        output_.data = self.data
        output_.size_offset = copy.deepcopy(self.size_offset)
        v = output_.dim[first]
        output_.dim[first] = output_.dim[second]
        output_.dim[second] = v
        v = output_.size_offset[first]
        output_.size_offset[first] = output_.size_offset[second]
        output_.size_offset[second] = v
        return output_

    def transpose(self, *axis):
        output_ = Tensor()
        output_.data = self.data
        if axis is None:
            output_.dim = copy.deepcopy(self.dim)
            output_.size_offset = copy.deepcopy(self.size_offset)
            for i in range(len(output_.dim) // 2):
                v = output_.dim[i]
                output_.dim[i] = output_.dim[len(output_.dim) - 1 - i]
                output_.dim[len(output_.dim) - 1 - i] = v
                v = output_.size_offset[i]
                output_.size_offset[i] = output_.size_offset[len(output_.dim) - 1 - i]
                output_.size_offset[len(output_.dim) - 1 - i] = v
        else:
            if not isinstance(axis, tuple):
                raise ValueError
            if len(axis) != len(self.dim):
                raise ValueError
            for i, new_i in enumerate(axis):
                output_.dim[i] = copy.copy(self.dim[new_i])
                output_.size_offset[i] = copy.copy(self.size_offset[new_i])
        return output_

    def __matmul__(self, other):
        if len(self.dim) == len(other.dim) == 1:
            if len(self.dim[0]) == len(other.dim[0]):
                output_ = 1
                for i in range(self.dim[0]):
                    output_ *= self.data[i] * other.data[i]
                return output_
            else:
                raise ValueError
        if len(self.dim) == len(other.dim) == 2:
            if self.dim[1] == other.dim[0]:
                output_ = Tensor()
                m = self.dim[0]
                k = other.dim[1]
                output_.dim[0] = m
                output_.dim[1] = k
                output_.size_offset = {}
                output_._calculate_offsets()
                output_.data = [0] * (m * k)
                for i, j in [(x, y) for x in range(m) for y in range(k)]:
                    for p in range(self.dim[1]):
                        output_[i, j] += self[i, p] * other[p, j]
                return output_
            else:
                raise ValueError
        if len(self.dim) == 1 and len(other.dim) == 2:
            if self.dim[0] == other.dim[0]:
                output_ = Tensor()
                output_.dim[0] = other.dim[1]
                output_.data = [0] * other.dim[1]
                for i, j in [(x, y) for x in range(1) for y in range(other.dim[1])]:
                    for p in range(other.dim[0]):
                        output_.data[j] += self.data[p] * other[p, j]
                return output_
            else:
                raise ValueError
        if len(self.dim) == 2 and len(other.dim) == 1:
            if self.dim[1] == other.dim[0]:
                output_ = Tensor()
                output_.dim[0] = self.dim[0]
                output_.data = [0] * self.dim[0]
                for i, j in [(x, y) for x in range(self.dim[0]) for y in range(1)]:
                    for p in range(other.dim[0]):
                        output_.data[i] += self[i, p] * other.data[p]
                return output_
            else:
                raise ValueError
