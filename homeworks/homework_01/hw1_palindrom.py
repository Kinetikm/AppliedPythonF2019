#!/usr/bin/env python
# coding: utf-8


def check_palindrom(a):
    if a == "":
        return True
    bool_a = True
    for i in range(0, len(a)//2+1):
        if a[i] != a[len(a)-1-i]:
            bool_a = False
    return bool_a
    raise NotImplementedError
#метод проверки числа на палиндром

