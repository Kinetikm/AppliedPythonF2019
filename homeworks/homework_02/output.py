#!/usr/bin/env python
# coding: utf-8
'''
вывод
'''


def table(table):
    try:
        return row_json(table)
    except TypeError:
        try:
            return row_tsv(table)


def row_json(table):
    # print(table)
    max_len = {k: len(k) for k in table[0]}
    for slovar in table:
        for k in slovar:
            max_len[k] = max(max_len[k], len(str(slovar[k])))
    size_str = sum(max_len.values())
    size_razdel = len(max_len)
    wight_table = size_str + 5*size_razdel + 1
    length = '-'*wight_table
    print(length, end="\n")
    head = ''

    for name in max_len:
        t = (max_len[name] - len(name)) // 2
        add_space = (max_len[name] - len(name)) % 2
        head += '|  ' + ' '*t + ' '*add_space + name + ' '*t + '  '

    head += '|'
    print(head,  end="\n")
    for slovar in table:
        # словарь - это строка json
        # print(slovar)
        # print(len(slovar))
        head = ''
        for k in slovar:
            # print(k)
            t = (max_len[k] - len(str(slovar[k])))
            if k == 'Оценка':
                head += '|  ' + ' '*t + str(slovar[k]) + '  '
            else:
                head += '|  ' + str(slovar[k]) + ' '*t + '  '
        head += '|'
        print(head, end="\n")
    print(length,  end="\n")


def row_tsv(table):
    # print(table)
    t = []
    # print(len(table))
    for k in table:
        t.append(len(k))
    # максимальное к-во элементов в подмассивах
    max_array = max(t)
    # print(max_array)
    max_len_ar = []
    for i in range(max_array):
        array_lenght = []
        for k in table:
            # print(len(str(k[i])))
            array_lenght.append(len(k[i]))
            # print(k[i])
        # print("@@@@@@@",array_lenght)
        # print("max",max(array_lenght))
        max_len_ar.append(max(array_lenght))
    # массив максимум по всем столбцам
    # print(max_len_ar)
    len_ = '-'*(sum(max_len_ar) + 5*len(max_len_ar) + 1)
    print(len_)
    head = ''
    first = table[0]
    # print(first)
    for k in table:
        # print(k)
        head = ''
        # print(max_len_ar)
        # обработка заголовков
        if k == first:
            for i in range(len(k)):
                # print(k[i], 'i', i)
                # print("############3")
                t = (max_len_ar[i] - len(k[i]))//2
                add_space = (max_len_ar[i] - len(k[i])) % 2
                # print(max_len_ar[i], len(k[i]),k[i],t)
                head += '|  ' + ' ' * t + ' ' * add_space + str(k[i])\
                        + ' ' * t + '  '
            head += '|'
        # print(head)
        else:
            # for i in
            # t_1 = (max_len_ar[0] - len(k[0]))//2
            # head += '|  ' + ' '*t_1 + str(k[0]) + ' '*t_1 + '  '
            # head += '|'
            for i in range(len(k)):
                # print(k[i], 'i', i)
                # print("############3")
                # print("i",i,len(k)-1)
                if i != len(k) - 1:
                    t = (max_len_ar[i] - len(k[i]))
                    # print(max_len_ar[i], len(k[i]),k[i],t)
                    head += '|  ' + str(k[i]) + ' '*t + '  '
                else:
                    t = (max_len_ar[i] - len(k[i]))
                    # print(max_len_ar[i], len(k[i]),k[i],t)
                    head += '|  ' + ' ' * t + str(k[i]) + '  '
            head += '|'

        print(head)
    print(len_)
