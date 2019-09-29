#!/usr/bin/env python
# coding: utf-8

def enc(file):
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
                with open(path_2_file, 'r', encoding='cp1251') as f:
                    f.readline()
                    return 'cp1251'
            except:
                return
