#!/usr/bin/env python
# coding: utf-8
from copy import deepcopy
import itertools as it
import numpy as np


class Tensor:
    def __init__(self, init_matrix_representation):
        self.mat = init_matrix_representation
        self._shape = self._calculate_shape()

    def _calculate_shape(self):
        copy_arr = deepcopy(self.mat)
        shape = [len(copy_arr)]
        while isinstance(copy_arr[0], list):
            length = len(copy_arr[0])
            for ar in copy_arr:
                is_all_norm = True
                if not isinstance(ar, list) or len(ar) != length:
                    is_all_norm = False
            if is_all_norm:
                shape.append(len(ar))
                copy_arr = copy_arr[0]
            else:
                return tuple(shape)
        return tuple(shape)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.mat[key]
        i = 0
        elem = self.mat[key[i]]
        while i < len(key) - 1:
            i += 1
            elem = elem[key[i]]
        return elem

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.mat[key] = value
            return
        i = 0
        elem = self.mat[key[i]]
        while i < len(key) - 2:
            i += 1
            elem = elem[key[i]]
        i += 1
        elem[key[i]] = value

    def _make_operation(self, operation, other):
        if isinstance(other, Tensor) and self._shape != other._shape:
            raise ValueError

        result = deepcopy(self)
        index = [0] * (len(result._shape))

        for index in it.product(*[range(k) for k in self._shape]):
            if isinstance(other, Tensor):
                if operation == '+':
                    result[index] += other[index]
                elif operation == '-':
                    result[index] -= other[index]
                elif operation == '*':
                    result[index] *= other[index]
                elif operation == '/':
                    result[index] /= other[index]
            else:
                if operation == '+':
                    result[index] += other
                elif operation == '-':
                    result[index] -= other
                elif operation == '*':
                    result[index] *= other
                elif operation == '/':
                    result[index] /= other
        return result

    def __add__(self, other):
        return self._make_operation('+', other)

    def __radd__(self, other):
        return self._make_operation('+', other)

    def __sub__(self, other):
        return self._make_operation('-', other)

    def __mul__(self, other):
        return self._make_operation('*', other)

    def __truediv__(self, other):
        return self._make_operation('/', other)

    def __pow__(self, pow):
        result = deepcopy(self)
        for _ in range(pow - 1):
            result = result._make_operation('*', self)
        return result

    def __matmul__(self, other):
        if self._shape[-1] != other._shape[0]:
            raise ValueError

        length1 = len(self._shape)
        length2 = len(other._shape)
        if length1 == 1 and length2 == 1:
            result = Tensor([0] * self._shape[0])
            for i in range(result._shape[0]):
                result.mat[i] = other.mat[i] * self.mat[i]

        elif length1 == 2 and length2 == 2:
            result = Tensor([[0] * other._shape[1]
                             for _ in range(self._shape[0])])
            for i in range(self._shape[0]):
                for j in range(other._shape[1]):
                    for r in range(self._shape[1]):
                        result[i, j] += self[i, r] * other[r, j]

        elif length1 == 2 and length2 == 1:
            result = Tensor([0 for _ in range(self._shape[0])])
            for i in range(self._shape[0]):
                for r in range(self._shape[1]):
                    result[i] += self[i, r] * other[r]

        elif length1 == 1 and length2 == 2:
            result = Tensor([0 for _ in range(other._shape[1])])
            for i in range(other._shape[1]):
                for r in range(self._shape[0]):
                    result[i] += self[r] * other[r, i]

        return result

    def __str__(self):
        s = ''
        index = [0] * (len(self._shape))
        for index in it.product(*[range(k) for k in self._shape]):
            s += str(index) + ' ' + str(self[index]) + ' '
            s += '\n'

        return s

    def _begin_staistic(self, axis):
        if len(self._shape) <= 2:
            raise ValueError

        arr = 0
        for i in range(len(self._shape) - 1, -1, -1):
            if i == axis:
                continue
            arr = [deepcopy(arr) for _ in range(self._shape[i])]

        result = Tensor(arr)

        return result

    def sum(self, axis=None):
        if axis is None:
            result = 0
            for index in it.product(*[range(k) for k in self._shape]):
                result += self[index]
            return result

        result = self._begin_staistic(axis)

        for index in it.product(*[range(k) for k in result._shape]):
            for i in range(self._shape[axis]):
                index = list(index)
                ind = index[0:axis] + [i] + index[axis:]
                result[index] += self[ind]

        return result

    def mean(self, axis=None):
        if axis is None:
            result = 0
            n = 0
            for index in it.product(*[range(k) for k in self._shape]):
                result += self[index]
                n += 1
            return result / n

        result = self._begin_staistic(axis)

        for index in it.product(*[range(k) for k in result._shape]):
            n = 0
            for i in range(self._shape[axis]):
                index = list(index)
                ind = index[0:axis] + [i] + index[axis:]
                result[index] += self[ind]
                n += 1
            result[index] /= n

        return result

    def min(self, axis=None):
        if axis is None:
            result = self[[0 for _ in range(len(self._shape))]]
            for index in it.product(*[range(k) for k in self._shape]):
                if result > self[index]:
                    result = self[index]
            return result

        result = self._begin_staistic(axis)

        for index in it.product(*[range(k) for k in result._shape]):
            zero_ind = list(index[0:axis]) + [0] + list(index[axis:])
            result[index] = self[zero_ind]
            for i in range(1, self._shape[axis]):
                index = list(index)
                ind = index[0:axis] + [i] + index[axis:]
                if self[ind] < result[index]:
                    result[index] = self[ind]

        return result

    def max(self, axis=None):
        if axis is None:
            result = self[[0 for _ in range(len(self._shape))]]
            for index in it.product(*[range(k) for k in self._shape]):
                if result < self[index]:
                    result = self[index]
            return result

        result = self._begin_staistic(axis)

        for index in it.product(*[range(k) for k in result._shape]):
            zero_ind = list(index[0:axis]) + [0] + list(index[axis:])
            result[index] = self[zero_ind]
            for i in range(1, self._shape[axis]):
                index = list(index)
                ind = index[0:axis] + [i] + index[axis:]
                if self[ind] > result[index]:
                    result[index] = self[ind]
        return result

    def argmax(self, axis=None):
        if axis is None:
            maximum = self[[0 for _ in range(len(self._shape))]]
            n = 0
            result = n
            for index in it.product(*[range(k) for k in self._shape]):
                if self[index] > maximum:
                    maximum = self[index]
                    result = n
                n += 1
            return result

        result = self._begin_staistic(axis)

        for index in it.product(*[range(k) for k in result._shape]):
            zero_ind = list(index[0:axis]) + [0] + list(index[axis:])
            maximum = self[zero_ind]
            result[index] = 0
            for i in range(1, self._shape[axis]):
                index = list(index)
                ind = index[0:axis] + [i] + index[axis:]
                if self[ind] > maximum:
                    result[index] = i
                    maximum = self[ind]

        return result

    def argmin(self, axis=None):
        if axis is None:
            minimum = self[[0 for _ in range(len(self._shape))]]
            n = 0
            result = n
            for index in it.product(*[range(k) for k in self._shape]):
                if self[index] < minimum:
                    minimum = self[index]
                    result = n
                n += 1
            return result

        result = self._begin_staistic(axis)

        for index in it.product(*[range(k) for k in result._shape]):
            zero_ind = list(index[0:axis]) + [0] + list(index[axis:])
            minimum = self[zero_ind]
            result[index] = 0
            for i in range(1, self._shape[axis]):
                index = list(index)
                ind = index[0:axis] + [i] + index[axis:]
                if self[ind] < minimum:
                    result[index] = i
                    minimum = self[ind]

        return result

    def transpose(self, *args):
        if args:
            axis = args
        else:
            axis = None

        arr = 0

        if axis is None:
            for i in range(len(self._shape)):
                arr = [deepcopy(arr) for _ in range(self._shape[i])]

            result = Tensor(arr)

            for index in it.product(*[range(k) for k in result._shape]):
                result[index] = self[index[::-1]]

        else:
            for i in range(len(axis) - 1, -1, -1):
                arr = [deepcopy(arr) for _ in range(self._shape[axis[i]])]

            result = Tensor(arr)
            for index in it.product(*[range(k) for k in self._shape]):
                new_index = [index[i] for i in axis]
                result[new_index] = self[index]

        return result

    def swapaxes(self, axis1, axis2):
        new_shape = [i for i in range(len(self._shape))]

        new_shape[axis1], new_shape[axis2] = new_shape[axis2], new_shape[axis1]

        return self.transpose(*new_shape)
