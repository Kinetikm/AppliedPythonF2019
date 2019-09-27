#!/usr/bin/env python
# coding: utf-8


def reverse(a):
    '''
        Метод, принимающий на вход int и
        возвращающий инвертированный int
        :param number: исходное число
        :return: инвертированное число
        '''

    flag = 1
    if (a < 0):
        flag = -1
        a *= -1
    b = str(a)
    return int(b[::-1]) * flag
