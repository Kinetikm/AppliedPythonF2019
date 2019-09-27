#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_lst = input_lst[::-1]
    count = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            input_lst[count:i] = input_lst[count:i][::-1]
            count = i + 1
    return input_lst
