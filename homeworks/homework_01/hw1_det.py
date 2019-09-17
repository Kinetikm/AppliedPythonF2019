#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    M = list_of_lists
    if len(M) != len(M[0]):
        return None
    else:
        if len(M) == 2:
            return M[0][0] * M[1][1] - M[0][1] * M[1][0]
        elif len(M) == 1:
            return M[0][0]
        elif len(M) == 0:
            return None
        else:
            return sum([(-1) ** (i) * M[0][i] * calculate_determinant(
                minor(M, i)) for i in range(len(M))])
    raise NotImplementedError


def minor(M, c):
    m = [[1] * len(M) for i in range(len(M))]
    for i in range(len(M)):
        for j in range(len(M)):
            m[i][j] = M[i][j]
    m.pop(0)

    for i in range(len(m)):
        m[i].pop(c)
    return m
