#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    if len(list_of_lists) != len(list_of_lists[0]):
        return None

    def minor(mat, i):
        return list(map(lambda row: row[:i] + row[i + 1:], mat[1:]))

    def det(matrix):
        sum_m = 0
        if len(matrix) == 1 and len(matrix[0]) == 1:
            return matrix[0][0]
        else:
            for j in range(len(matrix)):
                sum_m += ((- 1) ** (2 + j)) * matrix[0][j] * \
                         det(minor(matrix, j))
            return sum_m

    return det(list_of_lists)
