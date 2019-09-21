#!/usr/bin/env python
# coding: utf-8


def reverse_word(input_lst, begin, end):
    tmp_b = begin
    tmp_e = end
    while tmp_b < tmp_e:
        input_lst[tmp_b], input_lst[tmp_e] = input_lst[tmp_e], input_lst[tmp_b]
        tmp_b += 1
        tmp_e -= 1


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    begin = 0
    try:
        space = input_lst.index(' ')
    except ValueError:
        return input_lst
    while space < len(input_lst):
        end = space - 1
        reverse_word(input_lst, begin, end)
        begin = end + 2
        try:
            space = input_lst.index(' ', begin)
        except ValueError:
            reverse_word(input_lst, begin, len(input_lst)-1)
            break
    input_lst.reverse()
    return input_lst
