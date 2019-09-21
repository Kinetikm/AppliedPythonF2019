#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    """
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '"""
    iter_num = 0
    i = 0
    p = 0
    num = 0
    while iter_num < len(input_lst):
        if input_lst[i] == ' ':
            num += 1
            if num == 1:
                input_lst.insert(len(input_lst), input_lst[i])
            else:
                input_lst.insert(len(input_lst) - p - 1, input_lst[i])
            for j in range(i):
                if num == 1:
                    input_lst.insert(len(input_lst) - p, input_lst[0])
                else:
                    input_lst.insert(len(input_lst) - p - 1, input_lst[0])
                input_lst.pop(0)
            input_lst.pop(0)
            i = 0
            p = iter_num
        else:
            i += 1
        iter_num += 1
    return input_lst
