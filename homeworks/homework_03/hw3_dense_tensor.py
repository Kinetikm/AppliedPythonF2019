#!/usr/bin/env python
# coding: utf-8
import copy
import itertools as it


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
        self.mat = init_matrix_representation
        self._shape = self._calculate_shape()
        """
        :param init_matrix_representation: list of lists
        """

    def _calculate_shape(self):
        copy_arr = copy.deepcopy(self.mat)
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
            return self.mat[key]
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

        result = copy.deepcopy(self)
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
        result = copy.deepcopy(self)
        for _ in range(pow - 1):
            result = result._make_operation('*', self)
        return result

    def __matmul__(self, other):
        if self._shape[0] != other._shape[-1]:
            raise ValueError

        result = Tensor([[0] * other._shape[1]] * self._shape[0])
        length1 = len(result._shape)
        length2 = len(other._shape)
        if length1 == 1 and length2 == 1:
            for i in range(result._shape[0]):
                result.mat[i] = other.mat[i] * self.mat[i]

        elif length1 == 2 and length2 == 2:
            for i in range(result._shape[0]):
                for j in range(other._shape[1]):
                    for r in range(result._shape[0]):
                        result[i, j] = result[i, r] * other[r, j]

        elif length1 == 2 and length2 == 1:
            for i in range(other._shape[0]):
                for j in range(result._shape[0]):
                    for r in range(result._shape[0]):
                        result[i, j] = result[i, r] * other[r]

        elif length1 == 2 and length2 == 1:
            for i in range(result._shape[0]):
                for j in range(other._shape[1]):
                    for r in range(result._shape[0]):
                        result[i, j] = result[r] * other[r, j]

        return result

    def __str__(self):
        s = ''
        index = [0] * (len(self._shape))
        for index in it.product(*[range(k) for k in self._shape]):
            s += str(index) + ' ' + str(self[index]) + ' '
            s += '\n'

        return s
