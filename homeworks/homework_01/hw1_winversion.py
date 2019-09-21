#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    input_lst = input_lst[::-1]  # сначала перевернём всё
    beg = 0
    for i in range(len(input_lst)):
        if ( input_lst[i] == ' ' ):  # теперь каждое слово по отдельности
            input_lst[beg:i] = input_lst[beg:i][::-1]
            beg = i+1
    input_lst[beg:] = input_lst[beg:][::-1]  # и последнее слово
    return input_lst
