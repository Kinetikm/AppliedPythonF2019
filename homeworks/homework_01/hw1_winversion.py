#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_list.reverse()
    start = 0
    len_list = len(input_list)
    for end in range(len_list):
        if input_list[end] == ' ':
            if start == 0:
                input_list[:end] = input_list[end - 1::-1]
            else:
                input_list[start:end] = input_list[end - 1:start - 1:-1]
            
            start = end + 1
        
        if end == len_list - 1:
            if start == 0:
                input_list.reverse()
            else:
                input_list[start:] = input_list[end:start - 1:-1]

return input_list


