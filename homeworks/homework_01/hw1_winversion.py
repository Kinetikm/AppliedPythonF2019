#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_lst.reverse()
    i = 0
    while i < len(input_lst):
        j = i
        wlen = 0
        if input_lst[i] == ' ':
            i += 1
            continue
        else:
            while j != len(input_lst) and input_lst[j] != ' ':
                wlen += 1
                j += 1
            for k in range(wlen // 2):
                с = input_lst[i+k]
                input_lst[i+k] = input_lst[i+wlen-1-k]
                input_lst[i+wlen-1-k] = c
            i += wlen
    return input_lst
