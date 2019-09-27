#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    """
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    """

    h = len(list_of_lists)
    for i in range(h):
        if (len(list_of_lists[i]) != h):
            return None
    res = det(list_of_lists)
    return res


def cut(a, idel, jdel):
    p = 0
    k = 0
    res = [0] * (len(a) - 1)
    for i in range(len(a) - 1):
        res[i] = [0] * (len(a) - 1)
    for i in range(len(a) - 1):
        if i == idel:
            p += 1
        for j in range(len(a) - 1):
            if j == jdel:
                k += 1
            res[i][j] = (a[(i + p)][(j + k)])
        k = 0
    return res


def det(a):
    if (len(a) == 1):
        return a[0][0]
    else:
        res = 0
        for j in range(len(a)):
            temp = cut(a, 0, j)
            res = res + (a[0][j]) * ((-1) ** (0 + j)) * det(temp)
    return res
