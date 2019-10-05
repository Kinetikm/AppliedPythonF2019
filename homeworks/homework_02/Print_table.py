#!/usr/bin/env python
# coding: utf-8


def table(table):
    try:
        return print_json(table)
    except TypeError:
        try:
            return print_tsv(table)


def print_json(table):
    max_len = {k: len(k) for k in table[0]}
    for val in table:
        for k in val:
            max_len[k] = max(max_len[k], len(str(val[k])))
    str_s = sum(max_len.values())
    table_ = str_s + 5*len(max_len) + 1
    len = '-'*table_
    print(len, end="\n")
    body = ''
    for name in max_len:
        t = (max_len[name] - len(name)) // 2
        add_space = (max_len[name] - len(name)) % 2
        body += '|  ' + ' '*t + ' '*add_space + name + ' '*t + '  '
    body += '|'
    print(body,  end="\n")
    for val in table:
        body = ''
        for k in val:
            t = (max_len[k] - len(str(val[k])))
            if k == 'Оценка':
                body += '|  ' + ' '*t + str(val[k]) + '  '
            else:
                body += '|  ' + str(val[k]) + ' '*t + '  '
        body += '|'
        print(body, end="\n")
    print(len,  end="\n")


def print_tsv(table):
    list = []
    for k in table:
        list.append(len(k))
    arr_max = max(list)
    max_list = []
    for i in range(arr_max):
        arr_len = []
        for k in table:
            arr_len.append(len(k[i]))
        max_list.append(max(arr_len))
    trait = '-'*(sum(max_list) + 5*len(max_list) + 1)
    print(trait)
    h = ''
    first = table[0]
    for k in table:
        h = ''
        if k == first:
            for i in range(len(k)):
                list = (max_list[i] - len(k[i]))//2
                add_space = (max_list[i] - len(k[i])) % 2
                h += '|  ' + ' ' * t + ' ' * add_space + str(k[i])\
                    + ' ' * t + '  '
            h += '|'
        else:
            for i in range(len(k)):
                if i != len(k) - 1:
                    list = (max_list[i] - len(k[i]))
                    h += '|  ' + str(k[i]) + ' '* list + '  '
                else:
                    list = (max_list[i] - len(k[i]))
                    h += '|  ' + ' ' * list + str(k[i]) + '  '
            h += '|'
        print(h)
    print(trait)
