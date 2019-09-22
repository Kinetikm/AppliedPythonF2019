#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_list, num):
    if not any(input_list):
        return None

    results = {}
    cur_sum = 0

    for i in range(len(input_list)):
        cur_sum = cur_sum + input_list[i]

        if cur_sum == num:
            return (0, i)
        if (cur_sum - num) in results:
            return (results[cur_sum - num] + 1, i)

        results[cur_sum] = i

    return ()
