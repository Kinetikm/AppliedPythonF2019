#!/usr/bin/env python
# coding: utf-8
def find_subarr(a, b):
    p=tuple()
    for i in range(len(a)):
        for j in range(len(a)):
            if sum(a[i:j]) == b:
                print(a[i:j])
                return i, j - 1
        return p
