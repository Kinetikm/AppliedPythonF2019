#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    digit = 1
    abs_number = number
    if number < 0:
        digit = -1
        abs_number *= digit
    string_number = str(abs_number)
    return int(string_number[::-1]) * digit
