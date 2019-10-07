#!/usr/bin/env python
# coding: utf-8
from copy import deepcopy

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
    4. Transpose by given axes (by default reverse demensions).
    5. Swap two axes.
    6. Matrix multiplication for tensors with dimension <= 2.
    """

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: list of lists
        """
        self.matrix = deepcopy(init_matrix_representation)
        self.d = self._get_d()
        self._nd = [*range(len(self.d))]

    def _get_d(self):
        if isinstance(self[0], int) or isinstance(self[0], float):
            return [len(self)]
        else:
            return [len(self)] + Tensor._get_d(self[0])

    def _make_operation(self, operation, other):
        if isinstance(other, Tensor):
            if other.d == self.d:
                result = Tensor(self.matrix)
                for ind in it.product(*[range(k) for k in self.d]):
                    if operation == '+':
                        result[ind] = result[ind] + other[ind]
                    elif operation == '-':
                        result[ind] = result[ind] - other[ind]
                    elif operation == '*':
                        result[ind] = result[ind] * other[ind]
                    # elif operation == '/':
                    #     result[ind] = result[ind] / other[ind]
                return result
            else:
                raise ValueError
        elif isinstance(other, int) or isinstance(other, float):
            result = Tensor(self.matrix)
            for ind in it.product(*[range(k) for k in self.d]):
                if operation == '+':
                    result[ind] = result[ind] + other
                elif operation == '-':
                    result[ind] = result[ind] - other
                elif operation == '*':
                    result[ind] = result[ind] * other
                elif operation == '/':
                    result[ind] = result[ind] / other
            return result
        else:
            raise ValueError

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.matrix[key]
        i = 0
        elem = self.matrix[key[i]]
        while i < len(key) - 1:
            i += 1
            elem = elem[key[i]]
        return elem

    def __setitem__(self, key, value):
        if isinstance(key, int):
            return self.matrix[key]
        i = 0
        elem = self.matrix[key[i]]
        while i < len(key) - 2:
            i += 1
            elem = elem[key[i]]
        i += 1
        elem[key[i]] = value

    def __add__(self, other):
        return self._make_operation('+', other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self._make_operation('-', other)

    def __mul__(self, other):
        return self._make_operation('*', other)

    def __matmul__(self, other):
        if isinstance(other, Tensor):
            if (len(other.d) == 1) and (self.d[-1] == other.d[0]):
                return Tensor([sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, other.matrix))
                               for row_a in self.matrix])
            if (len(self.d) <= 2) and (len(self.d) <= 2) and \
                    (self.d[-1] == other.d[0]):
                a = deepcopy(self.matrix)
                b = deepcopy(other.matrix)
                if not isinstance(b[0], list):
                    zip_b = zip(*[b])
                else:
                    zip_b = zip(*b)
                zip_b = list(zip_b)
                if not isinstance(a[0], list):
                    a = [a]
                r = [[sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b))
                      for col_b in zip_b] for row_a in a]
                if len(r) == 1:
                    r = r[0]
                return Tensor(r)
            else:
                raise ValueError
        else:
            raise ValueError

    def __truediv__(self, other):
        return self._make_operation('/', other)

    def __pow__(self, pow):
        result = deepcopy(self)
        for _ in range(pow - 1):
            result = result._make_operation('*', self)
        return result

    # def transpose(self, *axis):
    #     pass

    def rebuild(self, new_nd):
        if new_nd == self._nd:
            return
        self._nd = new_nd
        d = self.d.copy()
        for nm, el in enumerate(self._nd):
            self.d[nm] = d[el]
        _nmatrix = []
        for i in self.d[::-1]:
            if not _nmatrix:
                _nmatrix = [0 for _ in range(i)]
            else:
                _nmatrix = [deepcopy(_nmatrix) for _ in range(i)]

        t = Tensor(_nmatrix)
        for ind in it.product(*[range(k) for k in d]):
            ind1 = [0 for _ in range(len(ind))]
            for nm, el in enumerate(ind):
                ind1[self._nd.index(nm)] = el
            t[ind1] = self.__getitem__(ind)
        self.matrix = t.matrix

    def transpose(self, *axes):
        if len(axes) != len(self.d):
            raise ValueError
        else:
            t = Tensor(self.matrix)
            t.rebuild(axes)
            return t

    def swapaxes(self, first, second):
        if first == second:
            return self
        else:
            axes = self._nd
            axes[axes.index(first)], axes[axes.index(second)] = second, first
            t = Tensor(self.matrix)
            t.rebuild(axes)
            return t

    def __len__(self):
        return len(self.matrix)

    def __str__(self):
        s = ''
        for i in range(len(self)):
            if not isinstance(self[i], list):
                s += str(self[i]) + ' '
                continue
            for j in range(len(self[i])):
                s += str(self[i][j]) + ' '
            s += '\n'
        return s

    def _dimmult(self, ret_list, prod):
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
            if len(self.d) > axis >= 0:
                ret_list = []
                prod = [range(k) for k in self.d[0:axis]]
                prod.extend(range(k) for k in self.d[axis + 1:])
                for ind in it.product(*prod):
                    sm = 0
                    for i in range(self.d[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        sm += self.__getitem__(ind)
                        ind = list(ind)
                        ind.pop(axis)
                    ret_list.append(sm)
                prod = self.d[:axis] + self.d[axis + 1:]
                return Tensor(self._dimmult(ret_list, prod))
            else:
                raise ValueError
        else:
            sm = 0
            for ind in it.product(*[range(k) for k in self.d]):
                sm += self.__getitem__(ind)
            return sm

    def mean(self, axis=None):
        if axis:
            if len(self.d) > axis >= 0:
                ret_list = []
                prod = [range(k) for k in self.d[0:axis]]
                prod.extend(range(k) for k in self.d[axis + 1:])
                for ind in it.product(*prod):
                    sm = 0
                    nm = 0
                    for i in range(self.d[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        sm += self.__getitem__(ind)
                        nm += 1
                        ind = list(ind)
                        ind.pop(axis)
                    ret_list.append(sm / nm)
                prod = self.d[:axis] + self.d[axis + 1:]
                return Tensor(self._dimmult(ret_list, prod))
            else:
                raise ValueError
        else:
            sm = 0
            num = 0
            for ind in it.product(*[range(k) for k in self.d]):
                sm += self.__getitem__(ind)
                num += 1
            return sm / num

    def min(self, axis=None):
        if axis:
            if len(self.d) > axis >= 0:
                ret_list = []
                prod = [range(k) for k in self.d[0:axis]]
                prod.extend(range(k) for k in self.d[axis + 1:])
                for ind in it.product(*prod):
                    mn = None
                    for i in range(self.d[axis]):
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
                prod = self.d[:axis] + self.d[axis + 1:]
                return Tensor(self._dimmult(ret_list, prod))
            else:
                raise ValueError
        else:
            mn = None
            for ind in it.product(*[range(k) for k in self.d]):
                if not mn:
                    mn = self.__getitem__(ind)
                mn = min(mn, self.__getitem__(ind))
            return mn

    def max(self, axis=None):
        if axis:
            if len(self.d) > axis >= 0:
                ret_list = []
                prod = [range(k) for k in self.d[0:axis]]
                prod.extend(range(k) for k in self.d[axis + 1:])
                for ind in it.product(*prod):
                    mx = None
                    for i in range(self.d[axis]):
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
                prod = self.d[:axis] + self.d[axis + 1:]
                return Tensor(self._dimmult(ret_list, prod))
            else:
                raise ValueError
        else:
            mx = None
            for ind in it.product(*[range(k) for k in self.d]):
                if not mx:
                    mx = self.__getitem__(ind)
                mx = max(mx, self.__getitem__(ind))
            return mx

    def argmin(self, axis=None):
        if axis:
            if len(self.d) > axis >= 0:
                ret_list = []
                prod = [range(k) for k in self.d[0:axis]]
                prod.extend(range(k) for k in self.d[axis + 1:])
                for ind in it.product(*prod):
                    mn = None
                    for i in range(self.d[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        if not mn:
                            mn = self.__getitem__(ind)
                        else:
                            mn = min(mn, self.__getitem__(ind))
                        ind = list(ind)
                        ind.pop(axis)
                    for i in range(self.d[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        if self.__getitem__(ind) == mn:
                            mn = (mn, i)
                        ind = list(ind)
                        ind.pop(axis)
                    ret_list.append(mn[1])
                prod = self.d[:axis] + self.d[axis + 1:]
                return Tensor(self._dimmult(ret_list, prod))
            else:
                raise ValueError
        else:
            mn = None
            for ind in it.product(*[range(k) for k in self.d]):
                if not mn:
                    mn = self.__getitem__(ind)
                mn = min(mn, self.__getitem__(ind))
            for nm, ind in enumerate(it.product(*[range(k) for k in self.d])):
                if self.__getitem__(ind) == mn:
                    mn = nm
                    break
            return mn

    def argmax(self, axis=None):
        if axis:
            if len(self.d) > axis >= 0:
                ret_list = []
                prod = [range(k) for k in self.d[0:axis]]
                prod.extend(range(k) for k in self.d[axis + 1:])
                for ind in it.product(*prod):
                    mx = None
                    for i in range(self.d[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        if not mx:
                            mx = self.__getitem__(ind)
                        else:
                            mx = max(mx, self.__getitem__(ind))
                        ind = list(ind)
                        ind.pop(axis)
                    for i in range(self.d[axis]):
                        ind = list(ind)
                        ind.insert(axis, i)
                        ind = tuple(ind)
                        if self.__getitem__(ind) == mx:
                            mx = (mx, i)
                            break
                        ind = list(ind)
                        ind.pop(axis)
                    ret_list.append(mx[1])
                prod = self.d[:axis] + self.d[axis + 1:]
                return Tensor(self._dimmult(ret_list, prod))
            else:
                raise ValueError
        else:
            mx = None
            for ind in it.product(*[range(k) for k in self.d]):
                if not mx:
                    mx = self.__getitem__(ind)
                mx = max(mx, self.__getitem__(ind))
            for nm, ind in enumerate(it.product(*[range(k) for k in self.d])):
                if self.__getitem__(ind) == mx:
                    mx = nm
                    break
            return mx
