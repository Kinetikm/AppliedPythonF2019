#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    if number >= 0:
        number = int(''.join(list(str(number)[::-1])))
    else:
        number = int(''.join(list(str(-number)[::-1])))
    print(number)
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
