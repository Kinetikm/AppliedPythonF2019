#!/usr/bin/env python
# coding: utf-8

import chardet


def len_of_str(data):
    s = [0] * len(data[0])
    s[3] = len(data[0][3])
    for lst in data:
        for j in range(len(lst) - 1):
            s[j] = max(s[j], len(lst[j]))
    ln = 0
    # общая длина всей строки
    for i in range(len(s)):
        s[i] += 4
        ln += s[i]
    ln += len(s) + 1
    s.append(ln)
    return s


def print_table(data, ln):
    print('-' * ln[-1])
    for i in range(len(data[0])):
        st = "{:^" + str(ln[i]) + "}"
        print("|" + st.format(data[0][i]), end="")
    print("|")
    for j in range(1, len(data)):
        for i in range(len(data[j])):
            if i == 3:
                st = "{:>" + str(ln[i] - 2) + "}"
                print("|" + st.format(data[j][i]), end="")
            else:
                st = "{:" + str(ln[i] - 2) + "}"
                print("|  " + st.format(data[j][i]), end="")
        print("  |")
    print('-' * ln[-1])


def enc_detect(filename):
    file = open(filename, 'rb')
    for line in file:
        enc = chardet.detect(line)
        if enc['encoding'] in {'utf-8', 'utf-16', 'windows-1251'}:
            return enc['encoding']
    file.close()
    return enc['encoding']


def check_data(data):
    k = len(data[0])
    for lst in data:
        if len(lst) < k:
            raise MyException
