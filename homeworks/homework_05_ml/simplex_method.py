#!/usr/bin/env python
# coding: utf-8

import numpy as np


def simplex_method(a, b, c):

    n = a.shape[0]
    m = a.shape[1]
    b1 = b.reshape(n, 1)
    c1 = -c.reshape(1, m)
    matrix = np.concatenate((a, c1))
    matrix = np.concatenate((matrix, np.eye(n + 1)), axis=1)
    matrix = np.concatenate((matrix, np.concatenate((b1, [[0]]))), axis=1)
    column = list(zip(['s'] * n, range(n)))
    row = list(zip(['x'] * m, range(m)))
    while matrix[-1].min() < 0:
        j = matrix[-1].argmin()
        i = (matrix[:-1, -1] / matrix[:-1, j]).argmin()
        matrix[i, :] /= matrix[i, j]
        for k in range(n + 1):
            if k == i:
                continue
            matrix[k, :] -= matrix[i, :] * (matrix[k, j] / matrix[i, j])
        column[i] = row[j]
    x = np.array([0] * m)
    for i in range(len(column)):
        if column[i][0] == 'x':
            x[column[i][1]] = matrix[i, -1]
    return x
