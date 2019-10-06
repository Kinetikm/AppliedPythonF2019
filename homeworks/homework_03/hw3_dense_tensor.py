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

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: list of lists
        """
        self._matrix = init_matrix_representation

    @classmethod
    def empty_tensor(cls, size):
        empty_matrix = [0 for _ in range(size[-1])]
        for i in range(2, len(size) + 1):
            empty_matrix = [deepcopy(empty_matrix) for _ in range(size[-i])]
        return cls(empty_matrix)

    def size(self):
        s = [len(self._matrix)]
        line = self._matrix
        while isinstance(line[0], list):
            s.append(len(line[0]))
            line = line[0]
        return s

    def __add__(self, other):
        return self._binary_operator(other, 'add')

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self._binary_operator(other, 'sub')

    def __mul__(self, other):
        return self._binary_operator(other, 'mul')

    def __truediv__(self, other):
        return self._binary_operator(other, 'div')

    def __pow__(self, other):
        return self._binary_operator(other, 'pow')

    def sum(self, axis=None):
        return self._tensor_stat(axis, 'sum')

    def mean(self, axis=None):
        return self._tensor_stat(axis, 'mean')

    def min(self, axis=None):
        return self._tensor_stat(axis, 'min')

    def max(self, axis=None):
        return self._tensor_stat(axis, 'max')

    def argmax(self, axis=None):
        return self._tensor_stat(axis, 'argmax')

    def argmin(self, axis=None):
        return self._tensor_stat(axis, 'argmin')

    def _binary_operator(self, other, command):
        cords = [range(max_index) for max_index in self.size()]
        result = Tensor.empty_tensor(self.size())
        if isinstance(other, Tensor):
            if self.size() != other.size():
                raise ValueError
            for cord in product(*cords):
                if command == 'add':
                    result[cord] = self[cord] + other[cord]
                elif command == 'sub':
                    result[cord] = self[cord] - other[cord]
                elif command == 'mul':
                    result[cord] = self[cord] * other[cord]
                elif command == 'div':
                    result[cord] = self[cord] / other[cord]
                elif command == 'pow':
                    result[cord] = self[cord] ** other[cord]
        elif isinstance(other, int) or isinstance(other, float):
            for cord in product(*cords):
                if command == 'add':
                    result[cord] = self[cord] + other
                elif command == 'sub':
                    result[cord] = self[cord] - other
                elif command == 'mul':
                    result[cord] = self[cord] * other
                elif command == 'div':
                    result[cord] = self[cord] / other
                elif command == 'pow':
                    result[cord] = self[cord] ** other
        return result

    def _tensor_stat(self, axis, param):
        if axis is None:
            result = []
            cords = [range(max_index) for max_index in self.size()]
            for cord in product(*cords):
                result.append(self[cord])
            if param == 'sum':
                return sum(result)
            elif param == 'mean':
                return sum(result)/len(result)
            elif param == 'max':
                return max(result)
            elif param == 'min':
                return min(result)
            elif param == 'argmax':
                return result.index(max(result))
            elif param == 'argmin':
                return result.index(min(result))
        else:
            tmp_size = self.size()
            max_index = tmp_size.pop(axis)
            cords = [range(max_idx) for max_idx in tmp_size]
            result = Tensor.empty_tensor(tmp_size)
            for cord in product(*cords):
                tmp = []
                cord = list(cord)
                for i in range(max_index):
                    cord.insert(axis, i)
                    tmp.append(self[cord])
                    cord.pop(axis)
                if param == 'sum':
                    result[cord] = sum(tmp)
                elif param == 'mean':
                    result[cord] = sum(tmp) / len(tmp)
                elif param == 'max':
                    result[cord] = max(tmp)
                elif param == 'min':
                    result[cord] = min(tmp)
                elif param == 'argmax':
                    result[cord] = tmp.index(max(tmp))
                elif param == 'argmin':
                    result[cord] = tmp.index(min(tmp))
            return result

    def __matmul__(self, other):
        operand_1 = self
        operand_2 = other
        length_1 = len(operand_1.size())
        length_2 = len(operand_2.size())
        if length_1 == 1:
            operand_1 = Tensor([self._matrix])
        if length_2 == 1:
            operand_2 = Tensor([[e] for e in other.get_matrix()])
        m_1, n_1 = operand_1.size()
        m_2, n_2 = operand_2.size()
        if n_1 != m_2:
            raise ValueError
        operand_2 = operand_2.transpose(1, 0)
        result = Tensor.empty_tensor((m_1, n_2))
        for i, row_1 in enumerate(operand_1._matrix):
            for j, row_2 in enumerate(operand_2._matrix):
                tmp = []
                for k in range(n_1):
                    tmp.append(row_1[k] * row_2[k])
                result[i, j] = sum(tmp)
        if length_1 == 1:
            return Tensor(result._matrix[0])
        if length_2 == 1:
            return Tensor([item[0] for item in result._matrix])
        return result

    def swapaxes(self, axe1, axe2):
        tmp_dim = list(range(len(self.size())))
        tmp_dim[axe1], tmp_dim[axe2] = tmp_dim[axe2], tmp_dim[axe1]
        result = self.transpose(*tmp_dim)
        return result

    def __setitem__(self, cords, value):
        if isinstance(cords, int):
            self._matrix[cords] = value
            return
        item = self._matrix
        for i in range(len(cords) - 1):
            item = item[cords[i]]
        item[cords[-1]] = value

    def __getitem__(self, cords):
        if isinstance(cords, int):
            return self._matrix[cords]
        elem = self._matrix
        for cord in cords:
            elem = elem[cord]
        return elem

    def transpose(self, *axes):
        size = self.size()
        result = Tensor.empty_tensor([size[dim] for dim in axes])
        cords = [range(max_index) for max_index in size]
        for cord in product(*cords):
            new_cord = [cord[dim] for dim in axes]
            result[new_cord] = self[cord]
        return result

    def get_matrix(self):
        return self._matrix
