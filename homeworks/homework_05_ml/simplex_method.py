#!/usr/bin/env python
# coding: utf-8

import numpy as np


def s_matrixethod(a, b, c):
    """
    Почитать про симплекс метод простым языком:
    * https://  https://ru.wikibooks.org/wiki/Симплекс-метод._Простое_объяснение
    Реализацию алгоритма взять тут:
    * https://youtu.be/gRgsT9BB5-8 (это ссылка на 1-ое из 5 видео).

    Используем numpy и, в целом, векторные операции.

    a * x.T <= b
    c * x.T -> max
    :param a: np.array, shape=(n, m)
    :param b: np.array, shape=(n, 1)
    :param c: np.array, shape=(1, m)
    :return x: np.array, shape=(1, m)
    """
    n, m = a.shape
    x = np.zeros(m)
    s = np.zeros(n)
    s.fill(-1)

    simplex_m = np.hstack((a, np.eye(n), np.zeros((n, 1)), b.reshape((n, 1))))
    last_row = np.hstack((c * (-1), np.zeros(n), np.array([1, 0])))
    simplex_m = np.vstack((simplex_m, last_row))

    while simplex_m[-1].min() < 0:
        pivot_col = simplex_m[-1].argmin()
        min_in_pivot = None
        pivot_row = None

        for i in range(len(b)):
            if simplex_m[i][pivot_col] == 0:
                continue
            value = simplex_m[i][-1] / simplex_m[i][pivot_col]
            if min_in_pivot is None or min_in_pivot > value:
                min_in_pivot = value
                pivot_row = i

        simplex_m[pivot_row] = simplex_m[pivot_row] / simplex_m[pivot_row][pivot_col]

        for row in simplex_m:
            if np.array_equal(row, simplex_m[pivot_row]):
                continue
            row -= simplex_m[pivot_row] * row[pivot_col]
        s[pivot_row] = pivot_col

    for i in range(n):
        col = s[i]
        if col != -1:
            x[int(col)] = simplex_m[i][-1]
    return x
