#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    start = 0
    for i in range(len(input_lst)):
        a = input_lst.pop()
        if (a == " "):
            start = i
            input_lst.insert(start, a)
            start += 1
        else:
            input_lst.insert(start, a)
return input_lst
