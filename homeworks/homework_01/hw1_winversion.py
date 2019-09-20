#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп
    памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    words_num = input_lst.count(' ')
    temp_start_pos = 0
    temp_word_len = 0
    lst_len = len(input_lst)
    for i in range(words_num):
        while input_lst[lst_len-temp_word_len-1] != ' ':
            temp_word_len += 1
        for j in range(temp_word_len):
            input_lst.insert(temp_start_pos, input_lst[lst_len -
                                                       temp_word_len+j])
            del input_lst[lst_len-temp_word_len+j+1]
            temp_start_pos += 1
        input_lst.insert(temp_start_pos, ' ')
        temp_start_pos += 1
        del input_lst[-1]
        temp_word_len = 0
    return input_lst
