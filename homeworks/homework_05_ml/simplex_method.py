#!/usr/bin/env python
# coding: utf-8

import numpy as np


def simplex_table(a, b, c):
    n, m = a.shape
    table = np.zeros((n + 1, m + n + 1 + 1), dtype=float)

    table[0:n, 0:m] = a
    table[n, 0:m] = -c
    table[0:, m:m + n + 1] = np.eye(n + 1)
    table[0:n, -1] = b[:]

    return table

def pivot_num(table):
    b = np.copy(table[:-1, -1])

    col = np.argmin(table[-1])  # получим pivot column

    for i in range(table.shape[0]-1):
        b[i] /= table[i, col]

    row = np.argmin(b)  # пересечение row и col будет pivot number
    return row, col


def row_elimination(table, prow, pcol):
    k = table[prow, pcol]
    table[prow] /= k

    for i in range(table.shape[0]):
        if i == prow:
            continue
        table[i] += table[prow] * -np.sign(table[i, pcol]) * abs(table[i, pcol])


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

    table = simplex_table(a, b, c)
    _, m = a.shape
    pnumbers = {}  # запоминаем, какой строке соответствует какой Х
    while table[-1].min() < 0:
        prow, pcol = pivot_num(table)
        pnumbers[prow] = pcol
        row_elimination(table, prow, pcol)

    x = [0] * m
    for num in pnumbers:
        x[pnumbers[num]] = table[:, -1][num]

    return np.array(x)
