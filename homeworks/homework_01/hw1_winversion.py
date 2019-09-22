#!/usr/bin/env python
# coding: utf-8


def append(input_lst, space_pos, start_pos):
    #input_lst.append(' ')
    for i in range(len(input_lst) - space_pos):
        input_lst.insert(start_pos,input_lst.pop())
    return input_lst, (len(input_lst) - space_pos)

def rfind(input_lst):
    for i in range(len(input_lst)):
        if input_lst[len(input_lst)-i-1] == ' ':
            return len(input_lst)-i-1
    raise ValueError

def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    start_pos = 0
    try:
        space_pos = rfind(input_lst)
    except ValueError:
        return input_lst
    while start_pos < space_pos:
        input_lst, temp = append(input_lst, space_pos, start_pos)
        start_pos += temp
        space_pos = rfind(input_lst)
    input_lst.insert(start_pos-1,input_lst.pop(0))
    return input_lst
