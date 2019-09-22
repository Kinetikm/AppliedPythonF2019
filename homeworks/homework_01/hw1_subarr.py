#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    sub = tuple()
    if len(input_lst) == 0:
        return sub
    summa = dict()
    S = 0
    for x in range(len(input_lst)):
        S += input_lst[x]
        if S == num:
            sub = (0, x)
            return sub
        if S - num in summa:
            sub = (summa[S - num] + 1, x)
            return sub
        summa[S] = x
    return sub
