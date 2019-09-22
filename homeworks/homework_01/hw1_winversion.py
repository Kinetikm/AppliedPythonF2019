#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    if input_lst == []:
        return []
    List = []
    List.append(input_lst.pop(0))
    k = 0
    while True:
        if input_lst == []:
            break
        if input_lst[0] == ' ':
            k += 1
            input_lst.pop(0)
            List.append(input_lst.pop(0))
        else:
            List[k] = List[k] + input_lst.pop(0)
    List.reverse()
    while True:
        if List == []:
            break
        w = List.pop(0)
        for c in w:
            input_lst.append(c)
        input_lst.append(' ')
    input_lst.pop()
    return input_lst
