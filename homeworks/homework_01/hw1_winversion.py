#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    # инверсируем весь массив
    for i in range(len(input_lst) // 2):
        swap(input_lst, i, len(input_lst) - i - 1)

    # выделяем границы слов
    last_i = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            # инверсируем перевернутое слово
            for j in range((i - last_i) // 2):
                swap(input_lst, last_i + j, i - j - 1)

            last_i = i + 1

    # инверсируем последнее слово
    for i in range((len(input_lst) - last_i) // 2):
        swap(input_lst, last_i + i, len(input_lst) - i - 1)

    return input_lst


def swap(lst, pos1, pos2):
    '''
    Функция, меняющая два элемента массива местами
    :param lst: сам массив
    :param pos1: индекс 1го элемента
    :param pos2: индекс 2го элемента
    '''
    lst[pos1], lst[pos2] = lst[pos2], lst[pos1]
