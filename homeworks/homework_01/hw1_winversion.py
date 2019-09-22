#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    for word in input_lst.split(' '):
        print(' '.join(word.split()[::-1]))
