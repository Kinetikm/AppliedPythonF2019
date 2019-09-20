#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    """
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    """
    write_index = 0
    word_len = 0
    for _ in reversed(range(len(input_lst))):
        symbol = input_lst.pop()
        if symbol != ' ':
            input_lst.insert(write_index, symbol)
            word_len += 1
        else:
            write_index += word_len
            input_lst.insert(write_index, symbol)
            write_index += 1
            word_len = 0
    return input_lst
