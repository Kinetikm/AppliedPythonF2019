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
    n = a.shape[0]
    mat = np.vstack((a, -c))
    mat = np.hstack((mat, np.eye(n + 1)))
    mat = np.hstack((mat, np.vstack((b.reshape(-1, 1), np.zeros((1, 1))))))
    l = len(mat[n, :])
    while (mat[n, :] < 0).any():
        m = mat[n, 0]
        ind_1 = 0
        for i in range(l):
            if mat[n, i] < m:
                ind_1 = i
                m = mat[n, i]
        temp = mat[0, l - 1] / mat[0, ind_1]
        ind_2 = 0
        for i in range(n):
            if mat[i, l - 1] / mat[i, ind_1] < temp:
                temp = mat[i, l - 1] / mat[i, ind_1]
                ind_2 = i
        mat[ind_2, :] = mat[ind_2, :] / mat[ind_2, ind_1]
        for row in range(n + 1):
            if row != ind_2:
                mat[row, :] += -1 * mat[ind_2, :] * mat[row, ind_1]
    x = np.zeros((1, a.shape[1]))
    for row in range(n):
        for col in range(a.shape[1]):
            if mat[row, col] == 1.0:
                x[0, col] = mat[row, l - 1]
    return x[0]
