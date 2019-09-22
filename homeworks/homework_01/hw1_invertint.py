#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    if number < 0:
        flag = 1
    else:
        flag = 0
    number = abs(number)
    number = str(number)
    str_tmp = number[::-1]
    int_result = int(str_tmp)
    if flag == 1:
        int_result = (-1) * int_result
    return int_result
