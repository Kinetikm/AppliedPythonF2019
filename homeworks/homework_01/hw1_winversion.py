#!/usr/bin/env python
# coding: utf-8


def word_inversion (input_lst):
    word_len = 0
    index = 0
    probelnum = 0
    probelcount = input_lst.count(' ')
    for i in range(len(input_lst)):
        while (input_lst[len(input_lst) - 1] != " ")  and (i != (len(input_lst))) and (probelnum != probelcount):
            word_len += 1
            input_lst.insert(index, input_lst.pop())
            i += 1
        if probelnum != probelcount:
            i += 1
            input_lst.insert(word_len, input_lst.pop())
            probelnum += 1
            word_len += 1
            index = word_len

    return input_lst
