#!/usr/bin/env python
# coding: utf-8

import numpy as np


def step(m):
    col = np.where(m[-1] == m[-1].min())[0][0]
    n = 0
    ind = 0
    for x in range(0, len(m) - 1):
        if m[x, col]:
            if not n:
                n = m[x, -1] / m[x, col]
            elif n > (m[x, -1] / m[x, col]):
                n = m[x, -1] / m[x, col]
                ind = x
    return ind, col


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
    eye = np.concatenate([np.eye(a.shape[0]), np.zeros((1, a.shape[0]))])
    b1 = np.concatenate([b.reshape((b.shape[0], 1)), [[0]]])
    a1 = np.concatenate([a, [c * (-1)]])
    matrix = np.concatenate([a1, eye, b1], axis=1)
    res = np.zeros_like(c) - 1
    return solve(matrix, res)


def solve(matrix, res):
    indexes = step(matrix)
    matrix[indexes[0]] = matrix[indexes[0]] / matrix[indexes]
    for i in range(len(matrix)):
        if i != indexes[0]:
            matrix[i] = matrix[i] - matrix[indexes[0]] * matrix[i, indexes[1]]
    if indexes[0] in res:
        for i in range(len(res)):
            if res[i] == indexes[0]:
                res[i] = -1
    res[indexes[1]] = indexes[0]
    if matrix[-1].min() >= 0:
        result = np.zeros(res.shape[0])
        for i in range(len(res)):
            if res[i] > -1:
                result[i] = matrix[res[i], -1]
        return result
    else:
        return solve(matrix, res)
