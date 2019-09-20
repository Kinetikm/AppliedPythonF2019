#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_lst.reverse()
    begin = 0
    for i in range(len(input_lst)):
        if input_lst[i] == " ":
            input_lst[begin:i] = list(reversed(input_lst[begin:i]))
            begin = i+1
    input_lst[begin:len(input_lst)] = list(reversed(input_lst[begin:len(input_lst)]))
    return input_lst
