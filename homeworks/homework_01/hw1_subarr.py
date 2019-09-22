#!/usr/bin/env python
# coding: utf-8


def find_subarr(a, b):
        for i in range(len(a) - 1):
            if a[i] == b:
                return i, i
            elif a[i] + a[i + 1] == b:
                return i, i + 1
        return
