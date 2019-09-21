#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_lst = list(' '.join(''.join(input_lst).split()[::-1]))
    return input_lst
