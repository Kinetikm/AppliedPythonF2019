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
    first_row = [1] * len(list_of_lists)
    Minor = [1] * len(list_of_lists)
    if len(list_of_lists) != len(list_of_lists[0]) or len(list_of_lists) == 0:
        return None
    elif len(list_of_lists) == 1:
        return list_of_lists[0][0]
    else:
        for i in range(len(list_of_lists)):
            first_row[i] = (-1)**(i) * list_of_lists[0][i]
        # print("first row\n",first_row)
        for j in range(len(list_of_lists)):
            Minor[j] =\
                calculate_determinant(minor_on_the_first_row(list_of_lists, j))
        # print("new minor",Minor)
        r = [1] * len(first_row)
        for k in range(len(first_row)):
            r[k] = first_row[k] * Minor[k]
        # print(r)
        sum = 0
        for x in r:
            sum += x
            print(sum)
    return sum


def minor_on_the_first_row(list_of_list, a):
    lenght = len(list_of_list)
    new_list = [[1] * lenght for i in range(lenght)]
    for i in range(lenght):
        for j in range(lenght):
            new_list[i][j] = list_of_list[i][j]
    new_list.pop(0)
    for i in range(len(new_list)):
        new_list[i].pop(a)
    return new_list
