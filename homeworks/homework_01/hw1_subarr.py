#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):

    d = {}
    sum = 0
    for i in range(len(input_list)):
        sum += input_list[i]
        if sum == num:
            return (0, i)
        if (sum - num) in d:
            return (d[sum - num] + 1, i)
        d[sum] = i
    return ()
