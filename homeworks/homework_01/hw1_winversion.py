#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    """
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: input_lst: строка-массив букв
    """

    input_lst = input_lst[::-1]

    beginning = 0
    for i, el in enumerate(input_lst):
        if el == " ":
            input_lst[beginning:i] = reversed(input_lst[beginning:i])
            beginning = i + 1
    input_lst[beginning:] = reversed(input_lst[beginning:])
    return input_lst
