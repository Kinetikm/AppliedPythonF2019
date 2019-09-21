#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке
    inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    k = 0
    i = 0
    revers(input_lst, 0, len(input_lst)-1)
    while i < len(input_lst):
        if input_lst[i] == " ":
            revers(input_lst, k, i-1)
            k = i+1
        i += 1
    revers(input_lst, k, len(input_lst)-1)
    return input_lst


def revers(input_lst, one, two):
    for i in range(0, (two - one + 1)//2, 1):
        k = input_lst[one + i]
        input_lst[one + i] = input_lst[two - i]
        input_lst[two - i] = k
