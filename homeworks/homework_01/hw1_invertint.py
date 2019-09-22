#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    minus = False
    if number < 0:
        minus = True
        number = abs(number)
    number = str(number)
    number = number[::-1]
    number = int(number)
    if minus:
        number = -1 * number
    return number
