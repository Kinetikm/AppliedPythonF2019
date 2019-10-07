#!/usr/bin/env python
# coding: utf-8
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

    @staticmethod
    def __getshape__(lol):
        try:
            ln = len(lol)
        except TypeError:
            return None
        else:
            r = Tensor.__getshape__(lol[0])
            if r is None:
                r = []
                r.insert(0, ln)
            else:
                r.insert(0, ln)
            return r

    @staticmethod
    def __tolist__(lol, sh):
        page = []
        for i in range(sh[0]):
            if len(sh) == 1:
                return lol
            page += Tensor.__tolist__(lol[i], sh[1::])
        return page

    @staticmethod
    def __tomatrix__(listik, sh):
        matrix = []
        elements = 1
        for i in sh:
            elements *= i
        if elements != len(listik):
            return None
        for i in range(sh[0]):
            if len(sh) == 1:
                return listik
            k = len(listik) // sh[0]
            temp = listik[i * k:(i + 1) * k]
            temp = Tensor.__tomatrix__(temp, sh[1::])
            matrix.append(temp)
        return matrix

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: list of lists
        """
        self.__shape = self.__getshape__(init_matrix_representation)
        self.shape = tuple(self.__shape)
        self.__list = self.__tolist__(init_matrix_representation, self.__shape)

    @staticmethod
    def __givekoord__(shape, pos):
        koord = []
        temp = 1
        for i in range(1, len(shape)):
            temp *= shape[i]
        for j in range(1, len(shape)):
            koord.append(pos // temp)
            pos %= temp
            temp //= shape[j]
        koord.append(pos % shape[len(shape) - 1])
        return koord

    @staticmethod
    def __fromkoord__(shape, koord):
        temp = 1
        pos = 0
        for i in range(1, len(shape)):
            temp *= shape[i]
        for j in range(1, len(shape)):
            pos += temp * koord[j - 1]
            temp //= shape[j]
        pos += koord[len(koord) - 1]
        return (pos)

    def __getitem__(self, item):
        try:
            koord = list(item)
        except TypeError:
            koord = []
            if type(item) != int:
                raise IndexError
            koord.append(item)
        if len(koord) > len(self.__shape):
            raise IndexError
        if len(koord) == 0:
            raise IndexError
        if len(koord) < len(self.__shape):
            for i in range(len(koord)):
                if type(koord[i]) != int:
                    raise IndexError
                if koord[i] >= self.__shape[i]:
                    raise IndexError
            return Tensor(self.__tomatrix__(self.__list, self.__shape).__getitem__(item))
        for i in range(len(self.__shape)):
            if type(koord[i]) != int:
                raise IndexError
            if koord[i] >= self.__shape[i]:
                raise IndexError
        pos = self.__fromkoord__(self.__shape, koord)
        return self.__list[pos]

    def __setitem__(self, key, value):
        koord = list(key)
        if len(koord) != len(self.__shape):
            raise IndexError
        for i in range(len(self.__shape)):
            if type(koord[i]) != int:
                raise IndexError
            if koord[i] >= self.__shape[i]:
                raise IndexError

        pos = self.__fromkoord__(self.__shape, koord)
        self.__list[pos] = value

    def __add__(self, other):
        newlist = []
        if (type(other) == int) or (type(other) == float):
            for i in range(len(self.__list)):
                newlist.append(self.__list[i] + other)
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        if type(self) == type(other):
            if self.__shape != other.__shape:
                raise ValueError
            for i in range(len(self.__list)):
                newlist.append(self.__list[i] + other.__list[i])
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        raise TypeError

    def __sub__(self, other):
        newlist = []
        if (type(other) == int) or (type(other) == float):
            for i in range(len(self.__list)):
                newlist.append(self.__list[i] - other)
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        if type(self) == type(other):
            if self.__shape != other.__shape:
                raise ValueError
            for i in range(len(self.__list)):
                newlist.append(self.__list[i] - other.__list[i])
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        raise TypeError

    def __mul__(self, other):
        newlist = []
        if (type(other) == int) or (type(other) == float):
            for i in range(len(self.__list)):
                newlist.append(self.__list[i] * other)
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        if type(self) == type(other):
            if self.__shape != other.__shape:
                raise ValueError
            for i in range(len(self.__list)):
                newlist.append(self.__list[i] * other.__list[i])
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        raise TypeError

    def __truediv__(self, other):
        newlist = []
        if (type(other) == int) or (type(other) == float):
            for i in range(len(self.__list)):
                if other == 0:
                    raise ZeroDivisionError
                newlist.append(self.__list[i] / other)
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        if type(self) == type(other):
            if self.__shape != other.__shape:
                raise ValueError
            for i in range(len(self.__list)):
                if other.__list[i] == 0:
                    raise ZeroDivisionError
                newlist.append(self.__list[i] / other.__list[i])
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        raise TypeError

    def __radd__(self, other):
        newlist = []
        if (type(other) == int) or (type(other) == float):
            for i in range(len(self.__list)):
                newlist.append(self.__list[i] + other)
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        raise TypeError

    def __rsub__(self, other):
        newlist = []
        if (type(other) == int) or (type(other) == float):
            for i in range(len(self.__list)):
                newlist.append(-self.__list[i] + other)
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        raise TypeError

    def __rmul__(self, other):
        newlist = []
        if (type(other) == int) or (type(other) == float):
            for i in range(len(self.__list)):
                newlist.append(self.__list[i] * other)
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        raise TypeError

    def __rtruediv__(self, other):
        newlist = []
        if (type(other) == int) or (type(other) == float):
            for i in range(len(self.__list)):
                if self.__list[i] == 0:
                    raise ZeroDivisionError
                newlist.append(other / self.__list[i])
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        raise TypeError

    def __pow__(self, other):
        newlist = []
        if (type(other) == int) or (type(other) == float):
            for i in range(len(self.__list)):
                newlist.append(self.__list[i] ** other)
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        if type(self) == type(other):
            if self.__shape != other.__shape:
                raise ValueError
            for i in range(len(self.__list)):
                newlist.append(self.__list[i] ** other.__list[i])
            return Tensor(self.__tomatrix__(newlist, self.__shape))
        raise TypeError

    def __matmul__(self, other):
        if type(self) == type(other):
            if (len(self.__shape) <= 2) and (len(other.__shape) <= 2):
                if len(self.__shape) == 1:
                    sh1 = list(self.shape)
                    sh1.insert(0, 1)
                    matrix1 = self.__tomatrix__(self.__list, sh1)
                else:
                    sh1 = sh1 = list(self.shape)
                    matrix1 = self.__tomatrix__(self.__list, self.__shape)

                if len(other.__shape) == 1:
                    sh2 = list(other.shape)
                    sh2.append(1)
                    matrix2 = self.__tomatrix__(other.__list, sh2)
                else:
                    sh2 = sh2 = list(other.shape)
                    matrix2 = self.__tomatrix__(other.__list, other.__shape)

                if sh1[1] == sh2[0]:
                    value = []
                    for i in range(sh1[0]):
                        value.append([])
                        for j in range(sh2[1]):
                            res = 0
                            for k in range(sh1[1]):
                                res += matrix1[i][k] * matrix2[k][j]
                            value[i].append(res)
                    if len(value) == 1:
                        value = value[0]
                    if (len(self.__shape) == 1) and (len(other.__shape) == 1):
                        return value[0]
                    value = Tensor(value)
                    if (len(value.__shape) == 2) and (value.__shape[1] == 1):
                        value.__shape = [value.__shape[0]]
                        value.shape = tuple(value.__shape)
                    return value
                raise ValueError
            raise ValueError
        raise ValueError

        raise TypeError

    def __str__(self):
        return str(self.__tomatrix__(self.__list, self.__shape))

    def swapaxes(self, axes1, axes2):
        newlist = []
        newsh = self.shape
        newsh = list(newsh)
        newsh[axes1], newsh[axes2] = newsh[axes2], newsh[axes1]
        for i in self.__list:
            newlist.append(None)
        for i in range(len(self.__list)):
            koord = self.__givekoord__(self.__shape, i)
            koord[axes1], koord[axes2] = koord[axes2], koord[axes1]
            pos = self.__fromkoord__(newsh, koord)
            newlist[pos] = self.__list[i]
        return Tensor(self.__tomatrix__(newlist, newsh))

    def sum(self, axis=None):
        value = 0
        if axis is None:
            for i in self.__list:
                value += i
            return value
        if axis >= len(self.__shape):
            raise ValueError
        temp = self
        for i in range(axis, 0, -1):
            temp = temp.swapaxes(i, i - 1)
        temp = self.__tomatrix__(temp.__list, temp.__shape)
        for i in temp:
            value += Tensor(i)
        return value

    def mean(self, axis=None):
        if len(self.__list) == 0:
            return None
        value = 0
        if axis is None:
            for i in self.__list:
                value += i
            return value / len(self.__list)
        if axis >= len(self.__shape):
            raise ValueError
        temp = self
        for i in range(axis, 0, -1):
            temp = temp.swapaxes(i, i - 1)
        temp = self.__tomatrix__(temp.__list, temp.__shape)
        for i in temp:
            value += Tensor(i)
        return value / self.__shape[axis]

    def max(self, axis=None):
        mmax = self.__list[0]
        if axis is None:
            for i in self.__list:
                if i > mmax:
                    mmax = i
            return mmax
        if axis >= len(self.__shape):
            raise ValueError
        temp = self
        for i in range(axis, 0, -1):
            temp = temp.swapaxes(i, i - 1)
        newshape = temp.__shape[1::]
        temp = self.__tomatrix__(temp.__list, temp.__shape)
        for i in range(len(temp)):
            temp[i] = Tensor(temp[i]).__list
        value = []
        for i in range(len(temp[0])):
            mas = []
            for j in range(len(temp)):
                mas.append(temp[j][i])
            mas = max(mas)
            value.append(mas)
        value = self.__tomatrix__(value, newshape)
        return Tensor(value)

    def min(self, axis=None):
        mmin = self.__list[0]
        if axis is None:
            for i in self.__list:
                if i < mmin:
                    mmin = i
            return mmin
        if axis >= len(self.__shape):
            raise ValueError
        temp = self
        for i in range(axis, 0, -1):
            temp = temp.swapaxes(i, i - 1)
        newshape = temp.__shape[1::]
        temp = self.__tomatrix__(temp.__list, temp.__shape)
        for i in range(len(temp)):
            temp[i] = Tensor(temp[i]).__list
        value = []
        for i in range(len(temp[0])):
            mas = []
            for j in range(len(temp)):
                mas.append(temp[j][i])
            mas = min(mas)
            value.append(mas)
        value = self.__tomatrix__(value, newshape)
        return Tensor(value)

    def argmax(self, axis=None):
        mmax = 0
        if axis is None:
            for i in range(len(self.__list)):
                if self.__list[i] > self.__list[mmax]:
                    mmax = i
            return mmax
        if axis >= len(self.__shape):
            raise ValueError
        temp = self
        for i in range(axis, 0, -1):
            temp = temp.swapaxes(i, i - 1)
        newshape = temp.__shape[1::]
        temp = self.__tomatrix__(temp.__list, temp.__shape)
        for i in range(len(temp)):
            temp[i] = Tensor(temp[i]).__list
        value = []
        for i in range(len(temp[0])):
            mmax = 0
            for j in range(len(temp)):
                if temp[j][i] > temp[mmax][i]:
                    mmax = j
            value.append(mmax)
        value = self.__tomatrix__(value, newshape)
        return Tensor(value)

    def argmin(self, axis=None):
        mmin = 0
        if axis is None:
            for i in range(len(self.__list)):
                if self.__list[i] < self.__list[mmin]:
                    mmin = i
            return mmin
        if axis >= len(self.__shape):
            raise ValueError
        temp = self
        for i in range(axis, 0, -1):
            temp = temp.swapaxes(i, i - 1)
        newshape = temp.__shape[1::]
        temp = self.__tomatrix__(temp.__list, temp.__shape)
        for i in range(len(temp)):
            temp[i] = Tensor(temp[i]).__list
        value = []
        for i in range(len(temp[0])):
            mmin = 0
            for j in range(len(temp)):
                if temp[j][i] < temp[mmin][i]:
                    mmin = j
            value.append(mmin)
        value = self.__tomatrix__(value, newshape)
        return Tensor(value)

    def transpose(self, *axis):
        value = self
        if axis == ():
            for i in range(len(self.__shape) // 2):
                value = value.swapaxes(i, len(self.__shape) - i - 1)
            return value
        if type(axis) != tuple:
            raise ValueError
        order = []
        for i in range(len(self.__shape)):
            order.append(i)
        i = 0
        while i < len(self.__shape):
            if order[i] != axis[i]:
                j = i
                while order[i] != axis[j]:
                    j += 1
                value = value.swapaxes(i, j)
                order[i], order[j] = order[j], order[i]

            if order[i] == axis[i]:
                i += 1
        return value
