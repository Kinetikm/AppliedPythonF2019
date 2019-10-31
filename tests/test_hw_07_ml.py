#!/usr/bin/env python
# coding: utf-8

import numpy as np
from sklearn import linear_model
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split

from homeworks.homework_07_ml.logistic_regression import LogisticRegression


def test_simplex_method_01():
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

    lr1 = linear_model.LogisticRegression()
    try:
        lr2 = LogisticRegression(batch_size=500, max_iter=1000)
    except NotImplementedError:
        return True

    lr1.fit(x_train, y_train)
    lr2.fit(x_train, y_train)

    # check predict works
    assert lr2.predict(x_test).shape == y_test.shape

    loss1 = log_loss(y_test, lr1.predict_proba(x_test))
    loss2 = log_loss(y_test, lr2.predict_proba(x_test))

    assert loss2 < loss1 * 2
