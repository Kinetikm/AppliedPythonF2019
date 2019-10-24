#!/usr/bin/env python
# coding: utf-8

import numpy as np


def define_mark(simplex_table, C_bas, n, m, c):
    delta = np.zeros(n + m)
    for i in range(n + m):
        flag = False
        for j in range(n):
            delta[i] += simplex_table[j][i] * C_bas[j]
            if simplex_table[j][i] > 0:
                flag = True
        delta[i] -= c[i]
        if delta[i] < 0 and flag is False:
            return -1
    if min(delta).round(4) < 0:
        return delta.argmin()
    else:
        return -2


def changing_basis(arg_vvod, simplex_table, A0, n):
    x = None
    vichod = None
    for i in range(n):
        if simplex_table[i][arg_vvod] != 0:
            buf = A0[i] / simplex_table[i][arg_vvod]
            if buf > 0 and (x is None or buf < x):
                x = buf
                vichod = i
    return vichod


def changing_simplex_table(simplex_table, vichod, vvod, n, m, A0):
    buf = simplex_table[vichod][vvod]
    simplex_table[vichod] /= buf
    A0[vichod] /= buf
    for i in range(n):
        buf = simplex_table[i][vvod]
        if i != vichod:
            A0[i] -= A0[vichod] * buf
            for j in range(n + m):
                simplex_table[i][j] -= buf * simplex_table[vichod][j]

    return A0, simplex_table


def simplex_method(a, b, c):
    """
    a * x.T <= b
    c * x.T -> max
    :param a: np.array, shape=(n, m)
    :param b: np.array, shape=(n, 1)
    :param c: np.array, shape=(1, m)
    :return x: np.array, shape=(1, m)
    """
    a = a.astype(float)
    b = b.astype(float)
    c = c.astype(float)
    n, m = a.shape
    simplex_table = np.zeros((n, n + m), dtype=float)
    C_bas = [0] * n
    A0 = b
    basis = [i + m for i in range(n)]
    c = np.append(c, np.zeros(n))

    for i in range(n):
        for j in range(m):
            simplex_table[i][j] = a[i][j]
        for j in range(n):
            if i == j:
                simplex_table[i][m + j] = 1
            else:
                simplex_table[i][m + j] = 0

    while True:
        delta = define_mark(simplex_table, C_bas, n, m, c)
        if delta == -1:
            return "не ограничена, максимум достигается на бесконечности"
        if delta == -2:
            result = [0]*m
            for i in range(n):
                if basis[i] < m:
                    result[basis[i]] = A0[i].round(4)
            return result

        vichod = changing_basis(delta, simplex_table, A0, n)
        basis[vichod] = delta
        A0, simplex_table = changing_simplex_table(simplex_table, vichod, delta, n, m, A0)
        C_bas[vichod] = c[delta]
