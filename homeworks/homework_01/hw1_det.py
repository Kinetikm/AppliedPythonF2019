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
    def check_correctly(arr):
        n = len(arr)
        for elem in arr:
            if n != len(elem):
                return False
        return True
    if not check_correctly(list_of_lists):
        return None

    def minus_vec(a, b, k=1):
        return [a[i] - k * b[i] for i in range(len(a))]

    def plus_vec(a, b, k=1):
        return [a[i] + k * b[i] for i in range(len(a))]

    n = len(list_of_lists)
    for i in range(n):
        if abs(list_of_lists[i][i]) < 10e-5:
            for j in range(i + 1, n):
                if abs(list_of_lists[j][i]) > 10e-5:
                    list_of_lists[i] = plus_vec(list_of_lists[i],
                                                list_of_lists[j])
            if abs(list_of_lists[i][i]) < 10e-5:
                return 0
        for j in range(i + 1, n):
            k = list_of_lists[j][i] / list_of_lists[i][i]
            list_of_lists[j] = minus_vec(list_of_lists[j],
                                         list_of_lists[i], k)

    t = 1
    for i in range(n):
        t *= list_of_lists[i][i]
    return t
