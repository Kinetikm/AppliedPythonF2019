#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    import copy

    def minor(list_of_lists, i, j):
        M = copy.deepcopy(list_of_lists)
        del M[i]
        for i in range(len(list_of_lists[0]) - 1):
            del M[i][j]
        return M

    def det(list_of_lists):
        m = len(list_of_lists)
        n = len(list_of_lists[0])
        if m != n:
            return None
        if n == 1:
            return list_of_lists[0][0]
        signum = 1
        determinant = 0
        for j in range(n):
            determinant += list_of_lists[0][j] * signum * det(minor(list_of_lists, 0, j))
            signum *= -1
        return determinant

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
