#!/usr/bin/env python
# coding: utf-8


import chardet

enc_types = ['utf-8', 'utf-16', 'windows-1251']


def encoding_define(path_2_file):
    with open(path_2_file, 'r') as f:
        enc = chardet.detect(f.readline())['encoding']
        if enc in enc_types:
            return enc
        return
