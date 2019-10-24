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
    res = np.zeros(m)
    neg = np.zeros(n)
    neg.fill(-1)

    s_matrix = np.hstack((a, np.eye(n), np.zeros((n, 1)), b.reshape((n, 1))))
    last_row = np.hstack((c * (-1), np.zeros(n), np.array([1, 0])))
    s_matrix = np.vstack((s_matrix, last_row))

    while s_matrix[-1].min() < 0:
        col = s_matrix[-1].argmin()
        min_in_pivot = None
        row = None

        for i in range(len(b)):
            if s_matrix[i][col] == 0:
                continue
            value = s_matrix[i][-1] / s_matrix[i][col]
            if min_in_pivot is None or min_in_pivot > value:
                min_in_pivot = value
                row = i

        s_matrix[row] = s_matrix[row] / s_matrix[row][col]

        for row in s_matrix:
            if np.array_equal(row, s_matrix[row]):
                continue
            row -= s_matrix[row] * row[col]
        neg[row] = col

    for i in range(n):
        t = neg[i]
        if t != -1:
            res[int(t)] = s_matrix[i][-1]
    return res
