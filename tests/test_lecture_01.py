#!/usr/bin/env python
# coding: utf-8

from utils.file_processors import TarFileProcessor
from lectures.lecture_01.scripts.submission import calculator


def load_test_data():
    import os
    tarfile_processor = TarFileProcessor()
    test_filename = os.path.basename(__file__)
    test_filename = os.path.splitext(test_filename)[0]
    test_filename = os.path.join("tests/tests_data",
                                 test_filename + ".ini.gz")
    output = tarfile_processor.read_file(test_filename)
    return output


def test_calculator():
    params = load_test_data()
    for arguments in params:
        arguments = arguments.split()
        x = int(arguments[0])
        y = int(arguments[1])
        operation = arguments[2]
        assert calculator(x, y, operation) == int(arguments[3])
