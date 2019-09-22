#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    input_lst.append(' ')
    k = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            for s in range(i, k, -1):
                input_lst[s] = input_lst[k]
                for l in range(k, s):
                    input_lst[l] = input_lst[l+1]
            for n in range(k, i):
                input_lst[len(input_lst)] = input_lst[len(input_lst)+1]
            input_lst[i] = ' '
            k = i+1
    del input_lst[len(input_lst)-1]
    input_lst.reverse()
    print(input_lst)
