#!/usr/bin/env python
# coding: utf-8


import csv


def tsv_reader(file_name, encode):
    try:
        with open(file_name, "r", encoding=encode) as file:
            string = []
            for x in file.read().split("\n"):
                string.append(x.split("\t"))
            new_dict = {}
            for j in range(1, len(string) - 1):
                for value in zip(string[0], string[j]):
                    new_dict = {key: value for key, value in zip(string[0], string[j])}
            return new_dict
    except FileNotFoundError:
        print("Файл не валиден")
        return None
    except (UnicodeDecodeError, UnicodeError):
        print("Формат не валиден")
        return None
