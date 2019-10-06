#!/usr/bin/env python
# coding: utf-8


class Tensor:
    """
    Your realisation of numpy tensor.

    Must be implemented:
    3. Sum, mean, max, min, argmax, argmin by axis.
    if axis is None then operation over all elements.
    4. Transpose by given axes (by default reverse dimensions).
    5. Swap two axes.
    6. Matrix multiplication for tensors with dimension <= 2.
    """

    def shape_calc(matrix):
        shape = [len(matrix)]
        axis = matrix[0]
        while isinstance(axis, list):
            shape += [len(axis)]
            axis = axis[0]
        return shape

    def flat_matrix(matrix):
        line = []
        if len(Tensor.shape_calc(matrix)) == 1:
            return matrix
        else:
            for row in matrix:
                line += Tensor.flat_matrix(row)
            return line

    def __init__(self, init_matrix_representation, shape=None):
        raise NotImplementedError
        self.matrix = Tensor.flat_matrix(init_matrix_representation)
        if shape is None:
            self.shape = Tensor.shape_calc(init_matrix_representation)
        else:
            self.shape = shape
        print(self.shape)
        self.dim = len(self.shape)
        self.num_of_el = self.shape[0]
        for i in range(1, self.dim):
            self.num_of_el *= self.shape[i]

    def index_calc(num_of_el, shape, ind, start_i=0):
        if isinstance(ind, int):
            return ind
        elif start_i == len(ind) - 1:
            return ind[start_i]
        elif isinstance(ind, tuple):
            index = 0
            index += ind[start_i]*(num_of_el // shape[start_i])
            index += Tensor.index_calc(num_of_el // shape[start_i], shape, ind, start_i+1)
            return index

    def __getitem__(self, ind):
        return self.matrix[Tensor.index_calc(self.num_of_el, self.shape, ind)]

    def __setitem__(self, ind, value):
        self.matrix[Tensor.index_calc(self.num_of_el, self.shape, ind)] = value

    def __add__(self, other):
        if isinstance(other, Tensor):
            if self.shape == other.shape:
                return Tensor([self.matrix[i] + other.matrix[i] for i in range(self.num_of_el)], self.shape)
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            return Tensor([self.matrix[i] + other for i in range(self.num_of_el)], self.shape)
        else:
            raise ValueError

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Tensor):
            if self.shape == other.shape:
                return Tensor([self.matrix[i] - other.matrix[i] for i in range(self.num_of_el)], self.shape)
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            return Tensor([self.matrix[i] - other for i in range(self.num_of_el)], self.shape)
        else:
            raise ValueError

    def __mul__(self, other):
        if isinstance(other, Tensor):
            if self.shape == other.shape:
                return Tensor([self.matrix[i] * other.matrix[i] for i in range(self.num_of_el)], self.shape)
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            return Tensor([self.matrix[i] * other for i in range(self.num_of_el)], self.shape)
        else:
            raise ValueError

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            if other == 0:
                raise ZeroDivisionError
            return Tensor([self.matrix[i] / other for i in range(self.num_of_el)], self.shape)
        else:
            raise ValueError

    def __pow__(self, other):
        if isinstance(other, Tensor):
            if self.shape == other.shape:
                return Tensor([self.matrix[i] ** other.matrix[i] for i in range(self.num_of_el)], self.shape)
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            return Tensor([self.matrix[i] ** other for i in range(self.num_of_el)], self.shape)
        else:
            raise ValueError

    def sum(self, axis=None):
        if axis is None:
            return sum(self.matrix)
        else:
            num_new = self.num_of_el // self.shape[axis]
            shape_new = []
            for i in range(self.dim):
                if i != axis:
                    shape_new += [self.shape[i]]
            print(num_new, shape_new)

    def mean(self, axis=None):
        if axis is None:
            return self.sum()/self.num_of_el

    def min(self, axis=None):
        if axis is None:
            return min(self.matrix)

    def max(self, axis=None):
        if axis is None:
            return max(self.matrix)

    def argmax(self, axis=None):
        if axis is None:
            return (self.matrix).index(max(self.matrix))

    def argmin(self, axis=None):
        if axis is None:
            return (self.matrix).index(min(self.matrix))

    def transpose(self, *args):
        pass

    def swapaxes(self, *args):
        pass


'''
    def __matmul__(self, other):
        if isinstance(other, Tensor) and self.shape[-1] == other.shape[0]:
'''


'''
a = Tensor([[[1,2],[3,4]],
            [[5,6],[7,8]]])
b = Tensor([[[5,6],[7,8]],[[1,2],[3,4]]])
c = Tensor([[1,2],[3,4]])
print(a.matrix)
print(b.matrix)
print(a+b)
print(a+1)
print(a[(0,0,0)])
print(a[(0,1,0)])
a[(1,0,1)] = 0
print(a.matrix)
print(c[(0,1)])
print((a+b).matrix)
print(a+1)
print(a-2)
print(a*2)
print((2.5 + a).matrix)
#print(sum(a))
'''
