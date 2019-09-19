#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    idx = 0
    input_lst.reverse()
    for i in range(len(input_lst)):
        if (input_lst[i] == ' '):
            if (i - idx + 1 != 2):
                input_lst[idx:i] = input_lst[idx:i][::-1]
                idx = i + 1
            else:
                idx = i + 1
    input_lst[idx:] = input_lst[idx:][::-1]
    return input_lst
