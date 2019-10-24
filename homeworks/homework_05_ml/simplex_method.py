#!/usr/bin/env python
# coding: utf-8

import numpy as np


def simplex_method(a, b, c):
    n, m = np.shape(a)
    x = np.zeros(m)
    s = np.array([-1] * n)
    matrix = np.concatenate((a, c.reshape(1, m) * (-1)))
    matrix = np.concatenate((matrix, np.eye(n + 1)), axis=1)
    b_col = (b.reshape(n, 1), [[0]])
    matrix = np.concatenate((matrix, np.concatenate(b_col)), axis=1)
    while matrix[-1].min() < 0:
        p_col = matrix[-1].argmin()
        minb = b[0]
        p_row = 0
        for i in range(len(b)):
            if matrix[i][p_col] != 0:
                value = matrix[i][-1] / matrix[i][p_col]
                if minb > value:
                    minb = value
                    p_row = i
        matrix[p_row] /= matrix[p_row][p_col]
        for row in matrix:
            if not np.array_equal(row, matrix[p_row]):
                row -= matrix[p_row] * row[p_col]
        s[p_row] = p_col
    for i in range(n):
        if s[i] != -1:
            x[s[i]] = matrix[i][-1]
    return np.array(x)
