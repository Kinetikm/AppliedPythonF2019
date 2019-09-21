#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    if number >= 0:
        return int(str(number)[::-1])
    else:
        return -1*int(str(number)[::-1][:-1])
