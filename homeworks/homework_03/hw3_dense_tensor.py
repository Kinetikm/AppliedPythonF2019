#!/usr/bin/env python
# coding: utf-8


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
        self.matrix = init_matrix_representation
        self.shape = ()
        self.getshape(self.matrix)

    def getitem(self, mtr, key):
        if isinstance(key, (int, slice)):
            return mtr[key]
        if len(key) == 1:
            key = key[0]
        try:
            tmp = mtr[key]
        except:
            tmp = self.getitem(mtr[key[0]], key[1:])
        return tmp

    def setitem(self, mtr, key, data):
        if len(key) == 1:
            key = key[0]
        try:
            mtr[key] = data
        except:
            self.setitem(mtr[key[0]], key[1:], data)

    def __getitem__(self, key):
        return self.getitem(self.matrix, key)

    def __setitem__(self, key, data):
        self.setitem(self.matrix, key, data)

    def __str__(self):
        return str(self.matrix)

    def getshape(self, mtr):
        mtr = list(mtr)
        if isinstance(self.shape, tuple):
            self.shape = [len(mtr)]
        if isinstance(mtr[0], list):
            if len([1 for i in range(len(mtr) - 1) if
                    len(mtr[i]) == len(mtr[i + 1])]) + 1 == len(mtr):
                self.shape.append(len(mtr[0]))
                self.getshape(mtr[0])
        else:
            self.shape = tuple(self.shape)

    def add_num(self, mtr, numb):
        if isinstance(mtr, list):
            return [self.add_num(mtr[i], numb) for i in range(len(mtr))]
        else:
            return mtr + numb

    def add(self, mtr, other):
        if isinstance(mtr, list):
            return [self.add(mtr[i], other[i]) for i in range(len(mtr))]
        else:
            return mtr + other

    def __add__(self, other):
        if isinstance(other, Tensor):
            if self.shape == other.shape:
                return Tensor(self.add(self.matrix, other.matrix))
            else:
                raise ValueError
        else:
            return Tensor(self.add_num(self.matrix, other))

    def __sub__(self, other):
        return Tensor(self.__add__(other * -1))

    def mul_num(self, mtr, numb):
        if isinstance(mtr, list):
            return [self.mul_num(mtr[i], numb) for i in range(len(mtr))]
        else:
            return mtr * numb

    def mul(self, mtr, other):
        if isinstance(mtr, list):
            return [self.mul(mtr[i], other[i]) for i in range(len(mtr))]
        else:
            return mtr * other

    def __mul__(self, other):
        if isinstance(other, Tensor):
            if self.shape == other.shape:
                return Tensor(self.mul(self.matrix, other))
        else:
            return Tensor(self.mul_num(self.matrix, other))

    def __repr__(self):
        return str(self.matrix)

    def __truediv__(self, number):
        other = 1 / number
        return Tensor(self.mul_num(self.matrix, other))

    def _pow(self, mtr, number):
        if isinstance(mtr, list):
            return [self._pow(l, number) for l in mtr]
        else:
            return mtr ** number

    def __pow__(self, number):
        return self._pow(self.matrix, number)

    def makelist(self, shape):
        if len(shape) != 1:
            return [self.makelist(shape[1:]) for _ in range(shape[0])]
        else:
            return [None for _ in range(shape[0])]

    def _swapind(self, axis1, axis2, ind):
        ind = list(ind)
        ind[axis1], ind[axis2] = ind[axis2], ind[axis1]
        return tuple(ind)

    def swapaxes(self, axis1, axis2):
        if axis1 > len(self.shape) or axis2 > len(self.shape):
            raise IndexError
        new_shape = list(self.shape)
        new_shape[axis1], new_shape[axis2] = new_shape[axis2], new_shape[axis1]
        matrix = Tensor(self.makelist(new_shape))
        nw = [0 for _ in new_shape]
        while nw != [x - 1 for x in self.shape]:
            matrix[self._swapind(axis1, axis2, nw)] = self.__getitem__(
                tuple(nw))
            nw[-1] += 1
            for i in range(len(nw) - 1, -1, -1):
                if nw[i] == self.shape[i] and i != 0:
                    nw[i], nw[i - 1] = 0, nw[i - 1] + 1
        matrix[self._swapind(axis1, axis2, nw)] = self.__getitem__(tuple(nw))
        return Tensor(matrix)

    def _dum(self, tup):
        lst = [(i, x) for i, x in enumerate(tup) if i != x]
        for m in lst:
            if m[1] == lst[0][0]:
                return lst[0][0], m[0]

    def transpose(self, lst=None):
        if lst is None:
            lst = [x for x in range(len(self.shape) - 1, -1, -1)]
        else:
            lst = list(lst)
        query = []
        matrix = Tensor(self.matrix)
        while lst != [x for x in range(len(self.shape))]:
            query.append(dum(lst))
            lst[query[-1][0]], lst[query[-1][1]] = lst[query[-1][1]], lst[
                query[-1][0]]
        for op in query[::-1]:
            matrix = matrix.swapaxes(op[0], op[1])
        return Tensor(matrix)

    def _min(self, mtr, axis, cur):
        if cur != axis:
            return [self._min(mtr[i], axis, cur + 1) for i in
                    range(self.shape[cur])]
        else:
            return min([x for x in mtr])

    def min(self, axis=None):
        if axis is None:
            min_num = min(self.matrix)
            while isinstance(min_num, list):
                min_num = min(min_num)
            return min_num
        else:
            return self._min(self.matrix, axis, 0)

    def max(self, axis=None):
        tmp = Tensor(self.matrix) * -1
        return tmp.min(axis) * -1

    def _sum(self, mtr):
        if isinstance(mtr[0], list):
            return [self._sum(i) for i in mtr]
        else:
            return sum(mtr)

    def sum(self, axis=None):
        if axis is None:
            sum_num = self._sum(self.matrix)
            while isinstance(sum_num, list):
                sum_num = self._sum(sum_num)
            return sum_num
        else:
            que = []
            que += [x for x in range(len(self.shape)) if x != axis]
            que += [axis]
            matrix = Tensor(self.matrix).transpose(que)
            return Tensor(self._sum(matrix))

    def mean(self, axis=None):
        if axis is None:
            count = 1
            for x in self.shape:
                count *= x
            print(count)
            return Tensor(self.matrix).sum() / count
        else:
            return Tensor(Tensor(self.matrix).sum(axis)) / self.shape[axis]

    def _argmax(self, matrix):
        if isinstance(matrix[0], list):
            return [self._argmax(m) for m in matrix]
        else:
            for t1, tt in enumerate(matrix):
                if tt == max(matrix):
                    return t1

    def argmax(self, axis=None):
        if axis is None:
            ind = 0
            nw = [0 for _ in self.shape]
            mc = Tensor(self.matrix).max()
            while nw != [x - 1 for x in self.shape]:
                if self.__getitem__(tuple(nw)) == mc:
                    return ind
                nw[-1] += 1
                ind += 1
                for i in range(len(nw) - 1, -1, -1):
                    if nw[i] == self.shape[i] and i != 0:
                        nw[i], nw[i - 1] = 0, nw[i - 1] + 1
        else:
            que = []
            que += [x for x in range(len(self.shape)) if x != axis]
            que += [axis]
            matrix = Tensor(self.matrix).transpose(que)
            return Tensor(self._argmax(matrix))

    def argmin(self, axis=None):
        tmp = Tensor(self.matrix) * -1
        return tmp.argmax(axis)

    def dot(self, other):
        if len(other.shape) > 2 or len(self.shape) > 2:
            return None
        if len(self.shape) == 1:
            if len(other.shape) == 1:
                return sum([k * j for k, j in zip(self.matrix, other.matrix)])
            tmp = []
            for i_other in range(other.shape[1]):
                summ = 0
                for j, k in zip(self.matrix, other.transpose()[:, i_other]):
                    summ += j * k
                tmp.append(summ)
            return tmp
        if len(other.shape) == 1:
            tmp = []
            for i_self in range(self.shape[0]):
                summ = 0
                for j, k in zip(self.__getitem__(i_self), other.matrix):
                    summ += j * k
                tmp.append(summ)
            return tmp
        mtr = []
        for i_self in range(self.shape[0]):
            tmp = []
            for i_other in range(other.shape[1]):
                summ = 0
                for j, k in zip(self.__getitem__(i_self),
                                other.transpose()[:, i_other]):
                    summ += j * k
                tmp.append(summ)
            mtr.append(tmp)
        return Tensor(mtr)
