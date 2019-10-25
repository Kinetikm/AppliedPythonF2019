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
    matrix_ = np.vstack((a, -c))
    matrix_ = np.hstack((matrix_, np.eye(matrix_.shape[0])))
    b = b.reshape(-1, 1)
    x = np.zeros(c.shape)
    matrix_ = np.hstack((matrix_, np.vstack((b, np.zeros((1, 1))))))
    res = [-1 for _ in range(matrix_.shape[0])]
    while min(matrix_[-1, :]) < 0:
        col = np.argmin(matrix_[-1, :])
        row = np.argmin(matrix_[:-1, -1] / matrix_[:-1, col])
        matrix_[row, :] /= matrix_[row, col]
        for i in range(matrix_.shape[0]):
            if i != row:
                matrix_[i] += matrix_[row] * (-matrix_[i, col])
        res[row] = col
    for i in range(len(res)):
        if res[i] != -1:
            x[res[i]] = matrix_[i, -1]
    return x
