#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    ptr = 0
    for i, n in enumerate(input_lst):
        if n == ' ':
            input_lst = input_lst[:ptr] + input_lst[ptr:i][::-1] + input_lst[i:]
            ptr = i+1
        if i == len(input_lst)-1:
            input_lst = input_lst[:ptr] + input_lst[ptr:][::-1]

    return input_lst[::-1]
