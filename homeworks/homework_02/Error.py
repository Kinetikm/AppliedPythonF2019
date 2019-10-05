#!/usr/bin/env python
# coding: utf-8


class WrongFormatException(BaseException):
    def __init__(self, text):
        self.text = text


def check_json(data):
    t = set(data[0].keys())
    for dict_ in data:
        if t != set(dict_.keys()):
            raise WrongFormatException("wrong json format")


def check_tsv(data):
    t = len(data[0])
    for array in data:
        if len(array) != t:
            raise WrongFormatException("wrong json format")
