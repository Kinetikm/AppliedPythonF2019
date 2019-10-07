#!/usr/bin/env python
# coding: utf-8

from homeworks.homework_04.hw4_wordcounter import word_count_inference
import math


def test_output_dictionary():
    try:
        output = word_count_inference("./homeworks/homework_04/test_data")
    except NotImplementedError:
        return True
    answer = {'file_02': 0, 'file_06': 184, 'file_04': 209, 'file_03': 854, 'file_07': 607,
              'file_09': 4, 'file_01': 0, 'total': 2093, 'file_05': 235}
    for k, v in answer.items():
        assert k in output
        assert math.isclose(output[k], answer[k], rel_tol=0.05)
