#!/usr/bin/env python
# coding: utf-8


import os


def type_of_file(file):
    filename, file_extension = os.path.splitext(file)
    return file_extension[1:]
# метод получения типа файла: tsv или json
