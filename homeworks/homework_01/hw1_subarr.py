#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    kof = len(input_lst) - 2
    while i <= kof:
        if (input_lst[i] + input_lst[i + 1]) == num:
            print('(', i, ',', i + 1, ')', sep='')
            break

        if (input_lst[i] == num):
            print('(', i, ',', i, ')', sep='')
            break
        print('()')
        break
        i += 1
    raise NotImplementedError
