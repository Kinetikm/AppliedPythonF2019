#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    n = 0
    for i in range(len(input_lst)):
        if input_lst[i] is " ":
            input_lst[n:i:] = input_lst[n:i:][::-1]
            n = i + 1
    input_lst[n::] = input_lst[n::][::-1]
    input_lst = input_lst[::-1]
    return input_lst
