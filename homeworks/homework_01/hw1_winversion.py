#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    i = 0
    wl = 0
    while i + wl < len(input_lst):
        if input_lst[len(input_lst) - 1] != ' ':
            input_lst.insert(i, input_lst.pop())
            wl += 1
        else:
            i += wl
            wl = 0
            input_lst.insert(i, input_lst.pop())
            i += 1
    return input_lst
