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
    def calc_matrix(mass, ind):
        result = []
        for line in range(1, len(mass)):
            result.append(mass[line][:ind] + mass[line][ind+1:])
        return result

    if len(list_of_lists) == 0 or len(list_of_lists) != len(list_of_lists[0]):
        return None
    if len(list_of_lists) == 1:
        return list_of_lists[0]

    if len(list_of_lists[0]) == 2:
        return list_of_lists[0][0] * list_of_lists[1][1] - list_of_lists[0][1] * list_of_lists[1][0]

    res = 0
    for j in range(len(list_of_lists[0])):
        i = 1 if j%2 == 0 else -1
        res += i * list_of_lists[0][j] * calculate_determinant(calc_matrix(list_of_lists, j))
    return res
