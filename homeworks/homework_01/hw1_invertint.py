#!/usr/bin/env python
# coding: utf-8


def reverse(number): 
    if number >= 0 :
        stringnumber = str(number)
        number1 = int(stringnumber[::-1])
    else:
        stringnumber = str(abs(number))
        number1 = (int(stringnumber[::-1])) * -1
    return number1

