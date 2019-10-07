#!/usr/bin/env python
# coding: utf-8

import itertools
import copy
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

    class Matrix():
        def __init__(self, init_matrix_representation):
            self.matrix = init_matrix_representation
            self.dimension = 0
            x = self.matrix
            self.size = []
            while True:
                if isinstance(x, list):
                    self.size.append(len(x))
                    x = x[0]
                    self.dimension += 1
                else:
                    break

        def __getitem__(self, item):
            x = self.matrix
            if isinstance(item, int):
                x = x[item]
            else:
                for i in range(self.dimension):
                    x = x[item[i]]
            return x

        def __setitem__(self, key, value):
            # if self.dimension != len(key):
            #     raise IndexError
            s = 'self.matrix'
            if isinstance(key, int):
                s += '[' + str(key) + ']'
            else:
                for i in key:
                    s += '[' + str(i) + ']'
            s += ' = value'
            exec(s)

        def __str__(self):
            return (f'{self.matrix}')

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: list of lists
        """
        self.tensor = self.Matrix(init_matrix_representation)
        self.dimension = self.tensor.dimension
        self.size = self.tensor.size
        self.ll = []
        for i in range(self.dimension):
            self.ll.append([j for j in range(self.size[i])])

    def __setitem__(self, key, value):
        self.tensor[key] = value

    def __getitem__(self, item):

        return self.tensor[item]

    def __str__(self):
        return (f'{self.tensor.matrix}')

    def __mul__(self, other):
        try:
            C = copy.deepcopy(self.tensor)
            if isinstance(other, int) or isinstance(other, float):
                for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                    C[index] = self.tensor[index] * other
                result = Tensor(C.matrix)
                return result
            elif isinstance(other, Tensor):
                for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                    C[index] = self.tensor[index] * other.tensor[index]
                result = Tensor(C.matrix)
                return result
            else:
                raise ValueError
        except ValueError:
            pass

    def __rmul__(self, other):
        try:
            C = copy.deepcopy(self.tensor)
            if isinstance(other, int) or isinstance(other, float):
                for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                    C[index] = self.tensor[index] * other
                result = Tensor(C.matrix)
                return result

        except ValueError:
            pass

    def __add__(self, other):

        C = copy.deepcopy(self.tensor)
        if isinstance(self, Tensor) and (isinstance(other, int) or isinstance(other, float)):
            for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                C[index] = self.tensor[index] + other
            result = Tensor(C.matrix)
            return result
        elif isinstance(other, Tensor) and isinstance(self, Tensor):
            if other.size == self.size:
                C = copy.deepcopy(self.tensor)
                for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                    C[index] = self.tensor[index] + other.tensor[index]
                result = Tensor(C.matrix)

                return result
            else:
                raise ValueError
        else:
            raise ValueError

    def __radd__(self, other):
        C = copy.deepcopy(self.tensor)
        if isinstance(self, Tensor) and (isinstance(other, int) or isinstance(other, float)):
            for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                C[index] = self.tensor[index] + other
            result = Tensor(C.matrix)
            return result

        else:
            raise ValueError

    def __sub__(self, other):
        C = copy.deepcopy(self.tensor)
        if isinstance(self, Tensor) and (isinstance(other, int) or isinstance(other, float)):
            for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                C[index] = self.tensor[index] - other
            result = Tensor(C.matrix)
            return result
        elif isinstance(other, Tensor) and isinstance(self, Tensor):
            if other.size == self.size:

                C = copy.deepcopy(self.tensor)
                for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                    C[index] = self.tensor[index] - other.tensor[index]
                result = Tensor(C.matrix)

                return result
            else:
                raise ValueError
        else:
            raise ValueError

    def __rsub__(self, other):
        def __sub__(self, other):
            C = copy.deepcopy(self.tensor)

            if isinstance(self, Tensor) and (isinstance(other, int) or isinstance(other, float)):

                for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                    C[index] = self.tensor[index] - other
                result = Tensor(C.matrix)
                return result
            elif isinstance(other, Tensor) and isinstance(self, Tensor):
                if other.size == self.size:

                    C = copy.deepcopy(self.tensor)
                    for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                        C[index] = self.tensor[index] - other.tensor[index]
                    result = Tensor(C.matrix)

                    return result
                else:
                    raise ValueError
            else:
                raise ValueError

    def __truediv__(self, other):
        C = copy.deepcopy(self.tensor)

        if isinstance(other, int) or isinstance(other, float):
            if other is 0:
                raise ZeroDivisionError

            for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                C[index] = self.tensor[index] / other
            result = Tensor(C.matrix)
            return result
        else:
            raise ValueError

    def __pow__(self, power, modulo=None):
        C = copy.deepcopy(self.tensor)
        if isinstance(power, int) or isinstance(power, float):

            for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                C[index] = self.tensor[index] ** power
            result = Tensor(C.matrix)
            return result
        else:
            raise ValueError

    def sum(self, axis=None):
        if axis is None:
            sum = 0

            for index in itertools.product(*[self.ll[i] for i in range(len(self.ll))]):
                sum += self.tensor[index]
            return sum
        else:
            a = np.array(self.tensor.matrix)
            return a.sum(axis=axis)

    def max(self, axis=None):
        max = self.tensor[[0 for _ in range(self.dimension)]]
        if axis is None:
            list_of_list_of_index = []
            for i in range(self.dimension):
                list_of_list_of_index.append([j for j in range(self.size[i])])
            for index in itertools.product(*[list_of_list_of_index[i] for i in range(len(list_of_list_of_index))]):
                if max < self.tensor[index]:
                    max = self.tensor[index]
            return max
        else:
            a = np.array(self.tensor.matrix)
            return a.max(axis=axis)

    def min(self, axis=None):
        min = self.tensor[[0 for _ in range(self.dimension)]]
        if axis is None:
            list_of_list_of_index = []
            for i in range(self.dimension):
                list_of_list_of_index.append([j for j in range(self.size[i])])
            for index in itertools.product(*[list_of_list_of_index[i] for i in range(len(list_of_list_of_index))]):
                if min > self.tensor[index]:
                    min = self.tensor[index]
            return min
        else:
            a = np.array(self.tensor.matrix)
            return a.min(axis=axis)

    def argmax(self, axis=None):
        # max = self.tensor[[0 for _ in range(self.dimension)]]
        # arg = [[0 for _ in range(self.dimension)]]
        # if axis is None:
        #     list_of_list_of_index = []
        #     for i in range(self.dimension):
        #         list_of_list_of_index.append([j for j in range(self.size[i])])
        #     for index in itertools.product(*[list_of_list_of_index[i] for i in range(len(list_of_list_of_index))]):
        #         if max < self.tensor[index]:
        #             max = self.tensor[index]
        #             arg = index
        #     return arg
        # else:
        #     a = np.array(self.tensor.matrix)
        #     return a.argmax(axis=axis)
        a = np.array(self.tensor.matrix)
        return a.argmax(axis=axis)

    def argmin(self, axis=None):
        # min = self.tensor[[0 for _ in range(self.dimension)]]
        # arg = [[0 for _ in range(self.dimension)]]
        # if axis is None:
        #     list_of_list_of_index = []
        #     for i in range(self.dimension):
        #         list_of_list_of_index.append([j for j in range(self.size[i])])
        #     for index in itertools.product(*[list_of_list_of_index[i] for i in range(len(list_of_list_of_index))]):
        #         if min > self.tensor[index]:
        #             min = self.tensor[index]
        #             arg = index
        #     return arg
        # else:
        #     a = np.array(self.tensor.matrix)
        #     return a.argmin(axis=axis)
        a = np.array(self.tensor.matrix)
        return a.argmin(axis=axis)

    def mean(self, axis=None):
        sum = 0
        if axis is None:
            count_el = 1
            for i in self.size:
                count_el *= i
            sum = 0
            list_of_list_of_index = []
            for i in range(self.dimension):
                list_of_list_of_index.append([j for j in range(self.size[i])])
            for index in itertools.product(*[list_of_list_of_index[i] for i in range(len(list_of_list_of_index))]):
                sum += self.tensor[index]
            return sum / count_el
        else:
            a = np.array(self.tensor.matrix)
            return a.mean(axis=axis)

    def transpose(self, *args):
        a = np.array(self.tensor.matrix)
        return a.transpose(*args)

    def swapaxes(self, *args):
        a = np.array(self.tensor.matrix)
        return a.swapaxes(*args)

    def __matmul__(self, other):
        if isinstance(other, Tensor):
            if len(self.size) == 1:
                if self.size[0] == other.size[0]:
                    result = Tensor([0] * other.size[1])
                    for i in range(other.size[1]):
                        for j in range(self.size[0]):
                            result[i] += self.tensor[j] * other.tensor[j, i]
                    return result
                else:
                    print("Незьзя перемножить матрицы таких размеров")
                    raise Exception

            elif len(other.size) == 1:
                if self.size[1] == other.size[0]:
                    result = Tensor([0] * self.size[0])
                    for i in range(self.size[0]):
                        for j in range(self.size[1]):
                            result[i] += other.tensor[j] * self.tensor[i, j]
                    return result
                else:
                    print("Незьзя перемножить матрицы таких размеров")
                    raise Exception

            elif self.size[1] == other.size[0]:
                result_m = []
                for i in range(self.size[0]):
                    x = []
                    for j in range(other.size[1]):
                        x.append(0)
                    result_m.append(x)
                result = Tensor(result_m)
                for i in range(self.size[0]):
                    for j in range(other.size[1]):
                        for k in range(self.size[1]):
                            result[i, j] += self.tensor[i, k] * other.tensor[k, j]

                return result

            else:
                print("Незьзя перемножить матрицы таких размеров")
                raise ValueError
        else:
            raise ValueError
