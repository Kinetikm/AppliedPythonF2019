#!/usr/bin/env python
# coding: utf-8

import json


def opening(filename):
    encoding = ["utf8", "cp1251",  "utf16", "ASCII"]
    json_status = False
    for enc in encoding:
        try:
            with open(filename, "r", encoding=enc) as f:
                data = json.load(f)
                json_status = True
                break
        except json.decoder.JSONDecodeError:
            with open(filename, "r", encoding=enc) as f:
                data = f.read()
                json_status = False
                break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            return "file_not_found", False
    else:
        raise UnicodeDecodeError("Неизвестная кодировка")
    return data, json_status
