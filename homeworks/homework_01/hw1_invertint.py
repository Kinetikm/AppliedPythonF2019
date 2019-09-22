#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    if (number < 0):
        mnog = -1
        number = number * (-1)
    else:
        mnog = 1
    delitel = 1
    mas = []
    konech = 0
    while (number >= delitel):
        delitel *= 10
        novelement = number % delitel
        novelement = int(novelement // (delitel / 10))
        mas.append(novelement)
    delitel = delitel / 10
    for i in range(len(mas)):
        konech = konech + delitel * (mas[i])
        delitel = delitel / 10
    konech = int(konech * mnog)
    return konech
