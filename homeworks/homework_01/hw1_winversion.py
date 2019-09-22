#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_lst = input_lst[::-1]
    z = 0
    length = len(input_lst)
    for i in range(length):
        if input_lst[i] == ' ':
            mark = i
            tmp = mark
            for j in range(z, z + ((mark - z + 1))//2):
                input_lst[0], input_lst[tmp-1] = input_lst[tmp-1], input_lst[0]
                tmp -= 1
                z += 1
            z = mark + 1
        if i == (length - 1):
            mark = i
            tmp = mark
            for l in range(z, z + ((mark - z + 1))//2):
                input_lst[z], input_lst[tmp] = input_lst[tmp], input_lst[z]
                tmp -= 1
                z += 1
    return input_lst
