#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_lst = input_lst[::-1]
    s = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            input_lst[s:i] = input_lst[s:i][::-1]
            s = i + 1
    return input_lst


