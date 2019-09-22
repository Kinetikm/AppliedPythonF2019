#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_lst = ''.join(input_lst).split()[::-1]
    input_lst = ' '.join(input_lst)
    return list(input_lst)
