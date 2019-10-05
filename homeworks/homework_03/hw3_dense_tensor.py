#!/usr/bin/env python
# coding: utf-8
import itertools
from copy import deepcopy, copy
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

    def _get_ofset(self, pos):
        shape = self.shape
        offset = 0
        if self.dim == 1:
            return pos
        for i in range(len(pos)):
            index = pos[i]
            if index < 0:
                raise IndexError("Negative index")
            if index >= shape[i]:
                raise IndexError("Index out of range")
            offset += int(prod(shape[i+1:]))*index
        return offset

    def _get_index(self, position):
        """return indexes  of element in self.elements"""
        if position >= len(self.elements):
            raise IndexError('element position out of range')
        if self.dim == 1:
            return position
        indexes = [0 for _ in range(self.dim)]
        for i in range(self.dim):
            indexes[i] = int(position//(prod(self.shape[i+1:])))
            position = int(position%(prod(self.shape[i+1:])))
        return indexes

    def __getitem__(self, pos):
        '''offset = 0
        for i in range(len(pos)):
            index = pos[i]
            if index < 0:
                raise IndexError("Negative index")
            if index >= self.shape[i]:
                raise IndexError("Index out of range")
            offset += int(prod(self.shape[i+1:]))*index'''
        offset = self._get_ofset(pos)
        return self.elements[offset]

    def __setitem__(self, pos, value):
        '''offset = 0
        for i in range(len(pos)):
            index = pos[i]
            if index < 0:
                raise IndexError("Negative index")
            if index >= self.shape[i]:
                raise IndexError("Index out of range")
            offset += int(prod(self.shape[i + 1:])) * index'''
        offset = self._get_ofset(pos)
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

    def transpose(self, *axis):
        axis = list(axis)
        if len(axis) < self.dim:
            raise ValueError("axes don't match array")
        result = deepcopy(self)
        result.shape = list(np.array(self.shape)[axis])
        for i in range(len(self.elements)):
            index = np.array(self._get_index(i))
            index = index[axis]
            result[index] = self.elements[i]
        return result

    def swapaxes(self, ax1, ax2):
        new_shape = copy(self.shape)
        new_shape[ax1], new_shape[ax2] = new_shape[ax2], new_shape[ax1]
        result = deepcopy(self)
        result.shape = new_shape
        for i in range(len(self.elements)):
            index = np.array(self._get_index(i))
            index[ax1], index[ax2] = index[ax2], index[ax1]
            result[index] = self.elements[i]
        return result

    def __matmul__(self, other: 'Tensor'):
        if not self.dim <= 2 and other.dim <= 2:
            raise ValueError("Tensor rang greater then 2")
        if self.dim == 1:
            # умножаем вектор-строку на матрицу
            if self.shape[0] != other.shape[0]:
                raise ValueError("Dimension mismatch")
            result = np.zeros((other.shape[1]))
            for y in range(result.shape[0]):
                result[y] = sum((self.__getitem__(j) * other[j, y] for j in range(other.shape[0])))
            return Tensor(result.tolist())
        if other.dim == 1:
            # умножаем матрицу на вектор столбец
            if self.shape[1] != other.shape[0]:
                raise ValueError("Dimension mismatch")
            result = np.zeros((self.shape[0]))
            for x in range(result.shape[0]):
                result[x] = sum((self.__getitem__([x, j]) * other[j] for j in range(other.shape[0])))
            return Tensor(result.tolist())
        if self.shape[1] != other.shape[0]:
            raise ValueError("Dimension mismatch")
        if other.dim == 1:
             result = np.zeros((self.shape[0], other.shape[0]))
        else:
            result = np.zeros((self.shape[0], other.shape[1]))
        for x in range(result.shape[0]):
            for y in range(result.shape[1]):
                result[x,y] = sum((self.__getitem__([x, j]) * other[j, y] for j in range(other.shape[0])))
        return Tensor(result.tolist())


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
    '''
    np.random.seed(42)
    shapes = (20, 10, 20, 10)
    matrix = np.random.randint(-20, 30, shapes)
    #m = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    #matrix = np.array(m)
    tensor = Tensor(matrix.tolist())
    s_true = matrix.transpose(2, 0, 3, 1)
    s = tensor.transpose(2, 0, 3, 1)
    for ind in itertools.product(*[range(k) for k in s_true.shape]):
        if not s[ind] == s_true[ind]:
            print(ind)
    #print(matrix)
    #print(s_true)
    #print(s)

    '''
    np.random.seed(42)

    shapes = (20, 10, 20, 10)
    matrix = np.random.randint(-20, 30, shapes)
    tensor = Tensor(matrix.tolist())

    s = tensor.transpose(2, 0, 3, 1)
    s_true = matrix.transpose(2, 0, 3, 1)
    s1 = tensor.swapaxes(2, 0)
    s1_true = matrix.swapaxes(2, 0)

    for ind in itertools.product(*[range(k) for k in s_true.shape]):
        assert s[ind] == s_true[ind]

    for ind in itertools.product(*[range(k) for k in s1_true.shape]):
        assert s1[ind] == s1_true[ind]

