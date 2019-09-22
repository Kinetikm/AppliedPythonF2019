#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    res = 1
    l = len(list_of_lists)
    eps = 1e-15
    for i in range(l):
        if len(list_of_lists[i]) != l:
            return None
    for i in range(l):
        check = i
        for j in range(i + 1, l):
            if abs(list_of_lists[j][i]) > abs(list_of_lists[check][i]):
                check = j
        if abs(list_of_lists[check][i]) < eps:
            return 0
        list_of_lists[i], list_of_lists[check] = list_of_lists[check], list_of_lists[i]
        if i != check:
            res *= -1
        res *= list_of_lists[i][i]
        for j in range(i + 1, l):
            list_of_lists[i][j] /= list_of_lists[i][i]
        for j in range(l):
            if j != i and abs(list_of_lists[j][i]) > eps:
                for k in range(i + 1, l):
                    list_of_lists[j][k] -= list_of_lists[i][k] * list_of_lists[j][i]
    return res


