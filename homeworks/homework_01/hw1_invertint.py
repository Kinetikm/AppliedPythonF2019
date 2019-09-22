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
    s=str(number)
    if s[0] == '-' :
        sign = -1
        s = s[-1::]
    s=s[::-1]
    while (s[0]=="0"): 
        s=s[-1::]
    int(s)
    return s*sign
    raise NotImplementedError
