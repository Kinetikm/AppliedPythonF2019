#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
        ln, t = len(input_lst), 0
        stop = ln
        for i in range(1, ln + 1):
            if input_lst[-i - t] == ' ':
                start = ln - i
                for j in range(start + 1, stop):
                    input_lst.append(input_lst[j])
                    t += 1
                stop = start
                input_lst.append(' ')
                t += 1
            elif i == ln:
                start = 0
                for j in range(start, stop):
                    input_lst.append(input_lst[j])
                    t += 1
        return input_lst[ln::]



