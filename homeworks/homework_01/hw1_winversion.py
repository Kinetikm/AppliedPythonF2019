#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    return list(' '.join(''.join(input_lst).split()[::-1]))
