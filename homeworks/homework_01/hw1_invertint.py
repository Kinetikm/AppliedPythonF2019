#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    temp = 0
    znak = 0
    if number < 0:
        znak = -1
    else:
        znak = 1
    number = abs(number)
    while True:
        temp = (temp * 10) + (number % 10)
        number = number // 10
        if (number // 10) == 0 :
            temp = (temp * 10) + (number % 10)
            break
    number =  znak * temp
    return number
