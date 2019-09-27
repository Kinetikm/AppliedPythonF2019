#!/usr/bin/env python
# coding: utf-8


def encoding_define(path_2_file):
    try:
        with open(path_2_file, 'r', encoding='utf-8') as f:
            f.readline()
            return 'utf-8'
    except:
        try:
            with open(path_2_file, 'r', encoding='utf-16') as f:
                f.readline()
                return 'utf-16'
        except:
            try:
                with open(path_2_file, 'r', encoding='windows-1251') as f:
                    f.readline()
                    return 'windows-1251'
            except:
                return
