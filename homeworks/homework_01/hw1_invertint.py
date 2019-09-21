#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    
    
    res = 0
    residue = 0
    
    while number != 0:
        print("number -> {}".format(number))
        
        residue = number % 10
        number //= 10
        res += residue
        
        if number != 0:
            res *= 10
        else:
            break

    return res
    
    raise NotImplementedError
