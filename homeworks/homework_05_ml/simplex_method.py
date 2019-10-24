#!/usr/bin/env python
# coding: utf-8

import numpy as np


def simplex_method(a, b, c):
    c = c * -1
    n = a.shape[0]
    m = a.shape[1]
    b = b.reshape(n, 1)
    a = a.astype('float64')
    b = b.astype('float64')
    c = c.astype('float64')
    b = np.vstack((b, np.array([0])))
    table = np.vstack((a, c))
    table = np.hstack((table, b))
    table[-1, -1] = 0
    x_row = []
    for i in range(m):
        x_row.append((i, 'x'))
    y_column = []
    for i in range(n):
        y_column.append((i, 'y'))
    n += 1
    m += 1
    while min(table[-1, :-1]) < 0:
        col = np.argmin(table[-1, :-1])
        sim_col = np.copy(table[:-1, -1])
        for i in range(n - 1):
            sim_col[i] = sim_col[i] / table[i, col]
        row = np.argmin(sim_col)
        pivot = table[row, col]
        for i in range(m):
            table[row, i] /= pivot
        pivot = table[row, col]
        for i in range(n):
            if i != row:
                elem = table[i, col]
                for j in range(m):
                    table[i, j] -= table[row, j] * elem
        x_row[col], y_column[row] = y_column[row], x_row[col]
    x = [0] * (m - 1)
    for i in range(n - 1):
        if y_column[i][1] == 'x':
            x[y_column[i][0]] = table[i, -1]
    return np.array(x)
