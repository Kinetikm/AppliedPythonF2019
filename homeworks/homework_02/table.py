#!/usr/bin/env python
# coding: utf-8


from checkerror import *
from output import *
from readopen import *


if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        coding = define_coding(filename)
        # print(coding)
        data = data(filename, coding)
        table(data)
    except FileNotFoundError:
        print("Файл не валиден")
    except WrongFormatException:
        print("Формат не валиден")
