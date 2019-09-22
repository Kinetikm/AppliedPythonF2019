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
    for i in range(len(list_of_lists)):
        if len(list_of_lists) != len(list_of_lists[i]):
            return None
    n = len(list_of_lists)
    det = 1
    for i in range(n):
        print(i)
        j = i
        while (j < n) and (list_of_lists[i][j] == 0):
            j += 1
        if list_of_lists[i][j] == 0:
            return 0
        if j != i:
            for g in range(n):
                list_of_lists[g][i] += list_of_lists[g][j]
        for k in range(i + 1, n):
            alpha = list_of_lists[k][i]
            for g in range(n):
                list_of_lists[k][g] -= alpha * list_of_lists[i][g] / list_of_lists[i][i]
        print(list_of_lists)
        det *= list_of_lists[i][i]
    return det
