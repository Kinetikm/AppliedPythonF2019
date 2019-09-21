#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    sign = 1
    if number < 0:
        sign = -1
        number *= -1
    str_num = str(number)
    str_num = str_num[(len(str_num)-1)::-1]
    new_number = sign * int(str_num)
    return new_number




