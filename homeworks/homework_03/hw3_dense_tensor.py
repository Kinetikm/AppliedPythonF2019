from itertools import product
import copy
import numpy


class Tensor:

    def __init__(self, matrix):
        self.matrix = matrix

        self.all_size = [len(self.matrix)]
        sub_matrix = self.matrix
        while True:
            try:
                self.all_size.append(len(sub_matrix[0]))
                sub_matrix = sub_matrix[0]
            except Exception:
                break
        raise NotImplementedError

    def __setitem__(self, item, value):
        sub_matrix = self.matrix
        for i in item[:-1]:
            sub_matrix = sub_matrix[i]
        sub_matrix[item[-1]] = value

    def __getitem__(self, item):
        sub_matrix = self.matrix
        for i in item:
            sub_matrix = sub_matrix[i]
        return sub_matrix

    def __add__(self, other):
        return self._recursion(other, '+')

    __radd__ = __add__

    def __sub__(self, other):
        return self._recursion(other, '-')

    def __mul__(self, other):
        return self._recursion(other, '*')

    def __truediv__(self, other):
        return self._recursion(other, '/')

    def __pow__(self, other):
        return self._recursion(other, '**')

    def _recursion(self, other, sign):
        xyz = [range(i) for i in self.all_size]
        result = Tensor(copy.deepcopy(self.matrix))
        if isinstance(other, Tensor):
            if self.all_size != other.all_size:
                raise ValueError
            for ind in product(*xyz):
                result[ind] = self._base_oper(self[ind], other[ind], sign)
        else:
            for ind in product(*xyz):
                result[ind] = self._base_oper(self[ind], other, sign)
        return result

    def _base_oper(self, val_1, val_2, sign):
        if sign == '+':
            return val_1 + val_2
        elif sign == '-':
            return val_1 - val_2
        elif sign == '*':
            return val_1 * val_2
        elif sign == '/':
            return val_1 / val_2
        else:
            return val_1 ** val_2
