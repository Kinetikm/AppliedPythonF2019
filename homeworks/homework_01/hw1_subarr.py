#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    dict = {}
    sum = 0
    i = 0
    while i < len(input_lst):
        sum += input_lst[i]
        if sum == num:
            return 0, i
        if sum - num in dict:
            return dict[sum - num] + 1, i
        dict[sum] = i
        i += 1
    return ()
