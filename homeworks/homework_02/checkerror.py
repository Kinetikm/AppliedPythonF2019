#!/usr/bin/env python
# coding: utf-8
"""
оштбки
"""


class WrongFormatException(BaseException):
    def __init__(self, text):
        self.text = text


# проверка валидности json
# ножно проверить все ключи
def check_json(data):
    t = set(data[0].keys())
    # print(data)
    for slovar in data:
        if t != set(slovar.keys()):
            raise WrongFormatException("wrong json format")


# проверка валидности csv
# длины массивов
def check_tsv(data):
    # print(len(data[0]))
    t = len(data[0])
    for arra in data:
        if len(arra) != t:
            raise WrongFormatException("wrong json format")
