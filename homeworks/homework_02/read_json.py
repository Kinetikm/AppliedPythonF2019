#!/usr/bin/env python
# coding: utf-8


import json


def json_reader(file_name, encode):
    try:
        with open(file_name, "r", encoding=encode) as file:
            return json.load(file, object_hook=dict, parse_int=str)
    except FileNotFoundError:
        print("Файл не валиден")
        return None
    except (UnicodeDecodeError, UnicodeError):
        print("Формат не валиден")
        return None
