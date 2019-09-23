#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    n = "" 
    if number < 0: 
        number = number * (-1)
        n = "-" 
    b = str(number) 
    b = b[::-1] 
    b = n + b 
    return int(b)
