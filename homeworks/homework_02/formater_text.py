# -*- coding: utf-8 -*-


def text_formater(list_of_dictionary):
    length = 1

    for key in list_of_dictionary[0]:
        length += maximum(list_of_dictionary, key) + 5

    text = '-' * length + '\n'
    text += '|'
    for key in list_of_dictionary[0]:
        text += key.center(maximum(list_of_dictionary, key) + 4, ' ') + '|'

    text += '\n'
    for dictionary in list_of_dictionary:
        text += '|'
        for element in dictionary:
            len_dict_el = len(str(dictionary[element]))
            if element != 'Оценка':
                text += '  ' + str(dictionary[element]) + ' ' * \
                        (maximum(list_of_dictionary, element) + 2 - len_dict_el) \
                        + '|'
            else:
                text += '  ' + ' ' * \
                        (maximum(list_of_dictionary, element) - len_dict_el) + \
                        str(dictionary[element]) + '  |'
        text += '\n'

    text += '-' * length
    return text


def text_formater_tsv(row_list):
    list_len = []

    for i in range(len(row_list[0])):
        m = 0
        for r in row_list:
            if len(r[i]) > m:
                m = len(r[i])
        list_len.append(m)

    max_len = sum(list_len) + len(row_list[0]) * 5 + 1

    text = '-' * max_len + '\n'

    num_row = 1
    for row in row_list:
        text += '|'
        i = 0
        for elem in row:
            if num_row == 1:
                text += elem.center(list_len[i] + 4) + '|'
            else:
                if row_list[0][i] == 'Оценка':
                    text += '  ' + \
                            (' ' * (list_len[i] - len(elem)) + elem) + '  |'
                else:
                    text += '  ' + \
                            (elem + ' ' * (list_len[i] - len(elem))) + '  |'
            i += 1
        num_row += 1
        text += '\n'

    text += '-' * max_len
    return text


def len_row(row):
    row_len = 0
    for elem in row:
        row_len += len(elem)
    return row_len


def maximum(list, key):
    m = len(key)
    for elem in list:
        if len(str(elem[key])) > m:
            m = len(str(elem[key]))
    return m
