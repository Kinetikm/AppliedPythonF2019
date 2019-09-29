#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    if ' ' not in input_lst:
        return input_lst
    input_lst.reverse()
    temp_start_pos = 0
    lst_len = len(input_lst)
    for i in range(lst_len):
        if input_lst[i] == ' ':
            for j in range((i-temp_start_pos)//2):
                input_lst[temp_start_pos+j], input_lst[i-1-j] = \
                          input_lst[i-1-j], input_lst[temp_start_pos+j]
            temp_start_pos = i + 1
    for j in range((lst_len-temp_start_pos)//2):
        input_lst[temp_start_pos+j], input_lst[lst_len-1-j] = \
                  input_lst[lst_len-1-j], input_lst[temp_start_pos+j]
    return input_lst
