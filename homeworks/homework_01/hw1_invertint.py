#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    if number >= 0:
        copy = number
    else:
        copy = -1 * number
    ans = 0
    while copy > 0:
        ans = ans * 10 + copy % 10
        copy = copy // 10
    if number >= 0:
        return ans
    else:
        return (-1) * ans

print(reverse(-12345600540))
