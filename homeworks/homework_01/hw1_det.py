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
    n = len(list_of_lists)
    m = len(list_of_lists[0])
    if n != m:
        return None
    if n == 1:
        return list_of_lists[0][0]
    # приводим матрицу к верхнетреугольному виду
    for i in range(n):
        for j in range(m - 1, i, -1):
            if list_of_lists[i][i] != 0:
                koef = list_of_lists[j][i] / list_of_lists[i][i]
            else:
                koef = 0
            temp_list = [koef * item for item in list_of_lists[i]]
            list_of_lists[j] = [b - a for a, b in zip(temp_list, list_of_lists[j])]
    det = 1
    for i in range(n):
        det *= list_of_lists[i][i]
    return det
