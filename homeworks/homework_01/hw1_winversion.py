#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    """
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    """
    temp = list()
    write_index = 0
    for _ in reversed(range(len(input_lst))):
        symbol = input_lst.pop()
        if symbol != ' ':
            temp.insert(0, symbol)
        else:
            temp.append(symbol)
            for element in temp:
                input_lst.insert(write_index, element)
                write_index += 1
            temp = list()
    for element in temp:
        input_lst.insert(write_index, element)
        write_index += 1
    return input_lst
