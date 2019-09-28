#!/usr/bin/env python
# coding: utf-8


class GoodTable:

    def __init__(self, data: list):
        self.data = data

    def print_table(self):
        self.max_length, self.max_columns = self.calc_max_length()
        print('-' * self.max_length)
        for i, item in enumerate(self.data):
            for j, element in enumerate(item):
                if i == 0:
                    self.data[i][j] = str(element).center(self.max_columns[j])
                elif j != (len(item) - 1):
                    self.data[i][j] = str(element).ljust(self.max_columns[j])
                else:
                    self.data[i][j] = str(element).rjust(self.max_columns[j])
        for row in self.data:
            print('|  ' + '  |  '.join(row) + '  |')
        print('-' * self.max_length)

    def calc_max_length(self):
        max_col = []
        for i in range(len(self.data[0])):
            max_col.append(max([len(str(item[i])) for item in self.data]))
        max_len = sum(max_col) + len(self.data[0]) * 5 + 1
        return max_len, max_col
