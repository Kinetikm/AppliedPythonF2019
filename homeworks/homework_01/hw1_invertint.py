#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    res = 0
    residue = 0
    flag = False

    if number < 0:
        number *= -1
        flag = True

    while number != 0:
        residue = number % 10
        number //= 10
        res += residue

        if number != 0:
            res *= 10
        else:
            break
        
    if flag:
        res *= -1

    return res
