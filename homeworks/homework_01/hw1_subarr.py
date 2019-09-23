#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    pull_sum = dict()
    sum_sub = 0
    cord = 0
    for elem in input_lst:
        sum_sub += elem
        diff = sum_sub - num
        if sum_sub == num:
            res = (0, cord)
            return res
        if diff in pull_sum:
            res = (pull_sum[diff], cord)
            return res
        diff += num
        pull_sum[sum_sub] = cord + 1
        cord += 1
    return tuple()
