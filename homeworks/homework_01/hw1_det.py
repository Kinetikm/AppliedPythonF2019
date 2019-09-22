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

    # решение
    def __calculate_determinant(ll):
        rg = len(ll)
        if rg == 1:
            return ll[0][0]
        det = 0
        sign = 1
        for i in range(rg):
            det += sign * ll[0][i] * __calculate_determinant(
                [[el for el in ll[j][:i] + ll[j][i + 1:]] for j in range(1, rg)])
            sign *= -1
        return det

    # проверка
    m = len(list_of_lists)
    for item in list_of_lists:
        if len(item) != m:
            return None
    return __calculate_determinant(list_of_lists)
