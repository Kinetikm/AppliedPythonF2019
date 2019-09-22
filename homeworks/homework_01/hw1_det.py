#!/usr/bin/env python
# coding: utf-8
import copy


def SrezMatrix(Matrix, n):
    NewMatrix = copy.deepcopy(Matrix[1:])
    for i in range(len(NewMatrix)):
        NewMatrix[i].pop(n)
    return NewMatrix


def calculate_determinant(list_of_lists):
    '''
        Метод, считающий детерминант входной матрицы,
        если это возможно, если невозможно, то возвращается
        None
        Гарантируется, что в матрице float
        :param list_of_lists: список списков - исходная матрица
        :return: значение определителя или None
        '''
    if len(list_of_lists) == 1 and len(list_of_lists[0]) == 1:
        return list_of_lists[0][0]
    if len(list_of_lists[0]) != len(list_of_lists):
        return None
    sum = 0
    k = 1
    if len(list_of_lists) == 2 and len(list_of_lists[0]) == 2 \
        and len(list_of_lists[1]) == 2:
        return list_of_lists[0][0]*list_of_lists[1][1] - \
            list_of_lists[1][0]*list_of_lists[0][1]
    elif len(list_of_lists) > 2:
        for i in range(len(list_of_lists[0])):
            k += 1
            sum += (-1)**(k) * list_of_lists[0][i] * \
                calculate_determinant(SrezMatrix(list_of_lists, i))
    else:
        return None
    return sum
