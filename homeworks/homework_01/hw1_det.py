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
    if len(list_of_lists) == 0:
        return None
    elif len(list_of_lists) == 2:
        return list_of_lists[0][0] * list_of_lists[1][1] - list_of_lists[0][1] * list_of_lists[1][0]
    else:
        minor = 1
        ilog = 0
        for i in range(len(list_of_lists)):
            kek = []
            for y in range(1, len(list_of_lists)):
                lol = []
                for k in range(0, len(list_of_lists)):
                    if k != i:
                        lol.append(list_of_lists[y][k])
                kek.append(lol)

            ilog = ilog + list_of_lists[0][i] * minor * calculate_determinant(kek)
            minor = -minor
    return ilog
