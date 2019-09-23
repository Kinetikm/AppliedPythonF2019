#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(m):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    if len(m) <= 1:
        return None
    elif len(m) != len(m[0]):
        return None
    elif len(m) == 2:
        return m[0][0]*m[1][1] - m[0][1]*m[1][0]
    else:
        det = 1
        for k in range(len(m)):
            if m[k][k] == 0:
                return 0
            det *= m[k][k]
            for i in range(k+1, len(m)):
                m[i] = [m[i][j]-m[k][j]*m[i][k]/m[k][k] for j in range(len(m))]
        return det
