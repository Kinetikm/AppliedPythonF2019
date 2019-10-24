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

    # Блок первоначальной подгтовки симплекс матрицы
    simplex_mat = np.vstack((a, c * (-1)))
    simplex_mat = np.hstack((simplex_mat, np.eye(b.shape[0] + 1)))
    temp_mat = np.hstack((b, np.array([0])))[np.newaxis].transpose()
    simplex_mat = np.hstack((simplex_mat, temp_mat))
    print(simplex_mat)

    # Блок основных вычисления
    accessory_b_mat = b.copy()
    temp_row = [-1 for _ in range(simplex_mat.shape[0] - 1)]
    # Пробегаемся по поcледней строке в поисках разрежающего столбца и строки
    while simplex_mat[simplex_mat.shape[0] - 1, :].min() < 0:
        pivot_column = np.argmin(simplex_mat[simplex_mat.shape[0] - 1, :])
        for i in range(simplex_mat.shape[0] - 1):
            if simplex_mat[i, pivot_column] <= 0:
                accessory_b_mat[i] = simplex_mat[i, simplex_mat.shape[1] - 1]
            else:
                accessory_b_mat[i] = simplex_mat[i, simplex_mat.shape[1] - 1] / simplex_mat[i, pivot_column]
        pivot_row = np.argmin(accessory_b_mat)
        temp_row[pivot_row] = pivot_column
        elem = simplex_mat[pivot_row, pivot_column]
        simplex_mat[pivot_row] = simplex_mat[pivot_row] / elem
        for i in range(simplex_mat.shape[0]):
            if i != pivot_row:
                simplex_mat[i] = simplex_mat[i] + simplex_mat[pivot_row] * (-1) * simplex_mat[i][pivot_column]

    x = np.zeros(c.shape)
    for i in range(simplex_mat.shape[0] - 1):
        index = temp_row[i]
        if index > -1:
            x[temp_row[i]] = simplex_mat[i, simplex_mat.shape[1] - 1]

    print(x)
    return x


a = np.array([[2, 3, 2], [1, 1, 2]])
print(a.shape)
b = np.array([1000,  800])
print(b.shape)
c = np.array([7,  8, 10])
print(c.shape)
simplex_method(a, b, c)
