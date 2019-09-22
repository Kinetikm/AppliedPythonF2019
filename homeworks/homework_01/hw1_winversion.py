#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_lst.reverse()
    end1 = 0
    i = 0
    tmp = 0
    count = 0
    k = 0
    for i in range(len(input_lst)):
        if (input_lst[i] == ' '):
            j = i - 1
            for k in range(end1, ((i + end1) // 2)):
                input_lst[k], input_lst[j] = input_lst[j], input_lst[k]
                j = j - 1
            end1 = i + 1
        if (i == (len(input_lst) - 1)):
            j = i
            for z in range(end1, ((i + end1 + 1) // 2)):
                input_lst[z], input_lst[j] = input_lst[j], input_lst[z]
                j = j - 1
    raise NotImplementedError
