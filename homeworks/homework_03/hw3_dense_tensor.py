#!/usr/bin/env python
# coding: utf-8

from itertools import product
from copy import deepcopy


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
    operation = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
        "**": lambda x, y: x ** y,
    }
    stat = {
        "sum": lambda arr: sum(arr),
        "mean": lambda arr: sum(arr) / len(arr),
        "min": lambda arr: min(arr),
        "max": lambda arr: max(arr),
        "argmin": lambda arr: arr.index(min(arr)),
        "argmax": lambda arr: arr.index(max(arr)),
        "sum_vol": lambda arr: sum(arr),
        "mean_vol": lambda arr: sum(arr) / len(arr),
        "min_vol": lambda arr: min(arr),
        "max_vol": lambda arr: max(arr),
        "argmin_vol": lambda arr: arr.index(min(arr)),
        "argmax_vol": lambda arr: arr.index(max(arr)),
    }

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: list of lists
        """
        if isinstance(init_matrix_representation, tuple):
            self.matrix = [0 for i in range(init_matrix_representation[-1])]
            for i in range(2, len(init_matrix_representation) + 1):
                self.matrix = [deepcopy(self.matrix) for j in range(
                    init_matrix_representation[-i])]
            return
        self.matrix = init_matrix_representation

    def __getitem__(self, ind):
        a = self.matrix
        if isinstance(ind, tuple):
            for dim in ind:
                a = a[dim]
            return a
        if isinstance(self.matrix[0], list):
            if len(self.matrix[0]) > 1:
                return self.matrix[0][ind]
        return self.matrix[ind][0]

    def __setitem__(self, item, value):
        self._subdim(self.matrix[item[0]], item[1:], value)

    def _subdim(self, submatrix, item, value):
        if len(item) == 1:
            submatrix[item[0]] = value
            return
        self._subdim(submatrix[item[0]], item[1:], value)

    def __add__(self, other):
        return self.base_operations(other, "+")

    __radd__ = __add__

    def __sub__(self, other):
        return self.base_operations(other, "-")

    def __mul__(self, other):
        return self.base_operations(other, "*")

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        return self.base_operations(other, "/")

    def __pow__(self, other):
        return self.base_operations(other, "**")

    def base_operations(self, other, sign):
        try:
            if isinstance(other, Tensor):
                return Tensor([self.subdim_tensor(
                    self.matrix[i], other.matrix[i], sign) for i in range(len(self.matrix))])
            return Tensor([self.subdim_alpha(self.matrix[i], other, sign)
                           for i in range(len(self.matrix))])
        except BaseException:
            raise ValueError

    def __matmul__(self, other):
        if isinstance(self.matrix[0], list):
            factor0 = Tensor(self.matrix)
        else:
            factor0 = Tensor([self.matrix])
        if isinstance(other.matrix[0], list):
            factor1 = Tensor(other.matrix)
        else:
            factor1 = Tensor([[i] for i in other.matrix])
        comp = Tensor([[0 for j in range(len(factor1.matrix[0]))]
                       for i in range(len(factor0.matrix))])
        if len(factor1.matrix) == len(factor0.matrix[0]):
            for i in range(len(factor0.matrix)):
                for j in range(len(factor1.matrix[0])):
                    sum = 0
                    for k in range(len(factor0.matrix[0])):
                        sum += factor0[(i, k)] * factor1[(k, j)]
                    comp[(i, j)] = sum
            return comp
        raise ValueError

    def sum(self, axis=None):
        return self.statistic(axis, "sum")

    def mean(self, axis=None):
        return self.statistic(axis, "mean")

    def min(self, axis=None):
        return self.statistic(axis, "min")

    def max(self, axis=None):
        return self.statistic(axis, "max")

    def argmin(self, axis=None):
        return self.statistic(axis, "argmin")

    def argmax(self, axis=None):
        return self.statistic(axis, "argmax")

    def subdim_tensor(self, subdim, other_subdim, sign):
        if isinstance(subdim, list):
            return [
                self.subdim_tensor(
                    subdim[i],
                    other_subdim[i],
                    sign) for i in range(
                    len(subdim))]
        return self.operation[sign](subdim, other_subdim)

    def subdim_alpha(self, subdim, alpha, sign):
        if isinstance(subdim, list):
            return [
                self.subdim_alpha(
                    subdim[i],
                    alpha,
                    sign) for i in range(
                    len(subdim))]
        return self.operation[sign](subdim, alpha)

    def swapaxes(self, axe_frs, axe_snd):
        space = list(range(len(self.volume())))
        space[axe_frs], space[axe_snd] = space[axe_snd], space[axe_frs]
        return self.transpose(*space)

    def volume(self):
        vol = [len(self.matrix)]
        cur_dim = self.matrix[0]
        while isinstance(cur_dim, list):
            vol += [len(cur_dim)]
            cur_dim = cur_dim[0]
        return vol

    def statistic(self, axis, stat_oper):
        if axis is None:
            vol = self.volume()
            index = [range(i) for i in self.volume()]
            agregation = [self[i]for i in product(*index)]
            return self.stat[stat_oper](agregation)
        stat_oper += "_vol"
        vol = self.volume()
        ax = vol.pop(axis)
        res = Tensor(tuple(vol))
        index = [range(i) for i in vol]
        for ind in product(*index):
            ind = list(ind)
            lst = []
            for i in range(ax):
                ind.insert(axis, i)
                lst += [self[tuple(ind)]]
                ind.pop(axis)
            res[ind] = self.stat[stat_oper](lst)
        return res

    def transpose(self, *dim):
        vol = self.volume()
        res = Tensor(tuple(vol[i] for i in dim))
        coords = [range(i) for i in vol]
        for ptr in product(*coords):
            cur_ptr = [ptr[i] for i in dim]
            res[cur_ptr] = self[ptr]
        return res
