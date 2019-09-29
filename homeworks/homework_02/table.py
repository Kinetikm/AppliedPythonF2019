#!/usr/bin/env python
# coding: utf-8

import sys
import coding
import readtsv
import drawtab
import filetype

if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        with open(filename, "rb") as file:
            string = file.read()
    except FileNotFoundError:
        print("Файл не валиден")
    else:
        coding = coding.detect_coding(string)
        result = filetype.define_type(filename, coding)
        if type(result) == str:
            if result == 'Not json':
                data = readtsv.read(filename, coding)
            else:
                print(result)
        else:
            data = result
        if data:
            drawtab.draw_table(data)
