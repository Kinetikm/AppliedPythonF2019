#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace
    (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    input_lst.reverse()
    j = 0
    flag = False
    for i, ch in enumerate(input_lst):
        if ch == ' ':
            input_lst[j:i] = reversed(input_lst[j:i])
            j = i + 1
            flag = True
    if flag:
        input_lst[j:i + 1:1] = reversed(input_lst[j:i + 1])
    else:
        input_lst.reverse()
    return input_lst
