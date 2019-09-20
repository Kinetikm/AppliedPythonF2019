#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    n = len(input_lst)
    a = input_lst
    l = 0
    r = n - 1
    # reverse array
    while l < r:

        tmp = a[l]
        a[l] = a[r]
        a[r] = tmp
        l += 1
        r -= 1

    # pointer to a word START
    s = 0
    # pointer to a word END
    e = 0

    while e < n:
        if e == n - 1:

            while s < e:
                tmp = a[s]
                a[s] = a[e]
                a[e] = tmp
                s += 1
                e -= 1

            break

        if a[e] == ' ':
            space = e
            e -= 1

            while s < e:
                tmp = a[s]
                a[s] = a[e]
                a[e] = tmp
                s += 1
                e -= 1

            e = space
            s = space + 1

        e += 1
    return input_lst
