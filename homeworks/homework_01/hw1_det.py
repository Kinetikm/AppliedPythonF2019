#!/usr/bin/env python
# coding: utf-8

EPS = 1e-9


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''

    # print("here", list_of_lists)

    n = len(list_of_lists)
    for sublist in list_of_lists:
        if len(sublist) != n:
            return None

    det = 1
    for i in range(n):
        k = i
        for j in range(i+1, n):
            if abs(list_of_lists[j][i]) > abs(list_of_lists[k][i]):
                k = j
        # print("k", k)
        if abs(list_of_lists[k][i]) < EPS:
            return 0

        tmp = list_of_lists[i]
        list_of_lists[i] = list_of_lists[k]
        list_of_lists[k] = tmp

        if (i != k):
            det = -det

        det *= list_of_lists[i][i]

        for j in range(i+1, n):
            list_of_lists[i][j] /= list_of_lists[i][i]

        for j in range(n):
            if j != i and abs(list_of_lists[j][i]) > EPS:
                for k in range(i+1, n):
                    list_of_lists[j][k] -= list_of_lists[i][k] * list_of_lists[j][i]

    # print("res:", det)
    # print(list_of_lists)
    return det
