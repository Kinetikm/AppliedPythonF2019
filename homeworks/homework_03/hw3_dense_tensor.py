import copy
from itertools import product
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

    def __init__(self, init_matrix_representation=None):

        """
        :param init_matrix_representation: list of lists

        """
        self.dim_of = {}
        self.dimen = {}
        self.data = []
        if init_matrix_representation is not None:
            if not isinstance(init_matrix_representation, list):
                raise ValueError
            self._wrap(init_matrix_representation, 0)
            self._calc_offsets()

    def _calc_offsets(self):
        self.dim_of[len(self.dimen) - 1] = 1
        for i in range(len(self.dimen) - 2, -1, -1):
            self.dim_of[i] = self.dim_of[i + 1] * self.dimen[i + 1]

    def _wrap(self, obj, dim):
        if dim in self.dimen:
            if self.dimen[dim] != len(obj):
                raise ValueError
        else:
            self.dimen[dim] = len(obj)
        if all(isinstance(el, list) for el in obj):
            for el in obj:
                self._wrap(el, dim + 1)
        elif all(isinstance(el, (float, int)) for el in obj):
            for el in obj:
                self.data.append(el)
        else:
            raise ValueError

    def from_tensor(self):
        ret = Tensor()
        ret.dimen = copy.deepcopy(self.dimen)
        ret.dim_of = copy.deepcopy(self.dim_of)
        ret.data = copy.deepcopy(self.data)
        return ret

    def __getitem__(self, key):
        if not isinstance(key, (tuple, int)):
            raise IndexError
        if isinstance(key, tuple) and len(key) != len(self.dimen):
            raise IndexError
        if isinstance(key, int):
            if 0 <= key < len(self.data):
                return self.data[key]
            else:
                raise IndexError
        for i, ind in enumerate(key):
            if ind < 0 or ind >= self.dimen[i]:
                raise IndexError
        index = 0
        for i, ind in enumerate(key):
            index += ind * self.dim_of[i]
        return self.data[index]

    def __setitem__(self, key, value):
        if not isinstance(key, tuple):
            raise IndexError
        if not isinstance(value, (int, float, np.int, np.float, np.int64)):
            raise ValueError
        if len(key) != len(self.dimen):
            raise IndexError
        for i, ind in enumerate(key):
            if ind < 0 or ind >= self.dimen[i]:
                raise IndexError
        index = 0
        for i, ind in enumerate(key[:len(key):]):
            index += ind * self.dim_of[i]
        self.data[index] = value

    def __sub__(self, other):
        res = self.from_tensor()
        if isinstance(other, Tensor):
            if self.dimen == other.dimen:
                for i, val in enumerate(self.data):
                    res.data[i] = val - other.data[i]
            else:
                raise ValueError
        elif isinstance(other, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                res.data[i] = val - other
        return res

    def __add__(self, other):
        res = self.from_tensor()
        if isinstance(other, Tensor):
            if self.dimen == other.dimen:
                for i, val in enumerate(self.data):
                    res.data[i] = val + other.data[i]
            else:
                raise ValueError
        elif isinstance(other, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                res.data[i] = val + other
        return res

    def __radd__(self, other):
        res = self.from_tensor()
        if isinstance(other, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                res.data[i] = val + other
        return res

    def __mul__(self, other):
        res = self.from_tensor()
        if isinstance(other, Tensor):
            if self.dimen == other.dimen:
                for i, val in enumerate(self.data):
                    res.data[i] = val * other.data[i]
            else:
                raise ValueError
        elif isinstance(other, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                res.data[i] = val * other
        return res

    def __truediv__(self, other):
        res = self.from_tensor()
        if isinstance(other, (int, float, np.int, np.float, np.int64)):
            if other == 0:
                raise ZeroDivisionError
            for i, val in enumerate(self.data):
                res.data[i] = val / other
        return res

    def __pow__(self, power, modulo=None):
        res = self.from_tensor()
        if isinstance(power, (int, float, np.int, np.float, np.int64)):
            for i, val in enumerate(self.data):
                res.data[i] = val ** power
        return res

    def _compress(self, ax):
        res = Tensor()
        for k in self.dimen:
            if k > ax:
                res.dimen[k - 1] = self.dimen[k]
            elif k == ax:
                continue
            else:
                res.dimen[k] = self.dimen[k]
        res._calc_offsets()
        return res

    def sum(self, ax=None):
        if ax is None:
            res = 0
            for i in self.data:
                res += i
            return res
        else:
            res = self._compress(ax)
            n_el = len(self.data) // self.dimen[ax]
            res.data = [0] * n_el
            dims = []
            for i in range(len(self.dimen)):
                dims.append(self.dimen[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                i.pop(ax)
                res[tuple(i)] += self[index]
            return res

    def to_list(self):
        if len(self.dimen) == 1:
            return self.data
        return self._get_as_list(self.data, len(self.dimen) - 1)

    def _get_as_list(self, arr, dim):
        if dim == (len(self.dimen) - 1):
            dims = []
            v = []
            for i in range(len(self.dimen)):
                dims.append(self.dimen[i])
            for index in product(*[range(k) for k in dims]):
                v.append(self[index])
            arr = v
        if dim > 0:
            l1 = list()
            l2 = list()
            n = self.dimen[dim]
            for i, item in enumerate(arr):
                l2.append(copy.deepcopy(item))
                if i >= 0 and (i + 1) % n == 0:
                    l1.append(copy.deepcopy(l2))
                    l2.clear()
            return self._get_as_list(l1, dim - 1)
        else:
            return arr

    def mean(self, ax=None):
        if ax is None:
            ret = 0
            for i in self.data:
                ret += i
            return ret / len(self.data)
        else:
            t = self.sum(ax)
            for i, it in enumerate(t.data):
                t.data[i] = it / self.dimen[ax]
            return t

    def min(self, ax=None):
        if ax is None:
            return min(self.data)
        else:
            res = self._compress(ax)
            n_el = len(self.data) // self.dimen[ax]
            res.data = [max(self.data)] * n_el
            dims = []
            for i in range(len(self.dimen)):
                dims.append(self.dimen[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                i.pop(ax)
                if self[index] < res[tuple(i)]:
                    res[tuple(i)] = self[index]
            return res

    def max(self, ax=None):
        if ax is None:
            return max(self.data)
        else:
            res = self._compress(ax)
            n_el = len(self.data) // self.dimen[ax]
            res.data = [min(self.data)] * n_el
            dims = []
            for i in range(len(self.dimen)):
                dims.append(self.dimen[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                i.pop(ax)
                if self[index] > res[tuple(i)]:
                    res[tuple(i)] = self[index]
            return res

    def argmax(self, ax=None):
        max_val = max(self.data)
        if ax is None:
            return self.data.index(max_val)
        else:
            res = self._compress(ax)
            n_el = len(self.data) // self.dimen[ax]
            res.data = [0] * n_el
            dims = []
            for i in range(len(self.dimen)):
                dims.append(self.dimen[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                k = i.pop(ax)
                j = copy.deepcopy(i)
                j.insert(ax, res[tuple(i)])
                if self[index] > self[tuple(j)]:
                    res[tuple(i)] = k
            return res

    def argmin(self, ax=None):
        min_val = min(self.data)
        if ax is None:
            return self.data.index(min_val)
        else:
            res = self._compress(ax)
            n_el = len(self.data) // self.dimen[ax]
            res.data = [0] * n_el
            dims = []
            for i in range(len(self.dimen)):
                dims.append(self.dimen[i])
            for index in product(*[range(k) for k in dims]):
                i = list(index)
                k = i.pop(ax)
                j = copy.deepcopy(i)
                j.insert(ax, res[tuple(i)])
                if self[index] < self[tuple(j)]:
                    res[tuple(i)] = k
            return res

    def swap(self, first, second):
        if first < 0 or first >= len(self.dimen) or second < 0 or second >= len(self.dimen):
            raise ValueError
        res = Tensor()
        res.dimen = copy.deepcopy(self.dimen)
        res.data = self.data
        res.dim_of = copy.deepcopy(self.dim_of)
        v = res.dimen[first]
        res.dimen[first] = res.dimen[second]
        res.dimen[second] = v
        v = res.dim_of[first]
        res.dim_of[first] = res.dim_of[second]
        res.dim_of[second] = v
        return res

    def transpose(self, *ax):
        res = Tensor()
        res.data = self.data
        if ax is None:
            res.dimen = copy.deepcopy(self.dimen)
            res.dim_of = copy.deepcopy(self.dim_of)
            for i in range(len(res.dimen) // 2):
                v = res.dimen[i]
                res.dimen[i] = res.dimen[len(res.dimen) - 1 - i]
                res.dimen[len(res.dimen) - 1 - i] = v
                v = res.dim_of[i]
                res.dim_of[i] = res.dim_of[len(res.dimen) - 1 - i]
                res.dim_of[len(res.dimen) - 1 - i] = v
        else:
            if not isinstance(ax, tuple):
                raise ValueError
            if len(ax) != len(self.dimen):
                raise ValueError
            for i, new_i in enumerate(ax):
                res.dimen[i] = copy.copy(self.dimen[new_i])
                res.dim_of[i] = copy.copy(self.dim_of[new_i])
        return res

    def __matmul__(self, other):
        if len(self.dimen) == len(other.dimen) == 1:
            if len(self.dimen[0]) == len(other.dimen[0]):
                res = 1
                for i in range(self.dimen[0]):
                    res *= self.data[i] * other.data[i]
                return res
            else:
                raise ValueError
        if len(self.dimen) == len(other.dimen) == 2:
            if self.dimen[1] == other.dimen[0]:
                res = Tensor()
                m = self.dimen[0]
                k = other.dimen[1]
                res.dimen[0] = m
                res.dimen[1] = k
                res.dim_of = {}
                res._calc_offsets()
                res.data = [0] * (m * k)
                for i, j in [(x, y) for x in range(m) for y in range(k)]:
                    for p in range(self.dimen[1]):
                        res[i, j] += self[i, p] * other[p, j]
                return res
            else:
                raise ValueError
        if len(self.dimen) == 1 and len(other.dimen) == 2:
            if self.dimen[0] == other.dimen[0]:
                res = Tensor()
                res.dimen[0] = other.dimen[1]
                res.data = [0] * other.dimen[1]
                for i, j in [(x, y) for x in range(1) for y in range(other.dimen[1])]:
                    for p in range(other.dimen[0]):
                        res.data[j] += self.data[p] * other[p, j]
                return res
            else:
                raise ValueError
        if len(self.dimen) == 2 and len(other.dimen) == 1:
            if self.dimen[1] == other.dimen[0]:
                res = Tensor()
                res.dimen[0] = self.dimen[0]
                res.data = [0] * self.dimen[0]
                for i, j in [(x, y) for x in range(self.dimen[0]) for y in range(1)]:
                    for p in range(other.dimen[0]):
                        res.data[i] += self[i, p] * other.data[p]
                return res
            else:
                raise ValueError
