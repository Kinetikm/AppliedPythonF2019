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
    if len(list_of_lists) != len(list_of_lists[0]):
        return None
    elif len(list_of_lists) == 1:
        return list_of_lists[0][0]
    elif len(list_of_lists) == 2:
        return list_of_lists[0][0]*list_of_lists[1][1] - list_of_lists[1][0]*list_of_lists[0][1]
    else:
        sum = 0
        for i in range(len(list_of_lists)):
            sublist = []
            for j in range(len(list_of_lists)):
                if i != j:
                    sublist += [list_of_lists[j][1::]]
            sum += ((-1)**(2+i))*list_of_lists[i][0]*calculate_determinant(sublist)
        return sum
