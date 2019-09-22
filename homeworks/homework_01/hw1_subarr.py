#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_list, num):
    if not input_list:
        return None

    res_contain = []

    for index in range(1, len(input_list)):
        if input_list[index - 1] == num:
            res_contain.append([index - 1, index - 1])
        if input_list[index - 1] + input_list[index] == num:
            res_contain.append([index - 1, index])

    res = (res_contain[0][0], res_contain[0][1])

    return res
