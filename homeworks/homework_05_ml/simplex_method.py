#!/usr/bin/env python
# coding: utf-8

import numpy as np


def construct_matrix(a, b, c):
    tmp_a = a.copy()
    tmp_b = b.copy()
    tmp_c = c.copy() * (-1)
    right = np.hstack((tmp_b, np.array([0])))[np.newaxis].T
    left = np.vstack((tmp_a, tmp_c))
    left = np.hstack((left, np.eye(b.shape[0] + 1)))
    matrix = np.hstack((left, right))
    return matrix


def simplex_method(a, b, c):
    """
    Почитать про симплекс метод простым языком:
    * https://  https://ru.wikibooks.org/wiki/Симплекс-метод._Простое_объяснение
    Реализацию алгоритма взять тут:
    * https://youtu.be/gRgsT9BB5-8 (это ссылка на 1-ое из 5 видео).

    Используем numpy и, в целом, векторные операции.

    a * x.T <= b
    c * x.T -> max
    :param a: np.array, shape=(n, m)
    :param b: np.array, shape=(1, n)
    :param c: np.array, shape=(1, m)
    :return x: np.array, shape=(1, m)
    """

    simplex_matrix = construct_matrix(a, b, c)
    m = simplex_matrix.shape[0] - 1
    n = simplex_matrix.shape[1] - 1
    tmp = [-1 for _ in range(m)]
    tmp_b = b.copy()
    x = np.zeros(c.shape)
    while simplex_matrix[-1].min() < 0:
        pivot_col = np.argmin(simplex_matrix[-1])
        for j in range(m):
            if simplex_matrix[j, pivot_col] > 0:
                tmp_b[j] = simplex_matrix[j, -1] / simplex_matrix[j, pivot_col]
            else:
                tmp_b[j] = simplex_matrix[j, -1]
        pivot_row = np.argmin(tmp_b)
        pivot = simplex_matrix[pivot_row, pivot_col]
        simplex_matrix[pivot_row] /= pivot
        tmp[pivot_row] = pivot_col
        for i in range(m + 1):
            if i != pivot_row:
                simplex_matrix[i] += simplex_matrix[pivot_row] * (-1) * simplex_matrix[i][pivot_col]
    for i in range(m):
        index = tmp[i]
        if index > -1:
            x[tmp[i]] = simplex_matrix[i, -1]
    print(x)
    return x
