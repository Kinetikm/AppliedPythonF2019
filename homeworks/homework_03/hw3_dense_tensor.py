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
        self.size = self.get_size(init_matrix_representation)
        self.new_size = self.newsize()
        self.tensor = self.init(init_matrix_representation, self.size)
        self.ord = [i for i in range(len(self.size))]

    def init(self, lst, size):
        l = []
        for i in product(*[range(k) for k in size[:-1]]):
            l += self.get(lst, 0, i)
        return l

    def newsize(self):
        lst = [1]
        for i in self.size[::-1]:
            lst.append(lst[-1] * i)
        return lst[:-1:][::-1]

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.tensor[key]
        new_key = tuple([key[self.ord[i]] for i in range(len(key))])
        ind = sum([self.new_size[i] * new_key[i] for i in range(len(self.size))])
        return self.tensor[ind]

    def get(self, lst, lvl, count):
        try:
            len(count)
        except:
            return lst[count]
        else:
            if len(count) == lvl:
                return lst
            else:
                temp = self.get(lst[count[lvl]], lvl + 1, count)
            return temp

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.tensor[key] = value
            return
        new_key = tuple([key[self.ord[i]] for i in range(len(key))])
        ind = sum([self.new_size[i] * new_key[i] for i in range(len(self.size))])
        self.tensor[ind] = value

    def get_size(self, lst):
        size = []
        self.getsize(lst, size)
        return list(size)

    def getsize(self, lst, size):
        try:
            len(lst)
        except TypeError:
            return
        else:
            size.append(len(lst))
            self.getsize(lst[0], size)

    def __add__(self, other):
        if self.size != other.size:
            raise ValueError
        temp = deepcopy(self)
        for i in product(*[range(k) for k in temp.size]):
            if isinstance(other, Tensor):
                temp[i] += other[i]
            else:
                temp[i] += other
        return temp

    def __radd__(self, other):
        temp = deepcopy(self)
        for i in product(*[range(k) for k in temp.size]):
            temp[i] += other
        return temp

    def __sub__(self, other):
        temp = deepcopy(self)
        for i in product(*[range(k) for k in temp.size]):
            if isinstance(other, Tensor):
                temp[i] -= other[i]
            else:
                temp[i] -= other
        return temp

    def __mul__(self, other):
        temp = deepcopy(self)
        for i in product(*[range(k) for k in temp.size]):
            if isinstance(other, Tensor):
                temp[i] *= other[i]
            else:
                temp[i] *= other
        return temp

    def __truediv__(self, other):
        if not isinstance(other, Tensor) and other == 0:
            raise ZeroDivisionError
        temp = deepcopy(self)
        for i in product(*[range(k) for k in temp.size]):
            if isinstance(other, Tensor):
                if other[i] == 0:
                    raise ZeroDivisionError
                temp[i] /= other[i]
            else:
                temp[i] /= other
        return temp

    def __pow__(self, other):
        temp = deepcopy(self)
        for i in product(*[range(k) for k in temp.size]):
            if isinstance(other, Tensor):
                temp[i] **= other[i]
            else:
                temp[i] **= other
        return temp

    def mean(self, axis=None):
        sum = 0
        if axis is None:
            for i in range(len(self.tensor)):
                sum += self.tensor[i]
            return sum / len(self.tensor)
        elif 1:
            new = Tensor([0])
            new.size = [self.size[i] for i in range(len(self.size)) if i != axis]
            size = 1
            new.new_size = new.newsize()
            for i in new.size:
                size *= i
            new.tensor = [0 for i in range(size)]
            new.ord = [i for i in range(len(new.size))]
            for i in product(*[range(k) for k in self.size]):
                new[i[0:axis] + i[axis+1:]] += self[i]
            for i in product(*[range(k) for k in new.size]):
                new[i] /= self.size[axis]
            return new

    def sum(self, axis=None):
        sum = 0
        if axis is None:
            for i in range(len(self.tensor)):
                sum += self.tensor[i]
            return sum
        elif 1:
            new = Tensor([0])
            new.size = [self.size[i] for i in range(len(self.size)) if i != axis]
            size = 1
            new.new_size = new.newsize()
            for i in new.size:
                size *= i
            new.tensor = [0 for i in range(size)]
            new.ord = [i for i in range(len(new.size))]
            for i in product(*[range(k) for k in self.size]):
                new[i[0:axis] + i[axis+1:]] += self[i]
            return new

    def max(self, axis=None):
        max_val = min(self.tensor)
        if axis is None:
            for i in range(len(self.tensor)):
                if self.tensor[i] > max_val:
                    max_val = self.tensor[i]
            return max_val
        elif 1:
            new = Tensor([0])
            new.size = [self.size[i] for i in range(len(self.size)) if i != axis]
            size = 1
            new.new_size = new.newsize()
            for i in new.size:
                size *= i
            new.tensor = [max_val for i in range(size)]
            new.ord = [i for i in range(len(new.size))]
            for i in product(*[range(k) for k in self.size]):
                if new[i[0:axis] + i[axis+1:]] < self[i]:
                    new[i[0:axis] + i[axis+1:]] = self[i]
            return new

    def min(self, axis=None):
        min_val = max(self.tensor)
        if axis is None:
            for i in range(len(self.tensor)):
                if self.tensor[i] < min_val:
                    min_val = self.tensor[i]
            return min_val
        elif 1:
            new = Tensor([0])
            new.size = [self.size[i] for i in range(len(self.size)) if i != axis]
            size = 1
            new.new_size = new.newsize()
            for i in new.size:
                size *= i
            new.tensor = [min_val for i in range(size)]
            new.ord = [i for i in range(len(new.size))]
            for i in product(*[range(k) for k in self.size]):
                if new[i[0:axis] + i[axis+1:]] > self[i]:
                    new[i[0:axis] + i[axis+1:]] = self[i]
            return new

    def argmax(self, axis=None):
        max_val = min(self.tensor)
        max_ind = 0
        if axis is None:
            for i in range(len(self.tensor)):
                if self.tensor[i] > max_val:
                    max_val = self.tensor[i]
                    max_ind = i
            return max_ind
        elif 1:
            new = Tensor([0])
            new.size = [self.size[i] for i in range(len(self.size)) if i != axis]
            size = 1
            new.new_size = new.newsize()
            for i in new.size:
                size *= i
            new.tensor = [max_val for i in range(size)]
            new.ord = [i for i in range(len(new.size))]
            new1 = deepcopy(new)
            for i in product(*[range(k) for k in self.size]):
                if new[i[0:axis] + i[axis+1:]] < self[i]:
                    new[i[0:axis] + i[axis+1:]] = self[i]
                    new1[i[0:axis] + i[axis+1:]] = i[axis]
            return new1

    def argmin(self, axis=None):
        min_val = max(self.tensor)
        min_ind = 0
        if axis is None:
            for i in range(len(self.tensor)):
                if self.tensor[i] < min_val:
                    min_val = self.tensor[i]
                    min_ind = i
            return min_ind
        elif 1:
            new = Tensor([0])
            new.size = [self.size[i] for i in range(len(self.size)) if i != axis]
            size = 1
            new.new_size = new.newsize()
            for i in new.size:
                size *= i
            new.tensor = [min_val for i in range(size)]
            new.ord = [i for i in range(len(new.size))]
            new1 = deepcopy(new)
            for i in product(*[range(k) for k in self.size]):
                if new[i[0:axis] + i[axis+1:]] > self[i]:
                    new[i[0:axis] + i[axis+1:]] = self[i]
                    new1[i[0:axis] + i[axis+1:]] = i[axis]
            return new1

    def transpose(self, *new_ord):
        new = Tensor([0])
        new.tensor = self.tensor
        new.ord = deepcopy(self.ord)
        new.size = deepcopy(self.size)
        new.new_size = deepcopy(self.new_size)
        new.ord = list(new_ord)[::-1]
        return new

    def swapaxes(self, i, j):
        new = Tensor([0])
        new.tensor = self.tensor
        new.ord = deepcopy(self.ord)
        new.size = deepcopy(self.size)
        new.new_size = deepcopy(self.new_size)
        new.ord[i], new.ord[j] = new.ord[j], new.ord[i]
        return new

    def __matmul__(self, other):
        temp = None
        if len(self.size) == 1 and len(other.size) == 1 and other.size[0] == self.size[0]:
            temp = 0
            for i in range(self.size[0]):
                temp += self[i]*other[i]
        elif len(self.size) == 2 and len(other.size) == 2 and other.size[0] == self.size[1]:
            temp = Tensor([[0 for i in range(other.size[1])] for j in range(self.size[0])])
            for i in range(self.size[0]):
                for j in range(other.size[1]):
                    for k in range(self.size[1]):
                        temp[i, j] = temp[i, j] + self[i, k]*other[k, j]
        elif len(self.size) == 2 and len(other.size) == 1 and other.size[0] == self.size[1]:
            temp = Tensor([0 for i in range(self.size[0])])
            for i in range(self.size[0]):
                for j in range(other.size[0]):
                    temp[i] += self[i, j] * other[j]
        elif len(self.size) == 1 and len(other.size) == 2 and other.size[0] == self.size[0]:
            temp = Tensor([0 for i in range(other.size[1])])
            for i in range(other.size[1]):
                for j in range(other.size[0]):
                    temp[i] += self[j]*other[j, i]
        if temp is None:
            raise ValueError
        return temp
