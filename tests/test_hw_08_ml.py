#!/usr/bin/env python
# coding: utf-8

from homeworks.homework_08_ml.tfidf_vectorizer import TfIdfVectorizer
import math
import random
import os
from shutil import rmtree


def test_output_dictionary():
    try:
        vectorizer = TfIdfVectorizer(0.05, 0.95, (1, 2), -1)
    except NotImplementedError:
        return True
    seed = random.random()
    if os.path.exists("tmp_test_{}".format(seed)):
        rmtree("tmp_test_{}".format(seed))
    os.mkdir("tmp_test_{}".format(seed))
    vectorizer.fit("./homeworks/homework_08_ml/test_data", "tmp_test_{}".format(seed))
    vectorizer.idfs("tmp_file_{}".format(seed))
    check_dict = {"колдун":	2.69547141889535,
                  "горшок":	2.3770176877768154,
                  "и": 1.4977682275830093,
                  "с": 2.2900063107871858,
                  "город":  2.9831534913471307,
                  "под_подошва": 2.9831534913471307,
                  "подошва": 2.9831534913471307,
                  "город_под": 2.9831534913471307}
    with open("tmp_file_{}".format(seed), "r") as f:
        for line in f:
            spls = line.strip().split()
            if spls[0] in check_dict:
                assert math.isclose(check_dict[spls[0]], float(spls[1]), rel_tol=0.05)
                check_dict[spls[0]] = -1
    for v in check_dict.values():
        assert v == -1
    rmtree("tmp_test_{}".format(seed))
    os.remove("tmp_file_{}".format(seed))
