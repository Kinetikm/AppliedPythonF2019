#!/usr/bin/env python
# coding: utf-8


class Tensor:
    """
    Your realisation of numpy tensor.

    Must be implemented:
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

    def shape_calc(matrix):
        shape = [len(matrix)]
        axis = matrix[0]
        while isinstance(axis, list):
            shape += [len(axis)]
            axis = axis[0]
        return shape

    def __init__(self, init_matrix_representation):
        self.matrix = init_matrix_representation
        self.shape = Tensor.shape_calc(self.matrix)
        self.dim = len(self.shape)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.matrix[item]
        elif isinstance(item, tuple):
            result = self.matrix[item[0]]
            i = 1
            while isinstance(result, list):
                result = result[item[i]]
                i += 1
            return result

    def __setitem__(self, ind, value):
        if isinstance(ind, int):
            self.matrix[ind] = value
        elif isinstance(ind, tuple):
            result = self.matrix[ind[0]]
            i = 1
            while isinstance(result, list):
                if not isinstance(result[ind[i]], list):
                    result[ind[i]] = value
                result = result[ind[i]]
                i += 1

    def matrix_base(first, second, operation):
        if len(Tensor.shape_calc(first)) == 1:
            if operation == 'add':
                return [first[i] + second[i] for i in range(Tensor.shape_calc(first)[0])]
            elif operation == 'sub':
                return [first[i] - second[i] for i in range(Tensor.shape_calc(first)[0])]
            elif operation == 'mul':
                return [first[i] * second[i] for i in range(Tensor.shape_calc(first)[0])]
            elif operation == 'div':
                return [first[i] / second[i] for i in range(Tensor.shape_calc(first)[0])]
            elif operation == 'pow':
                return [first[i] ** second[i] for i in range(Tensor.shape_calc(first)[0])]
        else:
            return [Tensor.matrix_base(first[i], second[i], operation) for i in range(Tensor.shape_calc(first)[0])]


    def __add__(self, other):
        if isinstance(other, Tensor):
            if self.shape == other.shape:
                return Tensor(Tensor.matrix_base(self.matrix, other.matrix, 'add'))
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            print(self.shape)
            const_matrix = [other for i in range(self.shape[-1])]
            for dim in range(self.dim - 1)[::-1]:
                const_matrix = [const_matrix for i in range(self.shape[dim])]
            print(Tensor.shape_calc(const_matrix))
            return Tensor(Tensor.matrix_base(self.matrix, const_matrix, 'add'))
        else:
            raise ValueError

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Tensor):
            if self.shape == other.shape:
                return Tensor(Tensor.matrix_base(self.matrix, other.matrix, 'sub'))
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            const_matrix = [other for i in range(self.shape[-1])]
            for dim in range(self.dim - 1)[::-1]:
                const_matrix = [const_matrix for i in range(self.shape[dim])]
            return Tensor(Tensor.matrix_base(self.matrix, const_matrix, 'sub'))
        else:
            raise ValueError

    def __mul__(self, other):
        if isinstance(other, Tensor):
            if self.shape == other.shape:
                return Tensor(Tensor.matrix_base(self.matrix, other.matrix, 'mul'))
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            const_matrix = [other for i in range(self.shape[-1])]
            for dim in range(self.dim - 1)[::-1]:
                const_matrix = [const_matrix for i in range(self.shape[dim])]
            return Tensor(Tensor.matrix_base(self.matrix, const_matrix, 'mul'))
        else:
            raise ValueError

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            if other == 0:
                raise ZeroDivisionError
            const_matrix = [other for i in range(self.shape[-1])]
            for dim in range(self.dim - 1)[::-1]:
                const_matrix = [const_matrix for i in range(self.shape[dim])]
            return Tensor(Tensor.matrix_base(self.matrix, const_matrix, 'div'))
        else:
            raise ValueError

    def __pow__(self, other):
        if isinstance(other, Tensor):
            if self.shape == other.shape:
                return Tensor(Tensor.matrix_base(self.matrix, other.matrix, 'pow'))
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            const_matrix = [other for i in range(self.shape[-1])]
            for dim in range(self.dim - 1)[::-1]:
                const_matrix = [const_matrix for i in range(self.shape[dim])]
            return Tensor(Tensor.matrix_base(self.matrix, const_matrix, 'pow'))
        else:
            raise ValueError


a = Tensor([[[1,2],[3,4]],[[5,6],[7,8]]])
b = Tensor([[[5,6],[7,8]],[[1,2],[3,4]]])
print((a+b).matrix)
print(a+1)
print(a-2)
print(a*2)
print((2.5 + a).matrix)


