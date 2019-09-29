#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    k = 0
    n = 0
    l = 0
    for i in range(0, input_lst.count(" "), 1):
        k = k + n
        input_lst.insert(len(input_lst) - k, ' ')
        k = k + l
        n = 0
        while input_lst[0] != ' ':
            input_lst.insert(len(input_lst) - k, input_lst[0])
            input_lst.pop(0)
            n = n + 1
        input_lst.pop(0)
        n = n
        l = 1    
    return input_lst
    raise NotImplementedError
