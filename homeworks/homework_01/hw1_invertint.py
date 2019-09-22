#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    tmp = -1 if number < 0 else 1
    number *= tmp
    var = 0
    while number > 0:
        var = number % 10 + var*10
        number //= 10
    return tmp*var
