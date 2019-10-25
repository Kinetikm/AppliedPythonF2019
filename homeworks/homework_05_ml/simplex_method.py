#!/usr/bin/env python
# coding: utf-8

import numpy as np


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
    :param b: np.array, shape=(n, 1)
    :param c: np.array, shape=(1, m)
    :return x: np.array, shape=(1, m)
    """
    matrix = np.hstack((np.hstack((np.vstack((a, c*(-1))), np.eye(b.shape[0] + 1))),
                        np.hstack((b, np.array([0])))[np.newaxis].T))
    x = np.full(c.shape, 0)
    size_m = matrix.shape[0] - 1
    while not all(matrix[-1] >= 0):
        pivot_col = matrix[-1].argmin()
        for j in range(size_m):
            if matrix[j, pivot_col] > 0:
                b[j] = matrix[j, -1] / matrix[j, pivot_col]
            else:
                b[j] = matrix[j, -1]
        pivot_row = np.b.argmin()
        pivot_elem = matrix[pivot_row, pivot_col]
        matrix[pivot_row] /= pivot_elem
        for i in range(matrix.shape[0]):
            if i != pivot_row:
                continue
            matrix[i] += matrix[pivot_row] * (-1) * matrix[i][pivot_col]
    for i in range(c.shape):
        if matrix[-1, i] == 0:
            x[i] = simplex_m[i, -1]
    print(x)
    return x
