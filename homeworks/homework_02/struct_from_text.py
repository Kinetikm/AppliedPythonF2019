#!/usr/bin/env python
# coding: utf-8


import json
import csv


def get_struct(text):
    if text == '':
        return None
    try:
        text = json.loads(text)
    except BaseException:
        try:
            text = [i.split("\t") for i in text.strip().split("\n")]
            if len(text) > 2:
                text = [{text[0][k]:cell for k, cell in enumerate(
                    line)} for i, line in enumerate(text) if i > 0]
        except BaseException:
            return None
    return text
