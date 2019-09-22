#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    if str_num[0] == '-':
        return int('-' + str_num[:0:-1])
    else:
        return int(str_num[::-1])
