#!/usr/bin/env python
# coding: utf-8
import copy


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    res = 0
    A = list_of_lists
    if (len(A) != len(A[0])):
        return None
    if (len(A) == 2):
        return A[0][0] * A[1][1] - A[1][0] * A[0][1]
    if (len(A) == 1):
        return A[0][0]

    for i in range(len(A)):    # иду по строке, i-номер столбца
        res += (-1)**(2+i) * A[0][i] * calculate_determinant(minor(A, 0, i))
    return res


def minor(A, i, j):
    M = copy.deepcopy(A)
    del M[i]      # удалил текущую строку
    for i in range(len(A[0]) - 1):
        del M[i][j]    # удалил текущий столбец
    return M
