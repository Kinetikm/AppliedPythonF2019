#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    str_num = str(number)[::-1]
    if len(str_num) > 1:
        for n in str_num:
            if n == '0':
                str_num = str_num[1:]
            else:
                break
    if str_num[-1] == '-':
        str_num = '-' + str_num[:-1]
    return int(str_num)
