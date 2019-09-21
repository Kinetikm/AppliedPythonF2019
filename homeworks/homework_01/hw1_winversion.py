#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    input_lst = input_lst[::-1]

    start = 0

    for idx in range(len(input_lst)):
        if input_lst[idx] == ' ':
            input_lst[start:idx] = input_lst[start:idx][::-1]
            start = idx + 1

    input_lst[start:] = input_lst[start:][::-1]

    return input_lst
