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
    temp = str(number)
    if number > 0:
        temp = int(temp[::-1])
    else:
        temp = -int(temp[:0:-1])
    return temp
