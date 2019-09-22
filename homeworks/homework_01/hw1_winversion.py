#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    """
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    """
    stroka = input_lst[::-1]
    stroka.append(' ')
    stroka.insert(0, ' ')
    flag = 0
    for i in range(len(stroka)):
        if stroka[i] == ' ':
            stroka[flag:i] = stroka[i:flag:-1]
            flag = i
    stroka.pop()
    stroka.remove(' ')
    return stroka
