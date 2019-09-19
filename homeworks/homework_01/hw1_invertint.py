#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    minus = 1 if number < 0 else 0
    num_list = list(str(abs(number)))
    num_list.reverse()
    while num_list[0] == '0':
        num_list.pop(0)
        if not num_list:
            return 0
    result_str = ''
    for sym in num_list:
        result_str += sym
    return -int(result_str) if minus else int(result_str)
