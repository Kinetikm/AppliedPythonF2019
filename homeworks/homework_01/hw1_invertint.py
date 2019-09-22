#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    res = 0
    residue = 0

    while number != 0:
        residue = number % 10
        number //= 10
        res += residue

        if number != 0:
            res *= 10
        else:
            break

    return res
