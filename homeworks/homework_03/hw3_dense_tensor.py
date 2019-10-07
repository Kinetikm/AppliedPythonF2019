#!/usr/bin/env python
# coding: utf-8

from copy import deepcopy
import numpy as np
import itertools


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
        self._matrix = []
        self._dim = []
        self.get_dimension(init_matrix_representation)
        self.make_matrix(init_matrix_representation)
        self._axis = [1]
        self.get_axis()

    def get_axis(self):
        mul = 1
        for i in range(len(self._dim) - 1, 0, -1):
            mul *= self._dim[i]
            self._axis.append(mul)
        self._axis.reverse()

    def get_dimension(self, lst):
        if isinstance(lst, list):
            self._dim.append(len(lst))
            self.get_dimension(lst[0])

    def make_matrix(self, init_matrix):
        if isinstance(init_matrix[0], list):
            for lst in init_matrix:
                self.make_matrix(lst)
        else:
            for item in init_matrix:
                self._matrix.append(item)

    def __getitem__(self, tpl):
        ind = 0
        if not isinstance(tpl, tuple):
            tpl = (tpl,)
        for i in range(len(tpl)):
            ind += tpl[i] * self._axis[i]
        return self._matrix[ind]

    def __setitem__(self, tpl, value):
        ind = 0
        if not isinstance(tpl, tuple):
            tpl = (tpl,)
        for i in range(len(tpl)):
            ind += tpl[i] * self._axis[i]
        self._matrix[ind] = value

    def __add__(self, other):
        res = deepcopy(self)
        if isinstance(other, Tensor):
            if self._dim == other._dim:
                for i in range(len(res._matrix)):
                    res._matrix[i] += other._matrix[i]
                return res
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            for i in range(len(res._matrix)):
                res._matrix[i] += other
            return res
        else:
            raise ValueError

    def __radd__(self, other):
        res = deepcopy(self)
        return res.__add__(other)

    def __sub__(self, other):
        res = deepcopy(self)
        if isinstance(other, Tensor):
            if self._dim == other._dim:
                for i in range(len(res._matrix)):
                    res._matrix[i] -= other._matrix[i]
                return res
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            for i in range(len(res._matrix)):
                res._matrix[i] -= other
            return res
        else:
            raise ValueError

    def __mul__(self, other):
        res = deepcopy(self)
        if isinstance(other, Tensor):
            if self._dim == other._dim:
                for i in range(len(res._matrix)):
                    res._matrix[i] *= other._matrix[i]
                return res
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            for i in range(len(res._matrix)):
                res._matrix[i] *= other
            return res
        else:
            raise ValueError

    def __rmul__(self, other):
        res = deepcopy(self)
        return res.__add__(other)

    def __truediv__(self, other):
        res = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float):
            if other != 0:
                for i in range(len(res._matrix)):
                    res._matrix[i] /= other
                return res
            else:
                raise ZeroDivisionError
        else:
            raise ValueError

    def __pow__(self, other):
        res = deepcopy(self)
        if isinstance(other, Tensor):
            if self._dim == other._dim:
                for i in range(len(res._matrix)):
                    res._matrix[i] **= other._matrix[i]
                return res
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            for i in range(len(res._matrix)):
                res._matrix[i] **= other
            return res
        else:
            raise ValueError

    def transpose(self, *tpl):
        t = deepcopy(self)
        if isinstance(tpl[0], list):
            tpl = tpl[0]
        t._axis = []
        if not tpl:
            tpl = list(range(len(self._axis)))
            tpl.reverse()
        for i in tpl:
            t._axis.append(self._axis[i])
        return t

    def swapaxes(self, axis1, axis2):
        res = deepcopy(self)
        tpl = list(range(len(self._axis)))
        tpl[axis1] = axis2
        tpl[axis2] = axis1
        return res.transpose(tpl)

    def sum(self, axis=None):
        result = deepcopy(self)
        tpl = [0] * len(self._axis)
        res = [0]
        if isinstance(axis, int):
            while tpl[axis] < self._dim[axis]:
                ind = 0
                for i in range(len(tpl)):
                    ind += tpl[i] * self._axis[i]
                res[-1] += self._matrix[ind]
                tpl[axis] += 1
                if tpl[axis] >= self._dim[axis]:
                    res.append(0)
                    if sum(tpl) - 1 < sum(self._dim) - len(self._dim):
                        tpl[axis] = 0
                        i = len(tpl) - 1
                        while i == axis and i > 0:
                            i -= 1
                        if tpl[i] + 1 < self._dim[i]:
                            tpl[i] += 1
                        else:
                            tpl[i] = 0
                            i -= 1
                            if i == axis:
                                i -= 1
                            while i > 0 and tpl[i] + 1 >= self._dim[i]:
                                if i == axis:
                                    i -= 1
                                    continue
                                tpl[i] = 0
                                i -= 1
                            tpl[i] += 1
                    else:
                        result._dim = []
                        result._axis = [1]
                        for i in range(len(self._dim)):
                            if i != axis:
                                result._dim.append(self._dim[i])
                        result.get_axis()
                        result._matrix = res[:len(res) - 1]
                        return result
        else:
            return sum(self._matrix)

    def mean(self, axis=None):
        result = deepcopy(self)
        tpl = [0] * len(self._axis)
        res = [0]
        k = 0
        if isinstance(axis, int):
            while tpl[axis] < self._dim[axis]:
                ind = 0
                for i in range(len(tpl)):
                    ind += tpl[i] * self._axis[i]
                res[-1] += self._matrix[ind]
                k += 1
                tpl[axis] += 1
                if tpl[axis] >= self._dim[axis]:
                    res[-1] /= k
                    k = 0
                    res.append(0)
                    tpl[axis] = 0
                    m = sum(tpl) + self._dim[axis] - 1
                    if m < sum(self._dim) - len(self._dim):
                        i = len(tpl) - 1
                        while i == axis and i > 0:
                            i -= 1
                        if tpl[i] + 1 < self._dim[i]:
                            tpl[i] += 1
                        else:
                            tpl[i] = 0
                            i -= 1
                            if i == axis:
                                i -= 1
                            while i > 0 and tpl[i] + 1 >= self._dim[i]:
                                if i == axis:
                                    i -= 1
                                    continue
                                tpl[i] = 0
                                i -= 1
                            tpl[i] += 1
                    else:
                        result._dim = []
                        result._axis = [1]
                        for i in range(len(self._dim)):
                            if i != axis:
                                result._dim.append(self._dim[i])
                        result.get_axis()
                        result._matrix = res[:len(res) - 1]
                        return result
        else:
            return sum(self._matrix) / len(self._matrix)

    def max(self, axis=None):
        result = deepcopy(self)
        res = [0]
        tpl = [0] * len(self._axis)
        if isinstance(axis, int):
            while tpl[axis] < self._dim[axis]:
                ind = 0
                for i in range(len(tpl)):
                    ind += tpl[i] * self._axis[i]
                res[-1] = max(res[-1], self._matrix[ind])
                tpl[axis] += 1
                if tpl[axis] >= self._dim[axis]:
                    res.append(0)
                    tpl[axis] = 0
                    m = sum(tpl) + self._dim[axis] - 1
                    if m < sum(self._dim) - len(self._dim):
                        i = len(tpl) - 1
                        while i == axis and i > 0:
                            i -= 1
                        if tpl[i] + 1 < self._dim[i]:
                            tpl[i] += 1
                        else:
                            tpl[i] = 0
                            i -= 1
                            if i == axis:
                                i -= 1
                            while i > 0 and tpl[i] + 1 >= self._dim[i]:
                                if i == axis:
                                    i -= 1
                                    continue
                                tpl[i] = 0
                                i -= 1
                            tpl[i] += 1
                    else:
                        result._dim = []
                        result._axis = [1]
                        for i in range(len(self._dim)):
                            if i != axis:
                                result._dim.append(self._dim[i])
                        result.get_axis()
                        result._matrix = res[:len(res) - 1]
                        return result
        else:
            return max(self._matrix)

    def min(self, axis=None):
        result = deepcopy(self)
        tpl = [0] * len(self._axis)
        res = [0]
        if isinstance(axis, int):
            while tpl[axis] < self._dim[axis]:
                ind = 0
                for i in range(len(tpl)):
                    ind += tpl[i] * self._axis[i]
                res[-1] = min(res[-1], self._matrix[ind])
                tpl[axis] += 1
                if tpl[axis] >= self._dim[axis]:
                    res.append(0)
                    tpl[axis] = 0
                    m = sum(tpl) + self._dim[axis] - 1
                    if m < sum(self._dim) - len(self._dim):
                        i = len(tpl) - 1
                        while i == axis and i > 0:
                            i -= 1
                        if tpl[i] + 1 < self._dim[i]:
                            tpl[i] += 1
                        else:
                            tpl[i] = 0
                            i -= 1
                            if i == axis:
                                i -= 1
                            while i > 0 and tpl[i] + 1 >= self._dim[i]:
                                if i == axis:
                                    i -= 1
                                    continue
                                tpl[i] = 0
                                i -= 1
                            tpl[i] += 1
                    else:
                        result._dim = []
                        result._axis = [1]
                        for i in range(len(self._dim)):
                            if i != axis:
                                result._dim.append(self._dim[i])
                        result.get_axis()
                        result._matrix = res[:len(res) - 1]
                        return result
        else:
            return min(self._matrix)

    def argmax(self, axis=None):
        result = deepcopy(self)
        tpl = [0] * len(self._axis)
        mx = None
        arg = [0]
        if isinstance(axis, int):
            while tpl[axis] < self._dim[axis]:
                ind = 0
                for i in range(len(tpl)):
                    ind += tpl[i] * self._axis[i]
                if not mx:
                    mx = self._matrix[ind]
                    arg[-1] = tpl[axis]
                elif self._matrix[ind] > mx:
                    mx = self._matrix[ind]
                    arg[-1] = tpl[axis]
                tpl[axis] += 1
                if tpl[axis] >= self._dim[axis]:
                    mx = None
                    arg.append(0)
                    tpl[axis] = 0
                    m = sum(tpl) + self._dim[axis] - 1
                    if m < sum(self._dim) - len(self._dim):
                        i = len(tpl) - 1
                        while i == axis and i > 0:
                            i -= 1
                        if tpl[i] + 1 < self._dim[i]:
                            tpl[i] += 1
                        else:
                            tpl[i] = 0
                            i -= 1
                            if i == axis:
                                i -= 1
                            while i > 0 and tpl[i] + 1 >= self._dim[i]:
                                if i == axis:
                                    i -= 1
                                    continue
                                tpl[i] = 0
                                i -= 1
                            tpl[i] += 1
                    else:
                        result._dim = []
                        result._axis = [1]
                        for i in range(len(self._dim)):
                            if i != axis:
                                result._dim.append(self._dim[i])
                        result.get_axis()
                        result._matrix = arg[:len(arg) - 1]
                        return result
        else:
            return self._matrix.index(max(self._matrix))

    def argmin(self, axis=None):
        result = deepcopy(self)
        tpl = [0] * len(self._axis)
        mn = None
        arg = [0]
        if isinstance(axis, int):
            while tpl[axis] < self._dim[axis]:
                ind = 0
                for i in range(len(tpl)):
                    ind += tpl[i] * self._axis[i]
                if not mn:
                    mn = self._matrix[ind]
                    arg[-1] = tpl[axis]
                elif self._matrix[ind] < mn:
                    mn = self._matrix[ind]
                    arg[-1] = tpl[axis]
                tpl[axis] += 1
                if tpl[axis] >= self._dim[axis]:
                    mn = None
                    arg.append(0)
                    tpl[axis] = 0
                    m = sum(tpl) + self._dim[axis] - 1
                    if m < sum(self._dim) - len(self._dim):
                        i = len(tpl) - 1
                        while i == axis and i > 0:
                            i -= 1
                        if tpl[i] + 1 < self._dim[i]:
                            tpl[i] += 1
                        else:
                            tpl[i] = 0
                            i -= 1
                            if i == axis:
                                i -= 1
                            while i > 0 and tpl[i] + 1 >= self._dim[i]:
                                if i == axis:
                                    i -= 1
                                    continue
                                tpl[i] = 0
                                i -= 1
                            tpl[i] += 1
                    else:
                        result._dim = []
                        result._axis = [1]
                        for i in range(len(self._dim)):
                            if i != axis:
                                result._dim.append(self._dim[i])
                        result.get_axis()
                        result._matrix = arg[:len(arg) - 1]
                        return result
        else:
            return self._matrix.index(min(self._matrix))

    def __matmul__(self, other):
        result = deepcopy(self)
        res = []
        result._axis = [1]
        if len(self._dim) == 1:
            if self._dim[0] == other._dim[0]:
                if len(other._dim) == 1:
                    result._dim = [1, 1]
                    sm = 0
                    for i in range(self._dim[0]):
                        a = self._matrix[self._axis[0] * i]
                        b = other._matrix[other._axis[0] * i]
                        sm += a * b
                    res.append(sm)
                    result.get_axis()
                    return res
                elif len(other._dim) == 2:
                    result._dim = [1, other._dim[1]]
                    for j in range(other._dim[1]):
                        sm = 0
                        for i in range(self._dim[0]):
                            a = self._matrix[i]
                            ind = i * other._axis[0] + j * other._axis[1]
                            b = other._matrix[ind]
                            sm += a * b
                        res.append(sm)
                    result.get_axis()
                    return res
            else:
                raise ValueError
        elif len(self._dim) == 2:
            if self._dim[1] == other._dim[0]:
                if len(other._dim) == 1:
                    result._dim = [self._dim[0], 1]
                    for i in range(self._dim[0]):
                        sm = 0
                        for j in range(self._dim[1]):
                            ind = i * self._axis[0] + j * self._axis[1]
                            sm += self._matrix[ind] * other._matrix[j]
                        res.append(sm)
                    result._matrix = res
                    result.get_axis()
                    return result
                elif len(other._dim) == 2:
                    result._dim = [self._dim[0], other._dim[1]]
                    for i in range(self._dim[0]):
                        for k in range(other._dim[1]):
                            sm = 0
                            for j in range(self._dim[1]):
                                ind1 = i * self._axis[0] + j * self._axis[1]
                                a = self._matrix[ind1]
                                ind2 = j * other._axis[0] + k * other._axis[1]
                                b = other._matrix[ind2]
                                sm += a * b
                            res.append(sm)
                    result._matrix = res
                    result.get_axis()
                    return result
            else:
                raise ValueError
