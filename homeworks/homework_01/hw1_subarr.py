#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    res_contain = {}
    curr_sum = 0
    for index in range(len(input_lst)):
        curr_sum = curr_sum + input_lst[index]
        if curr_sum == num:
            return 0, index
        if (curr_sum - num) in _dict:
            return res_contain[curr_sum - num] + 1, index
        res_contain[curr_sum] = index
