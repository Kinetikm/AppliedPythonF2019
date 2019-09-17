#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    string = str(number)
    if string[0] == '-':
        return - int(string[:0:-1])
    else:
        return int(str(number)[::-1])
    raise NotImplementedError
