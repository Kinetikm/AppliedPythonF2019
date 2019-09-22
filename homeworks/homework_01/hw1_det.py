#!/usr/bin/env python
# coding: utf-8


def srez(l, x):
    nl = []
    k = 0
    for i in range(1, len(l)):
        nl.append([])
        for j in range(0, len(l[0])):
            if j != x:
                nl[k].append(l[i][j])
        k += 1
    return nl


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    l = list_of_lists
    if len(l) == 0 or len(l) == 1 and len(l[0]) == 0 or len(l) != len(l[0]):
        return None
    if len(l) == 1 and len(l[0]) != 0:
        return l[0][0]
    if len(l) > 2:
        det = 0
        for i in range(0, len(l)):
            det += l[0][i] * ((-1) ** i) * calculate_determinant(srez(l, i))
        return det
    else:
        return l[0][0] * l[1][1] - l[0][1] * l[1][0]
