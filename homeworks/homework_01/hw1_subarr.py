#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_list, num):
    if type(input_list) is int:
        return None
    if not any(input_list):
        return None

    res_contain = []

    for index in range(1, len(input_list)):
        if input_list[index - 1] == num:
            res_contain.append([index - 1, index - 1])
        if input_list[index - 1] + input_list[index] == num:
            res_contain.append([index - 1, index])

    if res_contain:
        res = (res_contain[0][0], res_contain[0][1])
    else:
        return None

    return res
