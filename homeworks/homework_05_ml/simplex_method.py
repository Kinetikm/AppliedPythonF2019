#!/usr/bin/env python
# coding: utf-8

import numpy as np


def simplex_method(a, b, c):
    n, m = a.shape[0], a.shape[1]
    b = b.reshape(n, 1)
    c = c.reshape(1, m)
    c *= -1
    c = np.hstack((c, np.zeros((1, n))))
    b = np.vstack((b, [[0]]))
    simplex_matrix = np.hstack((np.vstack((np.hstack((a, np.eye(n))), c)), b))
    basis = -1 * np.ones(n, dtype=np.int16)
    result = np.zeros(m)
    while True:
        if min(simplex_matrix[-1, :-1]) >= 0:
            break
        pivot_column = np.argmin(simplex_matrix[-1, :-1])
        pivot_row = np.argmin(simplex_matrix[:-1, -1] / simplex_matrix[:-1, pivot_column])
        basis[pivot_row] = pivot_column
        np.divide(simplex_matrix[pivot_row], simplex_matrix[pivot_row, pivot_column], out=simplex_matrix[pivot_row])
        for i in range(n+1):
            if i == pivot_row:
                continue
            simplex_matrix[i] -= simplex_matrix[pivot_row] * (simplex_matrix[i, pivot_column] / simplex_matrix[pivot_row, pivot_column])
    for i in range(n):
        if basis[i] != -1:
            result[basis[i]] = simplex_matrix[i, -1]
    return result

