#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    """
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    """
    negativ = False
    if number < 0:
        negativ = True
    s = str(number)
    if negativ:
        s = s[1:]
    s = s[::-1]
    rev_numb = int(s)
    if negativ:
        rev_numb = -rev_numb
    return rev_numb
