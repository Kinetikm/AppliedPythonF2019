#!/usr/bin/env python
# coding: utf-8


def word_inversion(s):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param s: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в s проходят
    '''
    N = len(s)-1
    i, omega = N, 0
    s.reverse()
    while i > -1:
        if s[i] == ' ':
            s[i + 1:i + omega+1] = s[i + omega:i:-1]
            omega = 0
            i -= 1
        elif i == 0:
            s[i:omega+1] = s[omega-N-1:-N-2:-1]
            return s
        else:
            omega += 1
            i -= 1
