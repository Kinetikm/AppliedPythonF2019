#!/usr/bin/env python
# coding: utf-8

import numpy as np


def create_matr(a, b, c):
    a_copy = a.copy()
    b_copy = b.copy()
    c_copy = c.copy() * (-1)
    right = np.hstack((b_copy, np.array([0])))[np.newaxis].T
    left = np.vstack((a_copy, c_copy))
    left = np.hstack((left, np.eye(b.shape[0] + 1)))
    matrix = np.hstack((left, right))
    return matrix


def simplex_method(a, b, c):
    simplex_m = create_matr(a, b, c)
    m = simplex_m.shape[0] - 1
    lst = [-1 for _ in range(m)]
    b_copy = b.copy()
    x = np.zeros(c.shape)
    while simplex_m[-1].min() < 0:
        col = np.argmin(simplex_m[-1])
        for j in range(m):
            if simplex_m[j, col] > 0:
                b_copy[j] = simplex_m[j, -1] / simplex_m[j, col]
            else:
                b_copy[j] = simplex_m[j, -1]
        row = np.argmin(b_copy)
        pivot = simplex_m[row, col]
        simplex_m[row] /= pivot
        lst[row] = col
        for i in range(m + 1):
            if i != row:
                simplex_m[i] += simplex_m[row] * (-1) * simplex_m[i][col]
    for i in range(m):
        index = lst[i]
        if index > -1:
            x[lst[i]] = simplex_m[i, -1]
    print(x)
    return x