#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    index = 0
    count = 0
    while count != len(input_lst) :
        if input_lst[len(input_lst) - 1] == " " :
            index = count
            input_lst.insert(index, input_lst.pop())
            index += 1
        else:
                input_lst.insert(index, input_lst.pop())
            count += 1
    return input_lst


    raise NotImplementedError
