#!/usr/bin/env python
# coding: utf-8
import itertools
from copy import deepcopy
from numpy import prod
from operator import itemgetter
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

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: list of lists
        """
        self.shape = []
        self.dim = self._test_dim(init_matrix_representation)
        if self.dim is None:
            raise ValueError('input not a list')
        self.elements = init_matrix_representation
        for _ in range(self.dim-1):
            self.elements = [item for item in itertools.chain.from_iterable(self.elements)]
        if prod(self.shape) != len(self.elements):
            raise ValueError('missing element in input matrix')

    def _test_dim(self, testlist, dim=0):
        if isinstance(testlist, list):
            if not testlist:
                return dim
            dim = dim + 1
            self.shape.append(len(testlist))
            dim = self._test_dim(testlist[0], dim)
            return dim
        else:
            if dim == 0:
                return None
            else:
                return dim

    def __len__(self):
        return self.shape[0]*self.shape[1]

    def __getitem__(self, pos):
        offset = 0
        for i in range(len(pos)):
            index = pos[i]
            if index < 0:
                raise IndexError("Negative index")
            if index >= self.shape[i]:
                raise IndexError("Index out of range")
            offset += int(prod(self.shape[i+1:]))*index
        return self.elements[offset]

    def __setitem__(self, pos, value):
        offset = 0
        for i in range(len(pos)):
            index = pos[i]
            if index < 0:
                raise IndexError("Negative index")
            if index >= self.shape[i]:
                raise IndexError("Index out of range")
            offset += int(prod(self.shape[i + 1:])) * index
        self.elements[offset] = value

    def __add__(self, other):
        if not isinstance(other, Tensor):
            result = deepcopy(self)
            for i in range(len(self.elements)):
                result.elements[i] = self.elements[i] + other
            return result
        if self.shape != other.shape:
            raise ValueError('dimension mismatch')
        result = deepcopy(other)
        for i in range(len(self.elements)):
            result.elements[i] = self.elements[i] + other.elements[i]
        return result

    def __sub__(self, other):
        if not isinstance(other, Tensor):
            result = deepcopy(self)
            for i in range(len(self.elements)):
                result.elements[i] = self.elements[i] - other
            return result
        if self.shape != other.shape:
            raise ValueError('dimension mismatch')
        result = deepcopy(other)
        for i in range(len(self.elements)):
            result.elements[i] = self.elements[i] - other.elements[i]
        return result

    def __mul__(self, other):
        if not isinstance(other, Tensor):
            result = deepcopy(self)
            for i in range(len(self.elements)):
                result.elements[i] = self.elements[i] * other
            return result
        if self.shape != other.shape:
            raise ValueError('dimension mismatch')
        result = deepcopy(other)
        for i in range(len(self.elements)):
            result.elements[i] = self.elements[i] * other.elements[i]
        return result

    def __radd__(self, other):
        result = deepcopy(self)
        for i in range(len(self.elements)):
            result.elements[i] = self.elements[i] + other
        return result

    def __rsub__(self, other):
        result = deepcopy(self)
        for i in range(len(self.elements)):
            result.elements[i] = self.elements[i] - other
        return result

    def __rmul__(self, other):
        result = deepcopy(self)
        for i in range(len(self.elements)):
            result.elements[i] = self.elements[i] * other
        return result

    def __truediv__(self, other):
        result = deepcopy(self)
        for i in range(len(result.elements)):
            result.elements[i] /= other
        return result

    def __pow__(self, power, modulo=None):
        result = deepcopy(self)
        for i in range(len(result.elements)):
            result.elements[i] = pow(result.elements[i], power)
        return result

    def __str__(self):
        return str(self.elements)

    def sum(self, axis=None):
        if axis is None:
            return sum(self.elements)
        result_shape = [self.shape[i] for i in range(self.dim) if i != axis]
        result = np.zeros(result_shape)
        selected_index = [i for i in range(self.dim) if i!=axis]
        for i in range(len(self.elements)):
            index = self._get_index(i)
            # print(index)
            index = [index[j] for j in selected_index]
            # print(index)
            result[tuple(index)] += self.elements[i]
            # print(result)
        return result

    def mean(self, axis=None):
        if axis is None:
            return sum(self.elements)/len(self.elements)
        result_shape = [self.shape[i] for i in range(self.dim) if i != axis]
        result = np.zeros(result_shape)
        selected_index = [i for i in range(self.dim) if i!=axis]
        for i in range(len(self.elements)):
            index = self._get_index(i)
            # print(index)
            index = [index[j] for j in selected_index]
            # print(index)
            result[tuple(index)] += self.elements[i]
            # print(result)
        return result/self.shape[axis]

    def max(self, axis=None):
        if axis is None:
            return max(self.elements)
        result_shape = [self.shape[i] for i in range(self.dim) if i != axis]
        result = np.zeros(result_shape)
        selected_index = [i for i in range(self.dim) if i!=axis]
        for i in range(len(self.elements)):
            index = self._get_index(i)
            # print(index)
            index = [index[j] for j in selected_index]
            # print(index)
            if result[tuple(index)] < self.elements[i]:
                result[tuple(index)] = self.elements[i]
            # print(result)
        return result

    def min(self, axis=None):
        if axis is None:
            return min(self.elements)
        result_shape = [self.shape[i] for i in range(self.dim) if i != axis]
        result = np.zeros(result_shape)
        selected_index = [i for i in range(self.dim) if i!=axis]
        for i in range(len(self.elements)):
            index = self._get_index(i)
            # print(index)
            index = [index[j] for j in selected_index]
            # print(index)
            if result[tuple(index)] > self.elements[i]:
                result[tuple(index)] = self.elements[i]
            # print(result)
        return result

    def argmax(self, axis=None):
        if axis is None:
            return self.elements.index(max(self.elements))
        result_shape = [self.shape[i] for i in range(self.dim) if i != axis]
        result = np.zeros(result_shape)
        result_indeces = np.zeros(result_shape)
        selected_index = [i for i in range(self.dim) if i!=axis]
        for i in range(len(self.elements)):
            index = self._get_index(i)
            # print(index)
            index_sel = [index[j] for j in selected_index]
            # print(index)
            if result[tuple(index_sel)] < self.elements[i]:
                result[tuple(index_sel)] = self.elements[i]
                result_indeces[tuple(index_sel)] = index[axis]
            # print(result)
        return result_indeces.astype(int)

    def argmin(self, axis=None):
        if axis is None:
            return self.elements.index(min(self.elements))
        result_shape = [self.shape[i] for i in range(self.dim) if i != axis]
        result = np.zeros(result_shape)
        result_indeces = np.zeros(result_shape)
        selected_index = [i for i in range(self.dim) if i!=axis]
        for i in range(len(self.elements)):
            index = self._get_index(i)
            # print(index)
            index_sel = [index[j] for j in selected_index]
            # print(index)
            if result[tuple(index_sel)] > self.elements[i]:
                result[tuple(index_sel)] = self.elements[i]
                result_indeces[tuple(index_sel)] = index[axis]
            # print(result)
        return result_indeces.astype(int)

    def _get_index(self, position):
        """return indexes  of element in self.elements"""
        if position >= len(self.elements):
            raise IndexError('element position out of range')
        indexes = [0 for _ in range(self.dim)]
        for i in range(self.dim):
            indexes[i] = int(position//(prod(self.shape[i+1:])))
            position = int(position%(prod(self.shape[i+1:])))
        return indexes

    @staticmethod
    def zeros(shape, init=0):
        """return list of list contains zeros with shape *args"""
        dp = init
        for x in reversed(shape):
            dp = [deepcopy(dp) for _ in range(x)]
        return dp




if __name__ == '__main__':
    '''m = Tensor([[[1, 1], [1, 1]], [[2, 2], [2, 2]]])
    k = Tensor([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    n = Tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # print(m[0, 0, 0])
    # print(m[1, 1, 1])
    # print(n[1, 1])
    # print(n[2, 1])
    # print(m[2, 1])
    # m[2, 1] = 0
    # print(m[2, 1])
    # print(pow(m, 2))
    #print(m+k)
    #print(m)
    #print(k)
    #print(m.max(axis=0))
    print(n.mean(axis=0))'''
    shapes = (3, 3, 3, 2)
    matrix = np.random.randint(-20, 30, shapes)
    tensor = Tensor(matrix.tolist())
    argmax = tensor.argmin(axis=0)
    argmax_true = matrix.argmin(axis=0)
    #print(matrix)
    print(argmax)
    print(argmax_true)


