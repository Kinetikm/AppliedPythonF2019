#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''

    z = str(number)[::-1]

    if len(z) > 1:
        for n in z:
            if n == '0':
                z = z[1:]
            else:
                break

    if z[-1] == '-':
        z = '-' + z[:-1]

    return int(z)
