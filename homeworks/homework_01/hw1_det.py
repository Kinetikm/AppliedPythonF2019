#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    n = len(list_of_lists)
    for i in range(n-1):
        if len(list_of_lists[i+1]) != len(list_of_lists[i]):
            return None
    if n != len(list_of_lists[0]):
        return None
    if n == 1:
        return list_of_lists[0][0]
    det = 0.0
    for i in range(n):
        a = list_of_lists[i][0]
        b = list_of_lists[::]
        for j in range(n):
            b[j] = b[j][1::]
        b.pop(i)
        det += a * calculate_determinant(b) * (-1) ** i
    return det
