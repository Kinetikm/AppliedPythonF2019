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
    mas = list_of_lists
    for i in range(len(mas)):
        if (len(mas) != len(mas[i])):
            return None

    k = 0
    while (k < len(mas)):
        glav_el = mas[k][k]
        if (mas[k][k] == 0) and (k + 1 != len(mas)):
            for j in range(len(mas)):
                mas[k][j] = mas[k][j] + mas[k + 1][j]
            glav_el = mas[k][k]
        for i in range(len(mas)):
            if (i > k):
                delitel = mas[i][k] / glav_el
                for j in range(len(mas[i])):
                    if (j >= k):
                        mas[i][j] = mas[i][j] - mas[k][j] * delitel
        k += 1
    det = 1
    for k in range(len(mas)):
        det = det * mas[k][k]
    return det
