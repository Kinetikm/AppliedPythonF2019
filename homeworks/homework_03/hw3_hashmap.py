#!/usr/bin/env python
# coding: utf-8
import numpy as np
import itertools
from copy import deepcopy
from itertools import product


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

    def dim(self, a):
        if not type(a) == list:
            return []
        return [len(a)] + self.dim(a[0])

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: list of lists
        """
        if isinstance(init_matrix_representation, list):
            self.tensor = deepcopy(init_matrix_representation)
            self.size = tuple(self.dim(self.tensor))
        elif isinstance(init_matrix_representation, tuple):
            self.size = init_matrix_representation
            self.tensor = [0 for i in range(self.size[-1])]
            for i in range(2, len(self.size) + 1):
                self.tensor = [deepcopy(self.tensor) for j in range(self.size[-i])]

    def __getitem__(self, ids):
        res = self.tensor
        try:
            if isinstance(ids, int):
                return res[ids]
            else:
                for i in ids:
                    res = res[i]
                return res
        except:
            raise IndexError

    def set_additional(self, data, ind, value):
        i = ind[0]
        if isinstance(data[i], list):
            self.set_additional(data[i], ind[1:], value)
        else:
            data[i] = value
            return True

    def __setitem__(self, ids, value):
        try:
            self.set_additional(self.tensor, ids, value)
        except:
            raise IndexError

    def additional_operation(self, data, other, func):
        if isinstance(data, list):
            for i, v in enumerate(data):
                if isinstance(other, list):
                    temp = self.additional_operation(data[i], other[i], func)
                else:
                    temp = self.additional_operation(data[i], other, func)
                if temp is not None:
                    data[i] = temp
        else:
            return func(data, other)

    def __add__(self, other):
        if isinstance(other, Tensor):
            if self.size != other.size:
                raise ValueError
            result = deepcopy(self.tensor)
            self.additional_operation(result, other.tensor, lambda x, y: x + y)
            return Tensor(result)
        elif isinstance(other, int) or isinstance(other, float):
            result = deepcopy(self.tensor)
            self.additional_operation(result, other, lambda x, y: x + y)
            return Tensor(result)
        raise ValueError

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Tensor):
            if self.size != other.size:
                raise ValueError
            result = deepcopy(self.tensor)
            self.additional_operation(result, other.tensor, lambda x, y: x - y)
            return Tensor(result)
        elif isinstance(other, int) or isinstance(other, float):
            result = deepcopy(self.tensor)
            self.additional_operation(result, other, lambda x, y: x - y)
            return Tensor(result)
        raise ValueError

    __rsub__ = __sub__

    def __mul__(self, other):
        if isinstance(other, Tensor):
            if self.size != other.size:
                raise ValueError
            result = deepcopy(self.tensor)
            self.additional_operation(result, other.tensor, lambda x, y: x * y)
            return Tensor(result)
        elif isinstance(other, int) or isinstance(other, float):
            result = deepcopy(self.tensor)
            self.additional_operation(result, other, lambda x, y: x * y)
            return Tensor(result)
        raise ValueError

    __rmul__ = __mul__

    def __pow__(self, power, modulo=None):
        if isinstance(power, int):
            result = deepcopy(self.tensor)
            self.additional_operation(result, power, lambda x, y: x ** y)
            return Tensor(result)
        raise ValueError

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            if other == 0:
                raise ZeroDivisionError
            result = deepcopy(self.tensor)
            self.additional_operation(result, other, lambda x, y: x / y)
            return Tensor(result)
        raise ValueError

    def __matmul__(self, other):
        if len(self.size) == 1 or len(other.size) == 1:
            return self.mulvector(other)
        if self.size[1] != other.size[0]:
            raise ValueError
        result = [[0 for _ in range(other.size[1])] for _ in range(self.size[0])]
        rows = {}
        col = {}
        for i, r in enumerate(self.tensor):
            for j, v in enumerate(r):
                try:
                    rows[i][j] = v
                except:
                    rows[i] = {}
                    rows[i][j] = v
        for i, r in enumerate(other.tensor):
            for j, v in enumerate(r):
                try:
                    col[j][i] = v
                except:
                    col[j] = {}
                    col[j][i] = v
        for i, v1 in rows.items():
            for j, v2 in col.items():
                result[i][j] = sum({k: v * v2[k] for k, v in v1.items() if k in v2}.values())
        return Tensor(result)

    def mulvector(self, second):
        rows = {}
        col = {}
        if len(self.size) == 1:
            result = [0 for _ in range(second.size[1])]
            for i, r in enumerate(second.tensor):
                for j, v in enumerate(r):
                    try:
                        col[j][i] = v
                    except:
                        col[j] = {}
                        col[j][i] = v
            rows = {i: self.tensor[i] for i in range(len(self.tensor))}
            for j, v2 in {0: rows}.items():
                for i, v1 in col.items():
                    result[i] = sum({k: v * v1[k] for k, v in v2.items() if k in v1}.values())
        else:
            result = [0 for _ in range(self.size[0])]
            for i, r in enumerate(self.tensor):
                for j, v in enumerate(r):
                    try:
                        rows[i][j] = v
                    except:
                        rows[i] = {}
                        rows[i][j] = v
                col = {i: second.tensor[i] for i in range(len(second.tensor))}
            for i, v1 in rows.items():
                result[i] = sum({k: v * col[k] for k, v in v1.items() if k in col}.values())
        return Tensor(result)

    __rmatmul__ = __matmul__

    def additional(self, func):
        arrays = [range(i) for i in self.size]
        cp = list(product(*arrays))
        res = []
        for i in cp:
            res.append(self[i])
        res_min = min(res)
        res_max = max(res)
        return func(res)

    def additional_axis(self, axis, func):
        temp_size = list(self.size)
        del temp_size[axis]
        arrays = [range(i) for i in temp_size]
        cp = list(product(*arrays))
        res = Tensor(tuple(temp_size))
        for ind in cp:
            temp = []
            for indexes in range(self.size[axis]):
                ind = list(ind)
                ind.insert(axis, indexes)
                temp.append(self[ind])
                del ind[axis]
            res[ind] = func(temp)
        return res

    def sum(self, axis=None):
        if axis is not None:
            return self.additional_axis(axis, lambda x: sum(x))
        return self.additional(lambda x: sum(x))

    def mean(self, axis=None):
        if axis is not None:
            return self.additional_axis(axis, lambda x: sum(x) / len(x))
        return self.additional(lambda x: sum(x) / len(x))

    def min(self, axis=None):
        if axis is not None:
            return self.additional_axis(axis, lambda x: min(x))
        return self.additional(lambda x: min(x))

    def max(self, axis=None):
        if axis is not None:
            return self.additional_axis(axis, lambda x: max(x))
        return self.additional(lambda x: max(x))

    def argmin(self, axis=None):
        if axis is not None:
            return self.additional_axis(axis, lambda x: x.index(min(x)))
        return self.additional(lambda x: x.index(min(x)))

    def argmax(self, axis=None):
        if axis is not None:
            return self.additional_axis(axis, lambda x: x.index(max(x)))
        return self.additional(lambda x: x.index(max(x)))

    def transpose(self, *size):
        temp_size = [self.size[i] for i in size]
        res = Tensor(tuple(temp_size))
        arrays = [range(i) for i in self.size]
        cp = list(product(*arrays))
        for ind in cp:
            res[[ind[i] for i in size]] = self[ind]
        return res

    def swapaxes(self, *axis):
        size = [i for i in range(len(self.size))]
        size[axis[0]], size[axis[1]] = size[axis[1]], size[axis[0]]
        return self.transpose(*size)
