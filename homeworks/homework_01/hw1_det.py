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
    Нахождение определителя путём приведения матрицы к треугольному виду
    '''
    size = len(list_of_lists)
    if size != len(list_of_lists[0]):
        return
    det = 1
    for i in range(size-1):
        det *= list_of_lists[i][i]
        for j in range(i+1, size):
            multiplier = -1 * (list_of_lists[j][i] / list_of_lists[i][i])
            for k in range(i, size):
                list_of_lists[j][k] += multiplier * list_of_lists[i][k]
    det *= list_of_lists[size-1][size-1]
    return det
