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

    import copy

    def magic(list_of_lists, j):
        M = copy.deepcopy(list_of_lists)
        for list in M:
            for i in range(len(list)):
                if i == j:
                    list.pop(j)
        M.pop(0)
        return (M)

    for list in list_of_lists:
        if len(list_of_lists) != len(list):
            return None

    det = 0
    if len(list_of_lists) == 1:
        return list_of_lists[0][0]

    elif len(list_of_lists) == 2:
        return list_of_lists[0][0] * list_of_lists[1][1] - list_of_lists[0][1] * list_of_lists[1][0]

    else:
        for j in range(len(list_of_lists)):
            det += ((-1) ** (2 + j)) * list_of_lists[0][j] * calculate_determinant(magic(list_of_lists, j))
    return det
