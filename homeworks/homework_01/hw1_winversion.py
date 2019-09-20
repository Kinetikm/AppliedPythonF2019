#!/usr/bin/env python
# coding: utf-8


def swap(array, i, j):
    tmp = array[i]
    array[i] = array[j]
    array[j] = tmp


def word_inversion(input_lst):
    n = len(input_lst)
    l = 0
    r = n - 1
    # reverse array
    while l < r:
        swap(input_lst, l, r)
        l += 1
        r -= 1
    # pointer to a word START
    s = 0
    # pointer to a word END
    e = 0

    while e < n:
        if e == n - 1:
            while s < e:
                swap(input_lst, s, e)
                s += 1
                e -= 1
            break

        if input_lst[e] == ' ':
            space_index = e
            e -= 1
            while s < e:
                swap(input_lst, s, e)
                s += 1
                e -= 1

            e = space_index
            s = space_index + 1

        e += 1
    return input_lst
