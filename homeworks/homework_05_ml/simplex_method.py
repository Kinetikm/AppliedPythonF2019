#!/usr/bin/env python
# coding: utf-8

import numpy as np


def oper(x, y, k):
    return k*x + y
oper_vec = np.vectorize(oper)


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
    n, m = a.shape
    table = np.hstack((np.vstack((a, c*(-1))), np.eye(n+1), np.vstack((b.reshape(n, 1), np.array([0])))))
    x = np.zeros((1, m))[0]
    while np.min(table[-1, :]) < 0:
        mincol = table[-1, :].argmin()
        minrow = (table[:-1, -1]/table[:-1, mincol]).argmin()
        table[minrow, :] = table[minrow, :]/table[minrow, mincol]
        for i in range(n+1):
            if i != minrow:
                table[i, :] = oper_vec(table[minrow, :], table[i, :], -table[i, mincol]/table[minrow, mincol])
    ind = np.where(table[:-1, :m] == 1)
    for i in range(len(ind[1])):
        x[ind[1][i]] = table[ind[0][i], -1]
    return x
