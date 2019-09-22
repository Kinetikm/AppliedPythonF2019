#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    s = str(number)
    s = s.rstrip('0')
    s = s[::-1]
    if '-' in s:
        s = s.rstrip('-')
        s = '-'+s
        print(int(s))
    else:
        print(int(s))

    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''



