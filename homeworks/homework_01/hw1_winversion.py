#!/usr/bin/env python
# coding: utf-8


def leftshift(num, input_lst):
    for i in range(num, len(input_lst)-1):
        input_lst[i], input_lst[i+1] = input_lst[i+1], input_lst[i]


def word_inversion(input_lst):
    '''
        Метод инвертирующий порядок слов в строке inplace
        (без выделения доп памяти)
        :param input_lst: строка-массив букв (['H', 'i']).
        Пробелы одиночные
        :return: None Все изменения в input_lst проходят
        '''
    k = len(input_lst)
    if k == 0:
        return None
    try:
        _ = input_lst.index(' ')
    except:
        return input_lst
    for i in range(len(input_lst)-1, -1, -1):
        if input_lst[i] == ' ':
            for _ in range(k - i):
                leftshift(i, input_lst)
            k = i
    leftshift(k, input_lst)
    for i in range(k):
        leftshift(0, input_lst)
    return input_lst
