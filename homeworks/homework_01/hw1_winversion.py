#!/usr/bin/env python
# coding: utf-8
def word_inversion(input_lst):
    input_lst = [' '] + input_lst
    lst = input_lst[::-1]
    arr = []
    i = 0
    l = 0
    while i <= len(lst) - 1:
        if lst[i] == ' ':
            k = len(input_lst) - 1 - i
            c = input_lst[k:len(input_lst) - l:]
            arr = arr + c
            l = i + 1
        i += 1
    return arr[1:len(arr):]
