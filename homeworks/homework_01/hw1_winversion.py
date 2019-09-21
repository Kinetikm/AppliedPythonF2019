#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    beg = 0
    for i in range(len(input_lst)):
        if i == len(input_lst) - 1:
            input_lst[beg:] = input_lst[i:beg:-1] + [input_lst[beg]]
            continue
        if input_lst[i] == " ":
            input_lst[beg:i] = input_lst[i-1:beg:-1] + [input_lst[beg]]
            beg = i + 1
    input_lst.reverse()
    return(input_lst)
