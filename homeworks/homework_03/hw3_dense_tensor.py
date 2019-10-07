#!/usr/bin/env python
# coding: utf-8

from copy import deepcopy
from itertools import product


class Tensor:
    def __init__(self, init_matrix_representation):
        self.matrix = init_matrix_representation

    @classmethod
    def create_empty_tensor(cls, size):
        empty_matrix = [0 for i in range(size[-1])]
        for i in range(2, len(size)+1):
            empty_matrix = [deepcopy(empty_matrix) for j in range(size[-i])]
        return cls(empty_matrix)

    def size_of_matrix(self):
            size_ = []
            mat = self.matrix
            try:
                while True:
                    size__ = len(mat)
                    size_.append(size__)
                    (mat) = mat[0]
            except:
                return size_

    def __setitem__(self, key, value):
        try:
            def dd(a, k, val):
                for i in range(len(k)-1):
                    a = a[k[i]]
                a[k[-1]] = val
            dd(self.matrix, key, value)
        except:
            self.matrix[key] = value

    def __getitem__(self, coordinates):
        if isinstance(coordinates, int):
            return self.matrix[coordinates]
        element = self.matrix
        for coordinate in coordinates:
            element = element[coordinate]
        return element

    def __add__(self, other):
        size = self.size_of_matrix()
        coordinates = [range(max_idx) for max_idx in size]
        result = Tensor.create_empty_tensor(size)
        if isinstance(other, Tensor):
            if self.size_of_matrix() != other.size_of_matrix():
                raise ValueError
            for coordinate in product(*coordinates):
                result[coordinate] = self[coordinate] + other[coordinate]
        elif isinstance(other, int) or isinstance(other, float):
            for coordinate in product(*coordinates):
                result[coordinate] = self[coordinate] + other
        return result

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        size = self.size_of_matrix()
        coordinates = [range(max_idx) for max_idx in size]
        result = Tensor.create_empty_tensor(size)
        if isinstance(other, Tensor):
            if self.size_of_matrix() != other.size_of_matrix():
                raise ValueError
            for coordinate in product(*coordinates):
                result[coordinate] = self[coordinate] - other[coordinate]
        elif isinstance(other, int) or isinstance(other, float):
            for coordinate in product(*coordinates):
                result[coordinate] = self[coordinate] - other
        return result

    def __mul__(self, other):
        size = self.size_of_matrix()
        coordinates = [range(max_idx) for max_idx in size]
        result = Tensor.create_empty_tensor(size)
        if isinstance(other, Tensor):
            if self.size_of_matrix() != other.size_of_matrix():
                raise ValueError
            for coordinate in product(*coordinates):
                result[coordinate] = self[coordinate] * other[coordinate]
        elif isinstance(other, int) or isinstance(other, float):
            for coordinate in product(*coordinates):
                result[coordinate] = self[coordinate] * other
        return result

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        size = self.size_of_matrix()
        coordinates = [range(max_idx) for max_idx in size]
        result = Tensor.create_empty_tensor(size)
        if isinstance(other, Tensor):
            if self.size_of_matrix() != other.size_of_matrix():
                raise ValueError
            for coordinate in product(*coordinates):
                result[coordinate] = self[coordinate] * (1/other[coordinate])
        elif isinstance(other, int) or isinstance(other, float):
            for coordinate in product(*coordinates):
                result[coordinate] = self[coordinate] * (1/other)
        return result

    def __pow__(self, other):
        size = self.size_of_matrix()
        coordinates = [range(max_idx) for max_idx in size]
        result = Tensor.create_empty_tensor(size)
        if isinstance(other, Tensor):
            if self.size_of_matrix() != other.size_of_matrix():
                raise ValueError
            for coordinate in product(*coordinates):
                result[coordinate] = self[coordinate] ** other[coordinate]
        elif isinstance(other, int) or isinstance(other, float):
            for coordinate in product(*coordinates):
                result[coordinate] = self[coordinate] ** other
        return result

    def __consider_tensor(self, axis=None):
        size = self.size_of_matrix()
        if axis is None:
            result = []
            coordinates = [range(max_idx) for max_idx in size]
            for coordinate in product(*coordinates):
                result.append(self[coordinate])
            max_el, min_el = max(result), min(result)
            return {'sum': sum(result),
                    'mean': sum(result)/len(result),
                    'max': max_el,
                    'min': min_el,
                    'argmax': result.index(max_el),
                    'argmin': result.index(min_el)}
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            result = {'sum': Tensor.create_empty_tensor(size),
                      'mean': Tensor.create_empty_tensor(size),
                      'max': Tensor.create_empty_tensor(size),
                      'min': Tensor.create_empty_tensor(size),
                      'argmax': Tensor.create_empty_tensor(size),
                      'argmin': Tensor.create_empty_tensor(size)}
            for coordinate in product(*coordinates):
                lst = []
                coordinate = list(coordinate)
                for i in range(max_idx):
                    coordinate.insert(axis, i)
                    lst.append(self[coordinate])
                    coordinate.pop(axis)
                result['sum'][coordinate] = sum(lst)
                result['mean'][coordinate] = sum(lst)/len(lst)
                result['max'][coordinate] = max(lst)
                result['min'][coordinate] = min(lst)
                result['argmax'][coordinate] = lst.index(result['max'][coordinate])
                result['argmin'][coordinate] = lst.index(result['min'][coordinate])
            return result

    def sum(self, axis=None):
        return self.__consider_tensor(axis)['sum']

    def mean(self, axis=None):
        return self.__consider_tensor(axis)['mean']

    def max(self, axis=None):
        return self.__consider_tensor(axis)['max']

    def min(self, axis=None):
        return self.__consider_tensor(axis)['min']

    def argmax(self, axis=None):
        return self.__consider_tensor(axis)['argmax']

    def argmin(self, axis=None):
        return self.__consider_tensor(axis)['argmin']

    def transpose(self, *new_dimensions):
        size = self.size_of_matrix()
        new_size = [size[dimension] for dimension in new_dimensions]
        result = Tensor.create_empty_tensor(new_size)
        coordinates = [range(max_idx) for max_idx in size]
        for coordinate in product(*coordinates):
            new_coor = [coordinate[dimension] for dimension in new_dimensions]
            result[new_coor] = self[coordinate]
        return result

    def swapaxes(self, a1, a2):
        new_dim = list(range(len(self.size_of_matrix())))
        new_dim[a1], new_dim[a2] = new_dim[a2], new_dim[a1]
        return self.transpose(*new_dim)

    def __matmul__(self, other):
        l1, l2 = len(self.size_of_matrix()), len(other.size_of_matrix())
        tensor1 = Tensor([self.matrix]) if l1 == 1 else self
        tensor2 = Tensor([[element] for element in other.matrix]) if l2 == 1 else other
        num1_of_rows, num1_of_columns = tensor1.size_of_matrix()
        num2_of_rows, num2_of_columns = tensor2.size_of_matrix()
        if num1_of_columns != num2_of_rows:
            raise ValueError
        n = num1_of_columns
        tensor2 = tensor2.transpose(1, 0)
        result = Tensor.create_empty_tensor((num1_of_rows, num2_of_columns))
        for i, row1 in enumerate(tensor1.matrix):
            for j, row2 in enumerate(tensor2.matrix):
                result[i, j] = sum([row1[k]*row2[k] for k in range(n)])
        result = Tensor(result.matrix[0]) if l1 == 1 else result
        result = Tensor([element[0] for element in result.matrix]) if l2 == 1 else result
        return result
