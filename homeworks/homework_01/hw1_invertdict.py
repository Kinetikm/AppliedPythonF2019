#!/usr/bin/env python
# coding: utf-8


def invert_dict(source_dict):
    '''
    Функция которая разворачивает словарь, т.е.
    каждому значению ставит в соответствие ключ.
    :param source_dict: dict
    :return: new_dict: dict
    '''

    def insert_in_dict(d, key, val):
        if isinstance(key, (list, set)):
            for k in key:
                insert_in_dict(d, k, val)
        elif isinstance(key, dict):
            return
        elif '__hash__' in dir(key) and key.__hash__ is not None:
            if key in d:
                if isinstance(d[key], list):
                    d[key].append(val)
                else:
                    d[key] = [d[key], val]
            else:
                d[key] = val
        else:
            print('Error!')

    new_dict = {}
    for key in source_dict:
        if isinstance(source_dict[key], dict):
            continue
        elif isinstance(source_dict[key], (list, set)):
            for i in source_dict[key]:
                insert_in_dict(new_dict, i, key)
        else:
            insert_in_dict(new_dict, source_dict[key], key)
    return new_dict
