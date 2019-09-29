#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


def check_enc(filename):
    for enc in ("utf-8", "utf-16", "cp1251"):
        try:
            with open(filename, encoding=enc) as f:
                data = f.read()
                return data
        except (UnicodeDecodeError, UnicodeError):
            continue
        except FileNotFoundError:
            print("Файл не валиден")
            return None
    print("Формат не валиден")
    return None


def check_format(data):
    try:
        data = json.loads(data)
        return "json", data
    except:
        try:
            data = data.split("\n")
            return "tsv", data
        except:
            raise
