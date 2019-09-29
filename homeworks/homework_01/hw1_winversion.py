#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_lst.reverse()
    n = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            tmp = i
            for k in range(n, n + ((i - n + 1) // 2)):
                input_lst[n], input_lst[tmp-1] = input_lst[tmp-1], input_lst[n]
                tmp = tmp - 1
                n = n + 1
            n = i + 1
        if i == (len(input_lst)-1):
            tmp = i
            for j in range(n, n + ((i - n + 1) // 2)):
                input_lst[n], input_lst[tmp] = input_lst[tmp], input_lst[n]
                tmp = tmp - 1
                n = n + 1
    return input_lst
