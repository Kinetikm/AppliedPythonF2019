#!/usr/bin/env python
# coding: utf-8


import copy


def calculate_determinant(list_of_lists):
    return(determinant(list_of_lists))


def minor(list_of_lists, row, col):
    copy_list = copy.deepcopy(list_of_lists)
    for k in range(len(list_of_lists)):
        del copy_list[k][col]
    del copy_list[row]
    return copy_list


def determinant(list_of_list):
    m = len(list_of_list)
    n = len(list_of_list[0])
    if (m != n):
        return None
    elif (n == 1):
        return list_of_list[0][0]
    coeff = 1
    det = 0
    for i in range(n):
        det += list_of_list[0][i] * coeff * determinant(minor(list_of_list, 0, i))
        coeff *= (-1)
    return det
