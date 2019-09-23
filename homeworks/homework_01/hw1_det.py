#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):

    def det2(x):
        return x[0][0] * x[1][1] - x[0][1] * x[1][0]

    def minor(x, i, j):
        z = [n for k, n in enumerate(x) if k != i]
        z = [m for k, m in enumerate(zip(*z)) if k != j]
        return z

    def det(x):
        len_x = len(x)
        if len_x == 1:
            return list_of_lists[0][0]
        if len_x == 2:
            return det2(x)

        return sum((-1) ** j * x[0][j] * det(minor(x, 0, j))
                   for j in range(len_x))

    print(det(list_of_lists))
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    raise NotImplementedError
