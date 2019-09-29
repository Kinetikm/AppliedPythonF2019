#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходccят
    '''
    def find_space(cur_pos, input_lst):
        i = cur_pos
        while (i != len(input_lst)) and (input_lst[i] != " "):
            i += 1
        return i


    def word_inversion(input_lst):
        for i in range(len(input_lst) // 2):
            input_lst[i], input_lst[-i - 1] = input_lst[-i - 1], input_lst[i]
        next_space_pos = -1
        cur_space_pos = -1
        while next_space_pos < (len(input_lst)):
            cur_space_pos = next_space_pos
            next_space_pos = find_space(cur_space_pos + 1, input_lst)
            for i in range((next_space_pos - cur_space_pos) // 2):
                input_lst[cur_space_pos + i + 1], input_lst[next_space_pos - i - 1] = input_lst[next_space_pos - i - 1], \
                                                                                      input_lst[cur_space_pos + i + 1]
        return input_lst
