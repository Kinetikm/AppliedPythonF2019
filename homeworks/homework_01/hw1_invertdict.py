#!/usr/bin/env python
# coding: utf-8


def invert_dict(source_dict):
    '''
    Функция которая разворачивает словарь, т.е.
    каждому значению ставит в соответствие ключ.
    :param source_dict: dict
    :return: new_dict: dict
    '''

    new_dict = {}
    for key in source_dict:
        if isinstance(source_dict[key], list) or isinstance(
                source_dict[key], tuple) or \
                isinstance(source_dict[key], set):
            for val in merge(source_dict[key]):
                if new_dict.get(val, 'No') is 'No':
                    new_dict[val] = key
                else:
                    if not isinstance(new_dict[val], list):
                        new_dict[val] = [new_dict[val]]
                        new_dict[val].append(key)
                    else:
                        new_dict[val].append(key)
        else:
            val = source_dict[key]
            if new_dict.get(val, 'No') is 'No':
                new_dict[val] = key
            else:
                if not isinstance(new_dict[val], list):
                    new_dict[val] = [new_dict[val]]
                    new_dict[val].append(key)
                else:
                    new_dict[val].append(key)
    return new_dict


def merge(lstlst):
    all = []
    for lst in lstlst:
        if isinstance(lst, list) or isinstance(
                lst, tuple) or isinstance(lst, set):
            all = all + merge(lst)
        else:
            all.append(lst)
    return all
