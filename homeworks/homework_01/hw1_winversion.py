#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    """
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    """
    temp = list()
    new_list = list()
    for _ in reversed(range(len(input_lst))):
        symbol = input_lst.pop()
        if symbol != ' ':
            temp.insert(0, symbol)
        else:
            temp.append(symbol)
            new_list += temp
            temp = list()
    new_list += temp
    return new_list
