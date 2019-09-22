#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    st = str(number)
    st = st[::-1]
    if number != '':
        number = int(st)
    return(number)
