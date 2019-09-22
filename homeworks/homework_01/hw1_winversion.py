#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''

    input_lst.reverse()

    # print("".join(input_lst))

    word_start = 0
    for (i, elem) in enumerate(input_lst):
        is_last_iteration = i == len(input_lst) - 1
        if elem == ' ' or is_last_iteration:
            if is_last_iteration:
                i += 1
            # print("sswitching")
            # print(input_lst[word_start:i])
            # print("to")
            # switch = input_lst[i-1:(word_start-1 if word_start-1 > 0 else None):-1]
            # print(switch)

            for j in range(word_start, int((word_start+i)/2)):
                tmp = input_lst[j]
                rev_idx = i - (j-word_start) - 1
                input_lst[j] = input_lst[rev_idx]
                input_lst[rev_idx] = tmp

            # print("switched\n", input_lst[word_start:i])

            word_start = i + 1

    return input_lst
