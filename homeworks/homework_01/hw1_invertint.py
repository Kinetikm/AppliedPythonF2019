#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    s = str(number)
    invert_number = int(s[::-1])
    return invert_number
    #raise NotImplementedError
