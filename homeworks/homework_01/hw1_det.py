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

    lenOut = len(list_of_lists)
    checker = True
    if lenOut == 0:
        return None
    for i in range(lenOut):
        if lenOut != len(list_of_lists[i]):
            checker = False
    if checker:
        return solve(list_of_lists, 1)
    else:
        return None


def solve(matrix, mul):  # задаём функцию, которая считает определитель
    width = len(matrix)  # размер
    if width == 1:
        return mul * matrix[0][0]  # множитель
    else:
        sign = -1
        total = 0
        for i in range(width):
            m = []
            for j in range(1, width):
                buff = []
                for k in range(width):
                    if k != i:
                        buff.append(matrix[j][k])
                m.append(buff)
            sign *= -1
            total += mul * solve(m, sign * matrix[0][i])
        return total
