#!/usr/bin/env python
# coding: utf-8


import numpy as np


class CSRMatrix:
    def __init__(self, init_matrix_representation):
        raise NotImplementedError
        self.a = []
        self.ia = [0]
        self.ja = []
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.a = init_matrix_representation[2]
            self.ja = init_matrix_representation[1]
            if len(self.a) != 0:
                prev = init_matrix_representation[0][0]
                if (prev != 0):
                    for k in range(prev):
                        self.ia.append(0)
                count = 0
                for i in init_matrix_representation[0]:
                    for k in range(prev, i):
                        self.ia.append(count)
                    count += 1
                    prev = i
                self.ia.append(count)
        elif isinstance(init_matrix_representation, np.ndarray):
            count = 0
            for i in range(len(init_matrix_representation)):
                for j in range(len(init_matrix_representation[i])):
                    if (init_matrix_representation[i][j] != 0):
                        self.a.append(init_matrix_representation[i][j])
                        count += 1
                        self.ja.append(j)
                self.ia.append(count)
            if self.a == []:
                self.ia = [0]
        else:
            raise ValueError

    @property
    def nnz(self):
        return len(self.a)

    def __getitem__(self, ind):
        if len(self.a) == 0:
            return 0

        before = self.ia[ind[0]]  # сколько ненулевых элементов было в предыдущих строках
        if ind[0] != len(self.ia) - 1:
            next = self.ia[ind[0] + 1]  # before + в новой строке
        else:
            next = before

        if ind[0] >= len(self.ia) - 1 or ind[1] > max(self.ja):
            raise ValueError
        elif next == before or (ind[1] not in self.ja[before:next]):
            return 0
        else:
            result = self.ja[before:next].index(ind[1])
            return self.a[before+result]

    def __setitem__(self, ind, value):
        if len(self.a) == 0:
            self.a += [value]
            if ind[0] != 0:
                for i in range(ind[0]):
                    self.ia += [0]
            self.ia += [1]
            self.ja += [ind[1]]
            return

        if ind[0] >= len(self.ia) - 1 or ind[1] > max(self.ja):
            result = None
        else:
            result = self[ind]

        if (result is not None) and result != 0:
            before = self.ia[ind[0]]
            next = self.ia[ind[0] + 1]
            offset = self.ja[before:next].index(ind[1])
            self.a[before + offset] = value
        elif result == 0:
            if len(self.ia) - 1 <= ind[0]:
                self.ia += [self.ia[-1] + 1]
                self.ja += [ind[0]]
                self.a += [value]
                return
            for j in range(self.ia[ind[0]], self.ia[ind[0] + 1]):
                if self.ja[j] > ind[1]:
                    self.ja.insert(j, ind[1])
                    self.a.insert(j, value)
                    break
                elif j == self.ia[ind[0] + 1] - 1:
                    self.ja.insert(j + 1, ind[1])
                    self.a.insert(j + 1, value)
            for i in range(ind[0] + 1, len(self.ia)):
                self.ia[i] += 1

        elif result is None:   # добавляются элементы с индексами больше, чем размер матрицы
            if len(self.ia) - 1 <= ind[0]:
                last = self.ia[-1]
                for i in range(len(self.ia), ind[0]):
                    self.ia.append(last)
                self.ia.append(last + 1)
            else:
                for i in range(ind[0] + 1, len(self.ia)):
                    self.ia[i] += 1

            before = self.ia[ind[0]]
            next = self.ia[ind[0] + 1]
            if max(self.ja) < ind[1]:
                self.ja.insert(next, ind[1])
                self.a.insert(next, value)
            else:
                for j in range(before, next):  # ищем по ja, куда поставить новый номер столбца ind[1]
                    if self.ja[j] > ind[1]:
                        self.ja.insert(j, ind[1])
                        self.a.insert(j, value)
                        break
                    elif j == next - 1:  # если дошли до конца списка ja и последний элемент меньше ind[1]
                        self.ja.insert(j + 1, ind[1])
                        self.a.insert(j + 1, value)

    def __add__(self, other):
        if not isinstance(other, CSRMatrix):
            raise TypeError
        if self.ia == other.ia and self.ja == other.ja:
            data = [self.a[i] + other.a[i] for i in range(len(self.a))]
            row = []
            i = 0
            while len(row) != len(data):
                for j in range(self.ia[i + 1] - self.ia[i]):
                    row += [i]
                i += 1
            return CSRMatrix((row, self.ja, data))
        if len(self.ia) == len(other.ia):
            row = []
            column = []
            data = []
            self_ind = 0
            other_ind = 0
            for i in range(1, len(self.ia)):
                while self_ind < self.ia[i]:
                    if other_ind >= other.ia[i] or self.ja[self_ind] < other.ja[other_ind]:
                        data += [self.a[self_ind]]
                        row += [i-1]
                        column += [self.ja[self_ind]]
                        self_ind += 1
                    elif self.ja[self_ind] > other.ja[other_ind]:
                        data += [other.a[other_ind]]
                        row += [i - 1]
                        column += [other.ja[other_ind]]
                        other_ind += 1
                    elif self.ja[self_ind] == other.ja[other_ind]:
                        data += [other.a[other_ind] + self.a[self_ind]]
                        row += [i - 1]
                        column += [self.ja[self_ind]]
                        self_ind += 1
                        other_ind += 1

                if other_ind < other.ia[i]:
                    while other_ind < other.ia[i]:
                        data += [other.a[other_ind]]
                        row += [i - 1]
                        column += [other.ja[other_ind]]
                        other_ind += 1
            return CSRMatrix((row, column, data))

    def __sub__(self, other):
        if not isinstance(other, CSRMatrix):
            raise TypeError
        if self.ia == other.ia and self.ja == other.ja:
            data = [self.a[i] - other.a[i] for i in range(len(self.a))]
            row = []
            i = 0
            while len(row) != len(data):
                for j in range(self.ia[i + 1] - self.ia[i]):
                    row += [i]
                i += 1
            return CSRMatrix((row, self.ja, data))

    def __mul__(self, other):
        if isinstance(other, CSRMatrix) and self.ia == other.ia and self.ja == other.ja:
            data = [self.a[i] * other.a[i] for i in range(len(self.a))]
            row = []
            i = 0
            while len(row) != len(data):
                for j in range(self.ia[i + 1] - self.ia[i]):
                    row += [i]
                i += 1
            return CSRMatrix((row, self.ja, data))
        elif isinstance(other, int) or isinstance(other, float):
            data = [self.a[i] * other for i in range(len(self.a))]
            row = []
            i = 0
            while len(row) != len(data):
                for j in range(self.ia[i + 1] - self.ia[i]):
                    row += [i]
                i += 1
            return CSRMatrix((row, self.ja, data))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            data = [self.a[i] / other for i in range(len(self.a))]
            row = []
            i = 0
            while len(row) != len(data):
                for j in range(self.ia[i + 1] - self.ia[i]):
                    row += [i]
                i += 1
            return CSRMatrix((row, self.ja, data))

    def to_dense(self):
        result = []
        count = 0
        for i in range(1, len(self.ia)):
            row = [0 for k in range(max(self.ja) + 1)]
            for j in range(self.ia[i] - self.ia[i-1]):
                row[self.ja[count]] = self.a[count]
                count += 1
            result.append(row)
        return np.array(result)
