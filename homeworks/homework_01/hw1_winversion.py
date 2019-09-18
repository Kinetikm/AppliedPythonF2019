#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    if ' ' in input_lst:
        s = ''
        for letter in input_lst:
            s += letter
            #print(s)
        del input_lst[::]
        input_lst += [i for i in s.split()]
        input_lst.reverse()
        for i in range(len(input_lst)):
            input_lst += input_lst[0]
            input_lst.append(' ')
            del input_lst[0]
        input_lst.pop()
    return input_lst