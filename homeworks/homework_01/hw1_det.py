#!/usr/bin/env python
# coding: utf-8

import copy


def minor(list_of_lists, j):
    m = copy.deepcopy(list_of_lists)
    del m[0]
    for i in range(len(m)):
        del m[i][j]
    return m


def calculate_determinant(list_of_lists):
    a = len(list_of_lists)
    b = len(list_of_lists[0])
    if a != b:
        return
    if a == 1:
        return list_of_lists[0][0]
    det = 0
    for j in range(a):
        if j % 2 == 0:
            det = det + list_of_lists[0][j] * calculate_determinant(minor(list_of_lists, j))
        else:
            det = det - list_of_lists[0][j] * calculate_determinant(minor(list_of_lists, j))
    return det
