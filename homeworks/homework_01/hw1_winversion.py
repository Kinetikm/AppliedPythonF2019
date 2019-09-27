#!/usr/bin/env python
# coding: utf-8


def word_inversion(a):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''

    beg = 0
    end = 0
    res = []
    a = a[::-1]
    for i in range(len(a)):
        if a[i] != " ":
            end += 1
        else:
            b = a[beg:end:]
            res = res + b[::-1]
            res.append(' ')
            beg += 1
            end += 1
            beg = end
    b = a[beg:end:]
    res = res + b[::-1]
    return res
