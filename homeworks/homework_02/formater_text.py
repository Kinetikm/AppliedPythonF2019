# -*- coding: utf-8 -*-


def text_formater(list_of_dictionary):
    def maximum(list, key):
        m = len(key)
        for elem in list:
            if len(str(elem[key])) > m:
                m = len(str(elem[key]))
        return m

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
