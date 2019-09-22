#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    d = {}
    sum = 0
    if len(input_lst) == 0:
        return ()
    for i in range(len(input_lst)):
        sum += input_lst[i]
        if sum == num:
            return 0, i
        if sum - num in d:
            return d[sum - num] + 1, i
        d[sum] = i
    return ()
