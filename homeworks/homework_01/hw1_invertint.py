#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    str_num = str(number)
    if str_num[0] == '-':
        str_num = str_num[1::]
        return int('-' + str_num[::-1])
    else:
        return int(str_num[::-1])
