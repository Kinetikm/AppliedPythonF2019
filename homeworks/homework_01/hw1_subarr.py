#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    arr = ()
    if len(input_lst) == 0:
        return arr
    sum = {}
    S = 0
    for x in range(len(input_lst)):
        S += input_lst[x]
        if S == num:
            arr = (0, x)
            return arr
        if S - num in sum:
            arr = (sum[S - num] + 1, x)
            return arr
        sum[S] = x
    return arr
