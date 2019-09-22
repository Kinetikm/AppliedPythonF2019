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

    for i in range(len(list_of_lists)):
        if len(list_of_lists[i]) != len(list_of_lists):
            return None

    for i in range(len(list_of_lists)):
        for j in range(i+1, len(list_of_lists)):
            subtract_row(list_of_lists[j], list_of_lists[i], list_of_lists[j][i] / list_of_lists[i][i])

    s = 1
    for i in range(len(list_of_lists)):
        s *= list_of_lists[i][i]

    return s


def subtract_row(row1, row2, k):
    for i in range(len(row1)):
        row1[i] -= k * row2[i]
