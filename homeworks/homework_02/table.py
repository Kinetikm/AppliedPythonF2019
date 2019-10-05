#!/usr/bin/env python
# coding: utf-8


from Error import *
from Print_table import *
from open_file import *


if __name__ == '__main__':
    fname = sys.argv[1]
    try:
        coding = define_coding(fname)
        data = data(filename, coding)
        table(data)
    except FileNotFoundError:
        print("Файл не валиден")
    except WrongFormatException:
        print("Формат не валиден")
