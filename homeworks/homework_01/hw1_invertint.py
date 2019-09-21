#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    if number < 0:
        number = str(number)
        number = number[:0:-1]
        number = int(number)*(-1)
        return number
    else:
        number = str(number)
        number = number[::-1]
        return int(number)
