#!/usr/bin/env python
# coding: utf-8


def encoding(file_name):
    for enc in ('utf-8', 'utf-16', 'windows-1251'):
        with open(file_name, 'r', encoding=enc) as f:
            try:
                f.read()
                return enc
            except (UnicodeDecodeError, UnicodeError):
                print("Формат не валиден")
            except FileNotFoundError:
                print("Файл не валиден")
    return None
