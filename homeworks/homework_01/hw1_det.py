#!/usr/bin/env python
# coding: utf-8


def decrease(list_of_lists, i, j):
    L = []
    n = len(list_of_lists)
    ik = 0
    for k in range(n):
        if k == i:
            ik -= 1
            continue
        L.append([])
        for q in range(n):
            if q == j:
                continue
            L[k+ik].append(list_of_lists[k][q])
    return L


def calculate_determinant(list_of_lists):
    if list_of_lists == []:
        return None
    for i in range(len(list_of_lists)):
        if len(list_of_lists) != len(list_of_lists[i]):
            return None
    if len(list_of_lists) == 1:
        return list_of_lists[0][0]
    else:
        summ = 0
        for i in range(len(list_of_lists)):
            summ += ((-1)**(i)*list_of_lists[i][0] *
                     calculate_determinant(decrease(list_of_lists, i, 0)))
    return summ
