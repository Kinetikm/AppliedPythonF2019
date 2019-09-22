#!/usr/bin/env python
# coding: utf-8
import copy


def calculate_determinant(list_of_lists):
    res = 0
    n = 0
    m = len(list_of_lists)
    for i in list_of_lists:
        n = len(i)
        if m != n:
            return None
    if n == 1:
        return list_of_lists[0][0]
    for i in range(n):
        x = copy.deepcopy(list_of_lists)
        del x[0]
        for j in range(m - 1):
            del x[j][i]
        res += ((-1)**i) * list_of_lists[0][i] * calculate_determinant(x)
    return res
