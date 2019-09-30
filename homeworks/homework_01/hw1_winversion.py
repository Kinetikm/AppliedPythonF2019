#!/usr/bin/env python
# coding: utf-8


def change(i, j, list_):
    for l in range(len(list_[i + 1:j])//2):
        list_[i + 1 + l], list_[j - 1 - l] = list_[j - 1 - l], list_[i + 1 + l]


def word_inversion(input_lst):
    input_lst.reverse()
    arg1 = -1
    arg2 = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            arg2 = i
            change(arg1, arg2, input_lst)
            arg1 = arg2
    change(arg1, len(input_lst), input_lst)
    return input_lst
