#!/usr/bin/env python
# coding: utf-8
import numpy as np
import itertools
import copy


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
        self._matrix = copy.deepcopy(init_matrix_representation)
        self.dims = self.get_dims(self._matrix)
        self._flat_matr = self.flatten(self._matrix)
        self._ndims = [*range(len(self.dims))]

    def rebuild(self, new_ndims):
        if new_ndims == self._ndims:
            return
        self._ndims = new_ndims
        dims = self.dims.copy()
        for nm, el in enumerate(self._ndims):
            self.dims[nm] = dims[el]
        _nmatrix = []
        for i in self.dims[::-1]:
            if not _nmatrix:
                _nmatrix = [0 for _ in range(i)]
            else:
                _nmatrix = [copy.deepcopy(_nmatrix) for _ in range(i)]

        t = Tensor(_nmatrix)
        for ind in itertools.product(*[range(k) for k in dims]):
            ind1 = [0 for _ in range(len(ind))]
            for nm, el in enumerate(ind):
                ind1[self._ndims.index(nm)] = el
            t[ind1] = self.__getitem__(ind)
        self._matrix = t._matrix

    @staticmethod
    def flatten(l):
        return Tensor.flatten(l[0]) + (Tensor.flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]

    @staticmethod
    def get_dims(matr):
        if isinstance(matr[0], int) or isinstance(matr[0], float):
            return [len(matr)]
        else:
            return [len(matr)] + Tensor.get_dims(matr[0])

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._matrix[item]
        if len(item) == len(self.dims):
            it = self._matrix
            for i in item:
                it = it[i]
            return it
        else:
            raise IndexError

    def __setitem__(self, key, value):
        if len(key) == len(self.dims):
            it = self._matrix
            for i in key[:-1]:
                it = it[i]
            it[key[-1]] = value
        else:
            raise IndexError

    def __add__(self, other):
        if isinstance(other, Tensor):
            if other.dims == self.dims:
                nm = Tensor(self._matrix)
                for ind in itertools.product(*[range(k) for k in self.dims]):
                    nm[ind] = nm[ind] + other[ind]
                return nm
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            nm = Tensor(self._matrix)
            for ind in itertools.product(*[range(k) for k in self.dims]):
                nm[ind] = nm[ind] + other
            return nm
        else:
            raise ValueError

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Tensor):
            if other.dims == self.dims:
                nm = Tensor(self._matrix)
                for ind in itertools.product(*[range(k) for k in self.dims]):
                    nm[ind] = nm[ind] - other[ind]
                return nm
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            nm = Tensor(self._matrix)
            for ind in itertools.product(*[range(k) for k in self.dims]):
                nm[ind] = nm[ind] - other
            return nm
        else:
            raise ValueError

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, Tensor):
            if other.dims == self.dims:
                nm = Tensor(self._matrix)
                for ind in itertools.product(*[range(k) for k in self.dims]):
                    nm[ind] = nm[ind] * other[ind]
                return nm
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            nm = Tensor(self._matrix)
            for ind in itertools.product(*[range(k) for k in self.dims]):
                nm[ind] = nm[ind] * other
            return nm
        else:
            raise ValueError

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Tensor):
            if other.dims == self.dims:
                nm = Tensor(self._matrix)
                for ind in itertools.product(*[range(k) for k in self.dims]):
                    nm[ind] = nm[ind] / other[ind]
                return nm
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            if int(other) == 0:
                raise ZeroDivisionError
            nm = Tensor(self._matrix)
            for ind in itertools.product(*[range(k) for k in self.dims]):
                nm[ind] = nm[ind] / other
            return nm
        else:
            raise ValueError

    def __pow__(self, power, modulo=None):
        nm = Tensor(self._matrix)
        for ind in itertools.product(*[range(k) for k in self.dims]):
            nm[ind] = nm[ind] ** power
        return nm

    def __matmul__(self, other):
        if isinstance(other, Tensor):
            if (len(other.dims) == 1) and (self.dims[-1] == other.dims[0]):
                return Tensor([sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, other._matrix))
                               for row_a in self._matrix])
            if (len(self.dims) <= 2) and (len(self.dims) <= 2) and (self.dims[-1] == other.dims[0]):
                a = copy.deepcopy(self._matrix)
                b = copy.deepcopy(other._matrix)
                if not isinstance(b[0], list):
                    zip_b = zip(*[b])
                else:
                    zip_b = zip(*b)
                zip_b = list(zip_b)
                if not isinstance(a[0], list):
                    a = [a]
                r = [[sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b)) for col_b in zip_b] for row_a in a]
                if len(r) == 1:
                    r = r[0]
                return Tensor(r)
            else:
                raise ValueError
        else:
            raise ValueError

    @staticmethod
    def make_multidim(ret_list, prod):
        ret_list_list = []
        for i in prod[::-1]:
            nums = len(ret_list) // i
            it = 0
            while it < nums:
                ret_list_list.append(ret_list[it * i: (it + 1) * i])
                it += 1
            ret_list = ret_list_list.copy()
            ret_list_list.clear()
        return ret_list[0]

    def sum(self, axis=None):
        if axis:
            if len(self.dims) > axis >= 0:
                ret_list = []
                prod = [range(k) for k in self.dims[0:axis]]
                prod.extend(range(k) for k in self.dims[axis + 1:])
                for ind in itertools.product(*prod):
                    sm = 0
                    for i in range(self.dims[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        sm += self.__getitem__(ind)
                        ind = list(ind)
                        ind.pop(axis)
                    ret_list.append(sm)
                prod = self.dims[:axis] + self.dims[axis + 1:]
                return Tensor(self.make_multidim(ret_list, prod))
            else:
                raise ValueError
        else:
            sm = 0
            for ind in itertools.product(*[range(k) for k in self.dims]):
                sm += self.__getitem__(ind)
            return sm

    def mean(self, axis=None):
        if axis:
            if len(self.dims) > axis >= 0:
                ret_list = []
                prod = [range(k) for k in self.dims[0:axis]]
                prod.extend(range(k) for k in self.dims[axis + 1:])
                for ind in itertools.product(*prod):
                    sm = 0
                    nm = 0
                    for i in range(self.dims[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        sm += self.__getitem__(ind)
                        nm += 1
                        ind = list(ind)
                        ind.pop(axis)
                    ret_list.append(sm / nm)
                prod = self.dims[:axis] + self.dims[axis + 1:]
                return Tensor(self.make_multidim(ret_list, prod))
            else:
                raise ValueError
        else:
            sm = 0
            num = 0
            for ind in itertools.product(*[range(k) for k in self.dims]):
                sm += self.__getitem__(ind)
                num += 1
            return sm / num

    def min(self, axis=None):
        if axis:
            if len(self.dims) > axis >= 0:
                ret_list = []
                prod = [range(k) for k in self.dims[0:axis]]
                prod.extend(range(k) for k in self.dims[axis + 1:])
                for ind in itertools.product(*prod):
                    mn = None
                    for i in range(self.dims[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        if not mn:
                            mn = self.__getitem__(ind)
                        else:
                            mn = min(mn, self.__getitem__(ind))
                        ind = list(ind)
                        ind.pop(axis)
                    ret_list.append(mn)
                prod = self.dims[:axis] + self.dims[axis + 1:]
                return Tensor(self.make_multidim(ret_list, prod))
            else:
                raise ValueError
        else:
            mn = None
            for ind in itertools.product(*[range(k) for k in self.dims]):
                if not mn:
                    mn = self.__getitem__(ind)
                mn = min(mn, self.__getitem__(ind))
            return mn

    def max(self, axis=None):
        if axis:
            if len(self.dims) > axis >= 0:
                ret_list = []
                prod = [range(k) for k in self.dims[0:axis]]
                prod.extend(range(k) for k in self.dims[axis + 1:])
                for ind in itertools.product(*prod):
                    mx = None
                    for i in range(self.dims[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        if not mx:
                            mx = self.__getitem__(ind)
                        else:
                            mx = max(mx, self.__getitem__(ind))
                        ind = list(ind)
                        ind.pop(axis)
                    ret_list.append(mx)
                prod = self.dims[:axis] + self.dims[axis + 1:]
                return Tensor(self.make_multidim(ret_list, prod))
            else:
                raise ValueError
        else:
            mx = None
            for ind in itertools.product(*[range(k) for k in self.dims]):
                if not mx:
                    mx = self.__getitem__(ind)
                mx = max(mx, self.__getitem__(ind))
            return mx

    def argmin(self, axis=None):
        if axis:
            if len(self.dims) > axis >= 0:
                ret_list = []
                prod = [range(k) for k in self.dims[0:axis]]
                prod.extend(range(k) for k in self.dims[axis + 1:])
                for ind in itertools.product(*prod):
                    mn = None
                    for i in range(self.dims[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        if not mn:
                            mn = self.__getitem__(ind)
                        else:
                            mn = min(mn, self.__getitem__(ind))
                        ind = list(ind)
                        ind.pop(axis)
                    for i in range(self.dims[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        if self.__getitem__(ind) == mn:
                            mn = (mn, i)
                        ind = list(ind)
                        ind.pop(axis)
                    ret_list.append(mn[1])
                prod = self.dims[:axis] + self.dims[axis + 1:]
                return Tensor(self.make_multidim(ret_list, prod))
            else:
                raise ValueError
        else:
            mn = None
            for ind in itertools.product(*[range(k) for k in self.dims]):
                if not mn:
                    mn = self.__getitem__(ind)
                mn = min(mn, self.__getitem__(ind))
            for nm, ind in enumerate(itertools.product(*[range(k) for k in self.dims])):
                if self.__getitem__(ind) == mn:
                    mn = nm
                    break
            return mn

    def argmax(self, axis=None):
        if axis:
            if len(self.dims) > axis >= 0:
                ret_list = []
                prod = [range(k) for k in self.dims[0:axis]]
                prod.extend(range(k) for k in self.dims[axis + 1:])
                for ind in itertools.product(*prod):
                    mx = None
                    for i in range(self.dims[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        if not mx:
                            mx = self.__getitem__(ind)
                        else:
                            mx = max(mx, self.__getitem__(ind))
                        ind = list(ind)
                        ind.pop(axis)
                    for i in range(self.dims[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        if self.__getitem__(ind) == mx:
                            mx = (mx, i)
                            break
                        ind = list(ind)
                        ind.pop(axis)
                    ret_list.append(mx[1])
                prod = self.dims[:axis] + self.dims[axis + 1:]
                return Tensor(self.make_multidim(ret_list, prod))
            else:
                raise ValueError
        else:
            mx = None
            for ind in itertools.product(*[range(k) for k in self.dims]):
                if not mx:
                    mx = self.__getitem__(ind)
                mx = max(mx, self.__getitem__(ind))
            for nm, ind in enumerate(itertools.product(*[range(k) for k in self.dims])):
                if self.__getitem__(ind) == mx:
                    mx = nm
                    break
            return mx

    def transpose(self, *axes):
        if len(axes) != len(self.dims):
            raise ValueError
        else:
            t = Tensor(self._matrix)
            t.rebuild(axes)
            return t

    def swapaxes(self, first, second):
        if first == second:
            return self
        else:
            axes = self._ndims
            axes[axes.index(first)], axes[axes.index(second)] = second, first
            t = Tensor(self._matrix)
            t.rebuild(axes)
            return t
