#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    st = [input_lst[i] for i in range(len(input_lst))]
    k = 0
    print(st)
    st = st + [' ']
    for i in range(len(st)):
        if st[i] != ' ':
            k += 1
        else:
            for j in range(k // 2):
                st[i - k + j], st[i - j - 1] = st[i - j - 1], st[i - k + j]
            k = 0
    st = st[0: len(st) - 1]
    st.reverse()
    return st
