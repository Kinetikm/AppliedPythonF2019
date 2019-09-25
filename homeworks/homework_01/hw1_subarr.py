#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    input_dict = {}
    sum = 0
    for i in range(len(input_lst)):
        sum += input_lst[i]
        if (sum == num):
            return (0, i)
        if (sum - num) in input_dict:
            return (input_dict[sum - num] + 1, i)
        else:
            input_dict[sum] = i
    return()
    
    raise NotImplementedError
