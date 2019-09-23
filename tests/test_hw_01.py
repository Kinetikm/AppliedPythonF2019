#!/usr/bin/env python
# coding: utf-8

import os

from utils.file_processors import PickleFileProcessor

from homeworks.homework_01.hw1_brseq import is_bracket_correct
from homeworks.homework_01.hw1_arrsearch import find_indices
from homeworks.homework_01.hw1_invertint import reverse
from homeworks.homework_01.hw1_palindrom import check_palindrom
from homeworks.homework_01.hw1_invertdict import invert_dict
from homeworks.homework_01.hw1_winversion import word_inversion
from homeworks.homework_01.hw1_subarr import find_subarr
from homeworks.homework_01.hw1_det import calculate_determinant


def load_test_data(func_name):
    file_processor = PickleFileProcessor()
    test_filename = os.path.basename(__file__)
    test_filename = os.path.splitext(test_filename)[0]
    test_filename = os.path.join("tests/tests_data",
                                 test_filename + "_" + func_name + ".ini.pkl")
    output = file_processor.read_file(test_filename)
    return output


def test_word_inversion():
    data = load_test_data("winversion")
    try:
        word_inversion([])
    except NotImplementedError:
        return True
    for input_lst, result in data:
        output = word_inversion(input_lst)
        assert output == result


def test_subarray_finder():
    data = load_test_data("subarr")
    try:
        find_subarr([], 0)
    except NotImplementedError:
        return True
    for input_data, result in data:
        lst, num = input_data
        indexes = find_subarr(lst, num)
        if indexes:
            assert sum(lst[indexes[0]:indexes[1]+1]) == num
        else:
            assert indexes == result


def test_bracket_sequence():
    data = load_test_data("brseq")
    try:
        is_bracket_correct("()")
    except NotImplementedError:
        return True
    for input_string, result in data:
        output = is_bracket_correct(input_string)
        assert output is result


def test_search_indices():
    data = load_test_data("listscan")
    try:
        find_indices([], 0)
    except NotImplementedError:
        return True
    for lst, n, res in data:
        output = find_indices(lst, n)
        if output is None and res is None:
            assert True
        elif output is None and res[0] != res[1] \
                and lst[res[0]] + lst[res[1]] == n:
            assert False
        else:
            assert output[0] != output[1] \
                   and lst[output[0]] + lst[output[1]] == n


def test_inverse_int():
    data = load_test_data("invertint")
    try:
        reverse(0)
    except NotImplementedError:
        return True
    for inp, out in data:
        assert reverse(inp) == out


def test_palindrom():
    data = load_test_data("palindrom")
    try:
        check_palindrom("")
    except NotImplementedError:
        return True
    for input_string, answer in data:
        assert check_palindrom(input_string) is answer


def test_inverse_dict():
    data = load_test_data("invertdict")
    try:
        invert_dict("")
    except NotImplementedError:
        return True
    for test_case in data:
        input_string, answer = test_case['test_data'], test_case['true']
        output = invert_dict(input_string)
        assert len(answer) == len(output)
        for i in answer:
            if isinstance(answer[i], list):
                assert sorted(answer[i]) == sorted(output[i])
            else:
                assert answer[i] == output[i]


def test_determinant():
    data = load_test_data("det")
    try:
        calculate_determinant([[]])
    except NotImplementedError:
        return True
    for mx, answer in data:
        if answer is None:
            assert calculate_determinant(mx) is None
            continue
        assert abs(calculate_determinant(mx) - answer) / abs(answer) < 0.005
