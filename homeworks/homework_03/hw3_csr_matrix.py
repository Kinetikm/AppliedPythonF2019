#!/usr/bin/env python
# coding: utf-8

class CSRMatrix:

    def __init__(self):
        pass

"""
import numpy as np
from copy import deepcopy


class CSRMatrix:

    __slots__ = ["non_zero_value", "row_indexing", "column_indexing", "_nnz"]

    def __init__(self, init_matrix_representation):

        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:

        elif isinstance(init_matrix_representation, np.ndarray):
            self.non_zero_value = list()
            self.row_indexing = list()
            self.column_indexing = list()

            for row, container in enumerate(init_matrix_representation):
                for column, element in enumerate(container):
                    if element != 0:
                        self.non_zero_value += [element]
                        self.row_indexing += [row]
                        self.column_indexing += [column]

            self.row_indexing = deepcopy(init_matrix_representation[0])
            self.column_indexing = deepcopy(init_matrix_representation[1])
            self.non_zero_value = deepcopy(init_matrix_representation[2])

        elif isinstance(init_matrix_representation, CSRMatrix):
            self.non_zero_value = deepcopy(init_matrix_representation.non_zero_value)
            self.row_indexing = deepcopy(init_matrix_representation.row_indexing)
            self.column_indexing = deepcopy(init_matrix_representation.column_indexing)

        else:
            raise ValueError

    def __setitem__(self, index, value):
        if len(index) >= 3 or index[0] < 0 or index[1] < 0:
            raise LookupError

        if len(self.non_zero_value) == 0 and value != 0:
            self.non_zero_value += [value]
            self.row_indexing += [index[0]]
            self.column_indexing += [index[1]]

            return

        loop = 0
        while loop < len(self.non_zero_value) - 1 and index[0] > self.row_indexing[loop] and \
                index[1] > self.column_indexing[loop]:
            loop += 1

        if index[0] != self.row_indexing[loop] and index[1] != self.column_indexing[loop]:
            if value != 0:
                self.row_indexing += self.row_indexing[:loop] + [index[0]] + self.row_indexing[loop:]
                self.column_indexing += self.column_indexing[:loop] + [index[1]] + self.column_indexing[loop:]
                self.non_zero_value += self.non_zero_value[:loop] + [value] + self.non_zero_value[loop:]
            else:
                return
        elif index[0] != self.row_indexing[loop]:
            if value != 0:
                self.row_indexing += self.row_indexing[:loop] + [index[0]] + self.row_indexing[loop:]
                self.non_zero_value += self.non_zero_value[:loop] + [value] + self.non_zero_value[loop:]
            else:
                return
        elif index[1] != self.column_indexing[loop]:
            if value != 0:
                self.column_indexing += self.column_indexing[:loop] + [index[1]] + self.column_indexing[loop:]
                self.non_zero_value += self.non_zero_value[:loop] + [value] + self.non_zero_value[loop:]
            else:
                return
        else:
            if value != 0:
                self.non_zero_value[loop] = value
            else:
                self.non_zero_value.pop(loop)
                self.row_indexing.pop(loop)
                self.column_indexing.pop(loop)

        return

    def __getitem__(self, index):
        if len(index) >= 3:
            raise LookupError

        for i, j in zip(self.row_indexing, self.column_indexing):
            if i == index[0] and j == index[1]:
                return self.non_zero_value[i]

    def __add__(self, other):
        if isinstance(other, CSRMatrix):

            if len(other.non_zero_value) == 0:
                return
            if len(self.non_zero_value) == 0:
                return other

            res_row = list()
            res_column = list()
            res_value = list()

            index_self = 0
            index_other = 0

            while index_self != len(self.non_zero_value) and index_other != len(other.non_zero_value):

                if self.row_indexing[index_self] < other.row_indexing[index_other] or self.row_indexing[index_self] \
                        == other.row_indexing[index_other] and self.column_indexing[index_self] < \
                        other.column_indexing[index_other]:

                    res_row += [self.row_indexing[index_self]]
                    res_column += [self.column_indexing[index_self]]
                    res_value += [self.non_zero_value[index_self]]

                    index_self += 1

                elif other.row_indexing[index_other] < self.row_indexing[index_self] or other.row_indexing[index_other] \
                        == self.row_indexing[index_self] and other.column_indexing[index_other] < \
                        self.column_indexing[index_self]:

                    res_row += [other.row_indexing[index_other]]
                    res_column += [other.column_indexing[index_other]]
                    res_value += [other.non_zero_value[index_other]]

                    index_other += 1

                elif self.row_indexing[index_self] == other.row_indexing[index_other] and \
                        self.column_indexing[index_self] == other.column_indexing[index_other]:

                    value = self.non_zero_value[index_self] + other.non_zero_value[index_other]

                    if value != 0:
                        res_row += [self.row_indexing[index_self]]
                        res_column += [self.column_indexing[index_self]]
                        res_value += [value]

                    index_self += 1
                    index_other += 1

            while index_self < len(self.non_zero_value):
                res_row += [self.row_indexing[index_self]]
                res_column += [self.column_indexing[index_self]]
                res_value += [self.non_zero_value[index_self]]

                index_self += 1

            while index_other < len(other.non_zero_value):
                res_row += [other.row_indexing[index_other]]
                res_column += [other.column_indexing[index_other]]
                res_value += [other.non_zero_value[index_other]]

                index_other += 1

            return CSRMatrix((res_row, res_column, res_value))

        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, CSRMatrix):

            if len(other.non_zero_value) == 0:
                return
            if len(self.non_zero_value) == 0:
                for element in other.non_zero_value:
                    element = -element

                return other

            res_row = list()
            res_column = list()
            res_value = list()

            index_self = 0
            index_other = 0

            while index_self != len(self.non_zero_value) and index_other != len(other.non_zero_value):

                if self.row_indexing[index_self] < other.row_indexing[index_other] or self.row_indexing[index_self] \
                        == other.row_indexing[index_other] and self.column_indexing[index_self] < \
                        other.column_indexing[index_other]:

                    res_row += [self.row_indexing[index_self]]
                    res_column += [self.column_indexing[index_self]]
                    res_value += [-self.non_zero_value[index_self]]

                    index_self += 1

                elif other.row_indexing[index_other] < self.row_indexing[index_self] or other.row_indexing[index_other] \
                        == self.row_indexing[index_self] and other.column_indexing[index_other] < \
                        self.column_indexing[index_self]:

                    res_row += [other.row_indexing[index_other]]
                    res_column += [other.column_indexing[index_other]]
                    res_value += [-other.non_zero_value[index_other]]

                    index_other += 1

                elif self.row_indexing[index_self] == other.row_indexing[index_other] and \
                        self.column_indexing[index_self] == other.column_indexing[index_other]:

                    value = self.non_zero_value[index_self] - other.non_zero_value[index_other]

                    if value != 0:
                        res_row += [self.row_indexing[index_self]]
                        res_column += [self.column_indexing[index_self]]
                        res_value += [value]

                    index_self += 1
                    index_other += 1

            while index_self < len(self.non_zero_value):
                res_row += [self.row_indexing[index_self]]
                res_column += [self.column_indexing[index_self]]
                res_value += [-self.non_zero_value[index_self]]

                index_self += 1

            while index_other < len(other.non_zero_value):
                res_row += [other.row_indexing[index_other]]
                res_column += [other.column_indexing[index_other]]
                res_value += [-other.non_zero_value[index_other]]

                index_other += 1

            return CSRMatrix((res_row, res_column, res_value))

        else:
            raise TypeError

    def __mul__(self, other):
        if isinstance(other, CSRMatrix):

            if len(other.non_zero_value) == 0:
                return 0
            if len(self.non_zero_value) == 0:
                return 0

            res_row = list()
            res_column = list()
            res_value = list()

            index_self = 0
            index_other = 0

            while index_self != len(self.non_zero_value) and index_other != len(other.non_zero_value):

                if self.row_indexing[index_self] == other.row_indexing[index_other] and \
                        self.column_indexing[index_self] == other.column_indexing[index_other]:

                    value = self.non_zero_value[index_self] * other.non_zero_value[index_other]

                    if value != 0:
                        res_row += [self.row_indexing[index_self]]
                        res_column += [self.column_indexing[index_self]]
                        res_value += [value]

                    index_self += 1
                    index_other += 1

            return CSRMatrix((res_row, res_column, res_value))

        elif isinstance(other, float) or isinstance(other, int):

            if len(other) == 0:
                return 0
            if len(self.non_zero_value) == 0:
                return 0

            res_row = list()
            res_column = list()
            res_value = list()

            index_self = 0

            while index_self != len(self.non_zero_value):

                value = self.non_zero_value[index_self] * other

                if value != 0:
                    res_row += [self.row_indexing[index_self]]
                    res_column += [self.column_indexing[index_self]]
                    res_value += [value]

                index_self += 1

            return CSRMatrix((res_row, res_column, res_value))

        else:
            raise TypeError

    __rmul__ = __mul__

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError

        if isinstance(other, int) or isinstance(other, float):
            res_row = list()
            res_column = list()
            res_value = list()

            index_self = 0

            while index_self != len(self.non_zero_value):

                value = self.non_zero_value[index_self] / other

                if value != 0:
                    res_row += [self.row_indexing[index_self]]
                    res_column += [self.column_indexing[index_self]]
                    res_value += [value]

                index_self += 1

            return CSRMatrix((res_row, res_column, res_value))
        else:
            raise TypeError

    def __matmul__(self, other):
        if isinstance(other, CSRMatrix):
            if max(self.column_indexing) != max(other.row_indexing):

                res_row = list()
                res_column = list()
                res_value = list()

                pass
            else:
                raise ValueError
        else:
            raise TypeError

    nnz = property()

    @nnz.setter
    def nnz(self, value):
        if value != len(self.data):
            raise AttributeError
        self._nnz = value

    @nnz.getter
    def nnz(self):
        return self._nnz

    def to_dense(self):
        result = np.zeros((max(self.row_indexing), max(self.column_indexing)))

        for i, j, value in zip(self.row_indexing, self.column_indexing, self.non_zero_value):
            result[i, j] = value

        return result
"""
