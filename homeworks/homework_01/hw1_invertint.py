#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    if number == 0:
        return 0
    if number < 0:
        minus = 1
        number = (-1)*number
    a = str(number)
    if minus == 1:
        return (-1)*int(a[::-1])
    else:
        return int(a[::-1])
