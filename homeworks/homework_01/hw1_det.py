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
    raise NotImplementedError
    mult = 1
    ind = 0
    A = list_of_lists
    for i in range(len(A)):
        if len(A) != len(A[i]):
            return None
    i = 0
    if len(A) == 2 and len(A[0]) == 2:
        det2x2 = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return det2x2
    for i in range(len(A[0]) - 1):
        delit = 0
        j = 0
        while delit == 0 and j < len(A):
            delit = A[i][j]
            ind = j
            j += 1
        if delit == 0:
            return 0
        j = 0
        for j in range(len(A)):
            A[i][j] /= delit
        j = 0
        for j in range(i, len(A)):
            k = A[j][i]
            A[j][i] = A[j][ind]
            A[j][ind] = k
        if ind == i:
            mult = mult * delit
        else:
            mult = -1 * mult * delit
        for l in range(i + 1, len(A)):
            deli = A[l][i]
            for d in range(i, len(A)):
                A[l][d] -= A[i][d] * deli
    det = A[len(A) - 1][len(A) - 1] * mult
    return det
