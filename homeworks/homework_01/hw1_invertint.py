#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    st = str(number)
    st = st[::-1]
    if st[len(st) - 1] == '-':
        st = '-' + st[0: len(st) - 1]
    number = int(st)
    return(number)
