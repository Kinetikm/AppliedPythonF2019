import json
import os.path


def read_file(filename):
    if not os.path.exists(filename):
        print("Файл не валиден")
        return
    file = None
    try:
        file = open(filename, encoding='utf-8')
    except UnicodeError as err:
        try:
            file = open(filename, encoding='utf-16')
        except UnicodeError as err:
            try:
                file = open(filename, encoding='cp1251')
            except UnicodeTranslateError as err:
                print("Формат не валиден")
