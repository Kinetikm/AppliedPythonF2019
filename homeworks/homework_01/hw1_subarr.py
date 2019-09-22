#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_list, num):
    res_contain = {}
    curr_sum = 0

    for index in range(len(input_list)):
        curr_sum = curr_sum + input_list[index]

        if curr_sum == num:
            return 0, index
        if (curr_sum - num) in res_contain:
            return res_contain[curr_sum - num] + 1, index

        res_contain[curr_sum] = index
