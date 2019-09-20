#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''

    negative = True if number < 0 else False
    str_num = str(number)
    ans = 0
    if negative:
        ans_str = str_num[-1:0:-1]
        ans = (-1) * int(ans_str)
    else:
        ans_str = str_num[-1::-1]
        ans = int(ans_str)
    return ans
