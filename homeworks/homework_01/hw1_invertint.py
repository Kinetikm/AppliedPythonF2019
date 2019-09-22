#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    if number:
        st = str(number).rstrip('0')[::-1]
        if number < 0:
            st = '-' + st[:-1]
        it = int(st)
        return it
    return number
