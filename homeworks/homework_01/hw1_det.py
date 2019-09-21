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

    ll = list_of_lists
    m = len(ll)
    n = len(ll[0])
    if m != n:
        return None
    if m == 1:
        return ll[0][0]
    det = 0
    sign = 1
    for i in range(n):
        det += sign * ll[0][i] * calculate_determinant([[el for el in ll[j][:i] + ll[j][i + 1:]] for j in range(1, m)])
        sign *= -1
    return det
