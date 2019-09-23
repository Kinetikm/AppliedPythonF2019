#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    _dict = {}   
    curr_sum = 0 
    for i in range(0,len(input_lst)):
        curr_sum = curr_sum + arr[i]
        if curr_sum == num:  
            return 0, i
        if (curr_sum - num) in _dict:  
            return _dict[curr_sum - num] + 1, i
        _dict[curr_sum] = i   
    raise NotImplementedError
