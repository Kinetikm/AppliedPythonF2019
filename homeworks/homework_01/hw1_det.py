#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    res = 1
    eps = 1e-15
    n = len(list_of_lists)
    for i in range(n):
        if list_of_lists[i] != n:
            return None
    for i in range(n):
        s = i
        for k in range(i + 1, n):
            if abs(list_of_lists[k][i] > abs(list_of_lists[s][i])):
                s = k
        if i != s:
            list_of_lists[i], list_of_lists[j] = list_of_lists[j], list_of_lists[i]
            res *= -1
        if list_of_lists[i][i] < eps:
            return 0
        res *= list_of_lists[i][i]
        for j in range(i + 1, n):
            list_of_lists[i][j] /= list_of_lists[i][i]
        for j in range(n)
            if j != i and abs(list_of_lists[j][i]) > eps
                for k in range(i + 1, n):
                    list_of_lists[j][k] -= list_of_lists[i][k] * b
    return res
