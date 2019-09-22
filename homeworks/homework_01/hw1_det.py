#!/usr/bin/env python
# coding: utf-8


import copy


def minor(A, i, j):
    temp = copy.deepcopy(A)
    del temp[i]
    for i in range(len(A[0]) - 1):
        del temp[i][j]
    return temp


def calculate_determinant(list_of_lists):
    lines = len(list_of_lists)
    columns = len(list_of_lists[0])
    if lines != columns:
        return None
    if columns == 1:
        return list_of_lists[0][0]
    sign = 1
    det = 0
    for j in range(columns):
        det += list_of_lists[0][j] * sign * calculate_determinant(minor(list_of_lists, 0, j))
        sign *= -1
    return det
