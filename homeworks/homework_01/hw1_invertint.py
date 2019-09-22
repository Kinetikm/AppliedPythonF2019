#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    n = len(number)
    if n % 2 == 0:
        print(number[:-int(n/2)-1:-1])
        if number.startswith(number[:-int(n/2)-1:-1]):
            print(True)
        else:
            print(False)
    else:
        print(number[:-int(n//2)-1:-1])
        if number.startswith(s[:-int(n//2)-1:-1]):
            print(True)
        else:
            print(False)
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    raise NotImplementedError
