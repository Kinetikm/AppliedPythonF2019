# !/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    """
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    """
    iterator = len(input_lst) - 1
    input_lst.append(' ')
    flag = False
    second_space = iterator
    first_space = 0
    while iterator >= 0:
        if input_lst[iterator] == ' ' and not flag:
            first_space = iterator
            iterator -= 1
            flag = True
            continue
        elif input_lst[iterator] == ' ' and not iterator == 0:
            second_space = iterator
            for i in range(second_space, first_space, 1):
                input_lst.append(input_lst[iterator + 1])
                input_lst.pop(iterator + 1)
            iterator = second_space
            first_space = second_space
            iterator -= 1
        elif iterator == 0:
            for i in range(0, first_space, 1):
                input_lst.append(input_lst[iterator])
                input_lst.pop(iterator)
            input_lst.pop(0)
            break
        else:
            iterator -= 1

