#!/usr/bin/env python
# coding: utf-8


def reverse(int_n):
    s = str(int_n)
    sign = 1
    if int_n < 0:
        sign = -1
        s = s[1:len(s)]
    # проверка знака числа
    int_n = sign * int(s[::-1])
    return int_n
