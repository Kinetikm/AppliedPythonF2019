#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    cur = 0
    for i in range(len(input_lst)):
        if i == len(input_lst) - 1:
            input_lst[cur:i+1] = input_lst[i:cur:-1] + [input_lst[cur]]
        if input_lst[i] == ' ':
            input_lst[cur:i] = input_lst[i-1:cur:-1] + [input_lst[cur]]
            cur = i + 1  # следующий за пробелом элемент
    input_lst.reverse()
    return input_lst
