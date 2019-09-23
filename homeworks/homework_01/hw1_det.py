#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(s):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param s: список списков - исходная матрица
    :return: значение определителя или None
    '''
    res = 1
    N = len(s)
    for i in range(N):
        j = max(range(i, N), key=lambda k: abs(s[k][i]))
        if len(s) != len(s[i]):
            return
        if i != j:
            s[i], s[j] = s[j], s[i]
            res *= -1
        if s[i][i] == 0:
            return 0
        res *= s[i][i]
        for j in range(i + 1, N):
            b = s[j][i] / s[i][i]
            s[j] = [s[j][k] - b * s[i][k] for k in range(N)]
    return res


#
# s = [[1, 2, 3], [4, 5, 6], [2, 5, 3]]
# print(calculate_determinant(s))