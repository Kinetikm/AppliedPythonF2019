#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    s = str(abs(number))
    invert_number = int(s[::-1])
    return invert_number if number > 0 else - invert_number
