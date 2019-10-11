#!/usr/bin/env python
# coding: utf-8
import numpy as np
import numpy.random as rand
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

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: list of lists
        """
        self.size = []
        self.list = []
        p = init_matrix_representation
        while isinstance(p, list) and len(p) > 0:
            self.size.append(len(p))
            p = p[0]

        def make_list(input_list):
            if isinstance(input_list, list):
                for i in input_list:
                    make_list(i)
            else:
                self.list.append(input_list)

        make_list(init_matrix_representation)

    def get_index_in_1dim(self, item):
        if isinstance(item, int):
            return item
        elif len(item) == len(self.size):
            l = len(item)
            index = item[l - 1]
            p = self.size[l - 1]
            for i in range(l - 1, -1, -1):
                if self.size[i] > item[i] >= 0:
                    if i > 0:
                        index += p * item[i - 1]
                        p *= self.size[i - 1]
                else:
                    raise IndexError
            return index
        else:
            raise IndexError

    def __getitem__(self, item):
        return self.list[self.get_index_in_1dim(item)]

    def __setitem__(self, key, value):
        self.list[self.get_index_in_1dim(key)] = value

    def create_copy(self):
        output = Tensor([])
        output.size = self.size.copy()
        output.list = self.list.copy()
        return output

    def operation(self, other, sign):
        if isinstance(other, (int, float)):
            output = self.create_copy()
            if other != 0:
                for i in range(len(output.list)):
                    if sign == '+':
                        output.list[i] += other
                    elif sign == '-':
                        output.list[i] -= other
                    elif sign == '*':
                        output.list[i] *= other
                    elif sign == '**':
                        output.list[i] **= other
                    elif sign == '/':
                        output.list[i] /= other
            elif other == 0:
                if sign == '*':
                    output.list = [0] * len(self.list)
                elif sign == '**':
                    output.list = [1] * len(self.list)
                elif sign == '/':
                    raise ZeroDivisionError
            return output
        elif isinstance(other, Tensor):
            output = self.create_copy()
            if self.size == other.size:
                for i in range(len(output.list)):
                    if sign == '+':
                        output.list[i] += other.list[i]
                    elif sign == '-':
                        output.list[i] -= other.list[i]
                    elif sign == '*':
                        output.list[i] *= other.list[i]
                    elif sign == '**':
                        output.list[i] **= other.list[i]
                return output
            else:
                raise ValueError
        else:
            raise TypeError

    def __add__(self, other):
        return self.operation(other, '+')

    def __radd__(self, other):
        return self.operation(other, '+')

    def __sub__(self, other):
        return self.operation(other, '-')

    def __rsub__(self, other):
        return self.operation(other, '-')

    def __mul__(self, other):
        return self.operation(other, '*')

    def __rmul__(self, other):
        return self.operation(other, '*')

    def __pow__(self, power, modulo=None):
        return self.operation(power, '**')

    def __truediv__(self, other):
        return self.operation(other, '/')

    def get_next_elem(self, coordinate):
        if len(coordinate) == len(self.size):
            for i in range(len(coordinate) - 1, -1, -1):
                coordinate[i] += 1
                if coordinate[i] < self.size[i]:
                    return
                coordinate[i] = 0
        else:
            raise ValueError

    def get_components(self, index):
        index %= len(self.list)
        d = [0] * (len(self.size) - 1) + [1]
        for i in range(len(self.size) - 2, -1, -1):
            d[i] = d[i + 1] * self.size[i + 1]
        comp = [0] * len(self.size)
        for i in range(len(self.size)):
            comp[i] = index // d[i]
            index %= d[i]
        return comp

    def get_statistic_in_axis(self, axis, o):
        if isinstance(self, Tensor):
            if axis is not None:
                coord = [0] * len(self.size)
                ans = Tensor([])
                ans.size = self.size.copy()
                ans.size.pop(axis)
                ans.list = [[[] for i in range(2)] for j in range(len(self.list) // self.size[axis])]
                for i in range(len(self.list)):
                    index = self.get_index_in_1dim(coord)
                    val = self.list[index]
                    ans_coord = coord.copy()
                    ans_coord.pop(axis)
                    ans[ans_coord][0].append(index)
                    ans[ans_coord][1].append(val)
                    self.get_next_elem(coord)
                for i in range(len(ans.list)):
                    if o == 'max':
                        ans.list[i] = max(ans.list[i][1])
                    if o == 'min':
                        ans.list[i] = min(ans.list[i][1])
                    if o == 'sum':
                        ans.list[i] = sum(ans.list[i][1])
                    if o == 'mean':
                        s = sum(ans.list[i][1])
                        s /= len(ans.list[i][1])
                        ans.list[i] = s
                    if o == 'argmax':
                        m = ans.list[i][1][0]
                        ind = 0
                        for x in range(len(ans.list[i][1])):
                            if m < ans.list[i][1][x]:
                                m = ans.list[i][1][x]
                                ind = x
                        ans.list[i] = self.get_components(ans.list[i][0][ind])[axis]
                    if o == 'argmin':
                        m = ans.list[i][1][0]
                        ind = 0
                        for x in range(len(ans.list[i][1])):
                            if m > ans.list[i][1][x]:
                                m = ans.list[i][1][x]
                                ind = x
                        ans.list[i] = self.get_components(ans.list[i][0][ind])[axis]
                return ans
            else:
                if o == 'max':
                    return max(self.list)
                if o == 'min':
                    return min(self.list)
                if o == 'sum':
                    return sum(self.list)
                if o == 'argmax':
                    m = self.list[0]
                    ind = 0
                    for i in range(len(self.list)):
                        if self.list[i] > m:
                            m = self.list[i]
                            ind = i
                    return ind
                if o == 'argmin':
                    m = self.list[0]
                    ind = 0
                    for i in range(len(self.list)):
                        if self.list[i] < m:
                            m = self.list[i]
                            ind = i
                    return ind
                if o == 'mean':
                    return self.sum() / len(self.list)

    def max(self, axis=None):
        return self.get_statistic_in_axis(axis, 'max')

    def min(self, axis=None):
        return self.get_statistic_in_axis(axis, 'min')

    def sum(self, axis=None):
        return self.get_statistic_in_axis(axis, 'sum')

    def mean(self, axis=None):
        return self.get_statistic_in_axis(axis, 'mean')

    def argmax(self, axis=None):
        return self.get_statistic_in_axis(axis, 'argmax')

    def argmin(self, axis=None):
        return self.get_statistic_in_axis(axis, 'argmin')

    def __matmul__(self, other):
        if isinstance(self, Tensor) and isinstance(self, Tensor):
            if len(self.size) < 3 and len(other.size) < 3:
                if self.size[-1] == other.size[0]:
                    ans = Tensor([])
                    if len(self.size) == 1 and len(other.size) > 1:
                        ans.size.append(other.size[1])
                        ans.list = [0] * other.size[1]
                        for i in range(self.size[0]):
                            for j in range(other.size[1]):
                                ans[j] += self[i] * other[i, j]
                    elif len(self.size) > 1 and len(other.size) == 1:
                        ans.size.append(self.size[0])
                        ans.list = [0] * self.size[0]
                        for i in range(self.size[0]):
                            for j in range(other.size[0]):
                                ans[i] += self[i, j] * other[j]
                    elif len(self.size) == 1 and len(other.size) == 1:
                        ans.size.append(1)
                        for i in range(self.size[0]):
                            ans.list[0] += self.list[i] * other.list[i]
                    else:
                        ans.list = [0] * (self.size[0] * other.size[1])
                        ans.size = [self.size[0], other.size[1]]
                        for i in range(self.size[0]):
                            for j in range(other.size[1]):
                                for k in range(self.size[1]):
                                    ans[i, j] += self[i, k] * other[k, j]
                    return ans
                else:
                    raise ValueError
            else:
                raise ValueError
        else:
            raise ValueError

    def transpose(self, *args):
        if isinstance(args, (list, tuple)) and len(args) == len(self.size):
            ans = Tensor([])
            ans.list = [None] * len(self.list)
            coord = [0] * len(self.size)
            ans.size = []
            for i in range(len(self.size)):
                ans.size.append(self.size[args[i]])
            for i in range(len(self.list)):
                new_coord = []
                for i in range(len(self.size)):
                    new_coord.append(coord[args[i]])
                ans[new_coord] = self[coord]
                self.get_next_elem(coord)
            return ans
        else:
            raise ValueError

    def swapaxes(self, a1, a2):
        p = []
        for i in range(len(self.size)):
            p.append(i)
        p[a1] = a2
        p[a2] = a1
        return self.transpose(*p)
