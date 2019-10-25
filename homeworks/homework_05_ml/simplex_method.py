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
    last_row = a.shape[0]
    table = np.vstack((a, c*(-1)))
    table = np.concatenate((table, np.eye(last_row + 1)), axis=1)
    table = np.concatenate((table, np.vstack((np.array([b]).T, [0]))), axis=1)
    x_place = [-1 for i in range(last_row)]

    while np.signbit(table[last_row]).any():
        min_el_col = min(table[last_row])
        pivot_column = np.argmin(table[last_row])

        simplex_ratio = table[:-1, table.shape[1] - 1] / table[:-1, pivot_column]

        min_el_row = min(simplex_ratio)
        pivot_row = np.argmin(simplex_ratio)
        min_el_row = table[pivot_row][pivot_column]

        table[pivot_row, :] = table[pivot_row] / min_el_row
        if pivot_column in x_place:
            x_place[x_place.index(pivot_column)] = -1
        x_place[pivot_row] = pivot_column

        pivot = np.array([table[pivot_row]])

        coef = np.array([table[0:pivot_row, pivot_column] * (-1)]).T
        table[0:pivot_row] = coef @ pivot + table[0:pivot_row]
        coef = np.array([table[pivot_row + 1:last_row + 1, pivot_column] * (-1)]).T
        table[pivot_row + 1:last_row + 1, :] = coef @ pivot + table[pivot_row + 1:last_row + 1]

    x = [0 for i in range(len(c))]
    for i in range(len(x_place)):
        if x_place[i] != -1:
            x[x_place[i]] = round(table[i][table.shape[1] - 1], 2)

    return x
