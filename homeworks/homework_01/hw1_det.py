#!/usr/bin/env python
# coding: utf-8
import copy


def minor(lol, k, n):
    b = copy.deepcopy(lol)
    for i in range(len(b)):
        del b[i][n]
    del b[k]
    return b


def check(list_of_lists):
    if list_of_lists == []:
        return False
    lenth = len(list_of_lists)
    for i in range(len(list_of_lists)):
        if len(list_of_lists[i]) != lenth:
            return False
    return True


def rec_func(lol):
    if len(lol) == 1:
        return lol[0][0]
    if len(lol) == 2:
        return lol[0][0] * lol[1][1] - lol[0][1] * lol[1][0]
    s = 0
    for i in range(len(lol)):
        s += lol[0][i]*calculate_determinant(minor(lol, 0, i)) * (-1)**i
    return s


def calculate_determinant(list_of_lists):
    if check(list_of_lists):
        return rec_func(list_of_lists)
    else:
        return None
