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
    if len(list_of_lists) == 0 or len(list_of_lists) != len(list_of_lists[0]):
        return None
    elif len(list_of_lists) == 1:
        return list_of_lists[0][0]
    else:
        minor = 1
        complete_det = 0
        for i in range(len(list_of_lists)):
            subarr = []
            for y in range(1, len(list_of_lists)):
                tmp_str = []
                for k in range(0, len(list_of_lists)):
                    if k != i:
                        tmp_str.append(list_of_lists[y][k])
                subarr.append(tmp_str)

            complete_det = complete_det + list_of_lists[0][i] * minor * calculate_determinant(subarr)
            minor = -minor
    return complete_det
