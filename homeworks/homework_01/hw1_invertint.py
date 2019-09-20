#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    minus = 1 if number < 0 else 0
    num_list = list(str(abs(number)))
    num_list.reverse()
    result_str = ''.join(num_list)
    return -int(result_str) if minus else int(result_str)
