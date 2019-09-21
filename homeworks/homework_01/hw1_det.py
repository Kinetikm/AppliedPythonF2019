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
    boolean = False
    length = len(list_of_lists)
    for i in range(length):
        if length != len(list_of_lists[i]):
            boolean = True
            break
    if boolean or (length < 1):
        return None
    else:
        determinant = 1
        for i in range(length):
            for j in range(length):
                if list_of_lists[i][i] == 0 and list_of_lists[j][i] != 0:
                    for k in range(length):
                        list_of_lists[i][k] = list_of_lists[i][k] + \
                                              list_of_lists[j][k]
                    break
        for i in range(length - 1):
            determinant *= list_of_lists[i][i]
            for j in range(i + 1, length):
                mul = -1 * (list_of_lists[j][i] / list_of_lists[i][i])
                for k in range(i, length):
                    list_of_lists[j][k] += mul * list_of_lists[i][k]
        determinant *= list_of_lists[length - 1][length - 1]
        return determinant
