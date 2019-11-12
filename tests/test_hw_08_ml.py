#!/usr/bin/env python
# coding: utf-8
import math
import os
import random
from shutil import rmtree

import numpy as np
from sklearn import datasets
from sklearn.metrics import log_loss, mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from homeworks.homework_08_ml.tfidf_vectorizer import TfIdfVectorizer
from homeworks.homework_08_ml.tree import TreeClassifier, TreeRegressor


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


def test_tree_classifier():
    size = 5000
    n_feat = 20

    np.random.seed(0)

    C1 = np.random.randn(n_feat, n_feat) * 5
    C2 = np.random.randn(n_feat, n_feat) * 5
    gauss1 = np.dot(np.random.randn(size, n_feat) + np.random.randn(n_feat) * 0.3, C1)
    gauss2 = np.dot(np.random.randn(size, n_feat) + np.random.randn(n_feat) * 0.3, C2)

    x = np.vstack([gauss1, gauss2])
    y = np.r_[np.ones(size), np.zeros(size)]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    lr1 = DecisionTreeClassifier(max_depth=5, min_samples_leaf=8)
    try:
        lr2 = TreeClassifier(max_depth=5, min_samples_leaf=8)
    except NotImplementedError:
        return True

    lr1.fit(x_train, y_train)
    lr2.fit(x_train, y_train)

    # check predict works
    assert lr2.predict(x_test).shape == y_test.shape

    loss1 = log_loss(y_test, lr1.predict_proba(x_test))
    loss2 = log_loss(y_test, lr2.predict_proba(x_test))

    assert loss2 < loss1 * 2


def test_tree_regressor():
    diabetes = datasets.load_diabetes()
    x, y = diabetes["data"], diabetes["target"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    lr1 = DecisionTreeRegressor(max_depth=5, min_samples_leaf=8)
    try:
        lr2 = TreeRegressor(max_depth=5, min_samples_leaf=8)
    except NotImplementedError:
        return True

    lr1.fit(x_train, y_train)
    lr2.fit(x_train, y_train)

    mse1 = np.sqrt(mean_squared_error(y_test, lr1.predict(x_test)))
    mse2 = np.sqrt(mean_squared_error(y_test, lr2.predict(x_test)))
    mae1 = mean_absolute_error(y_test, lr1.predict(x_test))
    mae2 = mean_absolute_error(y_test, lr2.predict(x_test))

    assert mse2 < mse1 * 2 or mae2 < mae1 * 2
