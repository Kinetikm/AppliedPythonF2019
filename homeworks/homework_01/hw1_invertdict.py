#!/usr/bin/env python
# coding: utf-8


def invert_dict(source_dict):
    '''
    Функция которая разворачивает словарь, т.е.
    каждому значению ставит в соответствие ключ.
    :param source_dict: dict
    :return: new_dict: dict
    '''

    def add_to_dict(d, key, value):
        if isinstance(key, (list, tuple, set)):
            for i in key:
                add_to_dict(d, i, value)
        else:
            if '__hash__' in dir(key) and key.__hash__ is not None:
                if key in d:
                    if isinstance(d[key], list):
                        d[key].append(value)
                    else:
                        d[key] = [d[key], value]
                else:
                    d[key] = value
            else:
                print('error!')

    new_dict = {}
    for key in source_dict:
        if isinstance(source_dict[key], (dict)):
            continue
        if isinstance(source_dict[key], (list, tuple, set)):
            for i in source_dict[key]:
                add_to_dict(new_dict, i, key)
        else:
            add_to_dict(new_dict, source_dict[key], key)
    return new_dict
