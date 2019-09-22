#!/usr/bin/env python
# coding: utf-8
import copy


def minor(lol, k, n):
    b = copy.deepcopy(lol)
    for i in range(len(b)):
        del b[i][n]
    del b[k]
    return b


def calculate_determinant(list_of_lists):
    if len(list_of_lists) == len(list_of_lists[0]):
        prm = True
    else:
        prm = False
    if prm:
        lol = copy.deepcopy(list_of_lists)
        if len(lol) == 2:
            return lol[0][0] * lol[1][1] - lol[0][1] * lol[1][0]
        s = 0
        for i in range(len(lol)):
            s += lol[0][i]*calculate_determinant(minor(lol, 0, i)) * (-1)**i
        return s
    return None
