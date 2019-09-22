#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    if number==0:
        return 0
    s = str(number)
    s = s.rstrip('0')
    s = s[::-1]
    if '-' in s:
        s = s.rstrip('-')
        s = '-'+s
        return(int(s))
    else:
        return(int(s))

    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    raise NotImplementedError

   


