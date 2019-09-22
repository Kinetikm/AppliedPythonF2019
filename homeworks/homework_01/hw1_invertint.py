#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    l = list(str(number))
    l.reverse()
    if number >= 0:
        number = int(''.join(l))
        return number
    else:
        l.pop()
        l.insert(0, '-')
        number = int(''.join(l))
        return number
