#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    res_contain = {}
    curr_sum = 0
    for i in range(len(input_lst)):
        curr_sum = curr_sum + input_lst[i]
        if curr_sum == num:
            return 0, i
        if (curr_sum - num) in res_contain:
            return res_contain[curr_sum - num] + 1, i
        res_contain[curr_sum] = i
