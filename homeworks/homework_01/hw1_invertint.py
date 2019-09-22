#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    if str(number)[0] == '-':
        number = number*(-1)
        return int('-' + str(number)[::-1])
    return int(str(number)[::-1])
