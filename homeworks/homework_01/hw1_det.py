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

    if len(list_of_lists) != len(list_of_lists[0]):  # Матрица не квадратная
        return None
    else:
        for i in range(len(list_of_lists) - 1):
            for k in range(i + 1, len(list_of_lists)):
                if list_of_lists[i][i] != 0:
                    a = list_of_lists[k][i] / list_of_lists[i][i]
                    for j in range(i, len(list_of_lists)):
                        list_of_lists[k][j] -= a * list_of_lists[i][j]

    deter = 1
    for i in range(len(list_of_lists)):
        deter *= list_of_lists[i][i]

    return deter
