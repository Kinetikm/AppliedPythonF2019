#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    try:
        input_lst.index(" ")
    except ValueError:
        return input_lst

    input_lst = input_lst[::-1]
    index = 0
    for i in range(len(input_lst) + 1):
        if (i == len(input_lst)) or (input_lst[i] == " "):
            if index:
                input_lst[index:i] = input_lst[i-1:index-1:-1]
            else:
                input_lst[index:i] = input_lst[i-1::-1]
            index = i + 1

    return input_lst
