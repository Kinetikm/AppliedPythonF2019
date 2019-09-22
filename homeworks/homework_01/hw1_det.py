#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    matrix = list_of_lists
    if len(matrix[0]) != len(matrix) or len(matrix) == 0:
        return None
    if len(matrix) == 1:
        d = matrix[0]
        return d
    if len(matrix) == 2:
        d = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        return d
    d = 0
    for i in range(len(matrix)):
        matrix2 = matrix
        matrix2 = matrix2[1:]
        for j in range(len(matrix2)):
            matrix2[j] = matrix2[j][0:i] + matrix2[j][i+1:]
        if (i % 2 == 0):
            sign = 1
        else:
            sign = -1
        if len(matrix2) > 0:
            det = calculate_determinant(matrix2)
            d += sign * matrix[0][i] * det
    return d
