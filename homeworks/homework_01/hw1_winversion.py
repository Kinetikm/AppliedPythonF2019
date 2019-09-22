#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    i = 0
    ind = 0
    input_lst.append(" ")
    l = len(input_lst)
    for j in range(l):
        if input_lst[j] == " ":
            ind = (i + j) // 2
            rev_j = 1
            while i < ind:
                k = input_lst[i]
                input_lst[i] = input_lst[j - rev_j]
                input_lst[j - rev_j] = k
                i = i + 1
                rev_j += 1
            i = j + 1
    i = 0
    input_lst.pop()
    while i < (l - 1) // 2:
        k = input_lst[i]
        input_lst[i] = input_lst[l - 2 - i]
        input_lst[l - 2 - i] = k
        i = i + 1
    return None
