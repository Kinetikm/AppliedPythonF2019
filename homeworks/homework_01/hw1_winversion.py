#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    B = input_lst
    B = B[::-1]
    l = 0
    r = 0
    for i in range(len(B)):
        if B[i] == ' ':
            r = i
            B[l:r]=B[l:r][::-1]
            l = i+1
    B[l:]=B[l:][::-1]
    return B
