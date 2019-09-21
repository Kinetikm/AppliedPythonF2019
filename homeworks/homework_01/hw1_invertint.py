#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    negative = False
    if(number < 0):
        negative = True
    s = str(number)
    s =  s.replace('-', '')
    s = s[::-1]
    number = int(s)
    if negative: 
        number = number*-1
    return number
    
    
