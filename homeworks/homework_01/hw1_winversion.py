#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    ln, t = len(input_lst), 0
    stop = ln
    for i in range(1, ln + 1):
        if input_lst[-i-t] == ' ':
            start = ln - i
            for l in range(start + 1, stop):
                #input_lst.append(input_lst.pop(start+1))
                input_lst += [input_lst.pop(start+1)]
            stop = start
            input_lst += [input_lst.pop(start)]
        elif i == ln:
            start = -1
            for l in range(start + 1, stop):
                input_lst += [input_lst.pop(start+1)]
    return input_lst
