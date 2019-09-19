#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    result_list = []
    count = start_index = 0
    while count < len(input_lst):
        if input_lst[count] == " ":
            result_list.append(input_lst[start_index:count])
            start_index = count + 1
        elif count == len(input_lst) - 1:
            result_list.append(input_lst[start_index:count + 1])
            start_index = count + 1
        count += 1
    return_list = []
    for node_list in result_list[::-1]:
        for node in node_list:
            return_list.append(node)
        return_list.append(" ")

    return return_list[:-1]

