#!/usr/bin/env python
# coding: utf-8

import numpy as np
from sklearn import datasets
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split

from homeworks.homework_09_ml.boosting import GradientBoosting


def test_tree_regressor():
    diabetes = datasets.load_diabetes()
    x, y = diabetes["data"], diabetes["target"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    lr1 = GradientBoostingRegressor(max_depth=5, min_samples_leaf=8, subsample=0.8, n_estimators=100)
    try:
        lr2 = GradientBoosting(max_depth=5, min_samples_leaf=8, subsample=0.8, n_estimators=100)
    except NotImplementedError:
        return True

    lr1.fit(x_train, y_train)
    lr2.fit(x_train, y_train)

    mse1 = np.sqrt(mean_squared_error(y_test, lr1.predict(x_test)))
    mse2 = np.sqrt(mean_squared_error(y_test, lr2.predict(x_test)))
    mae1 = mean_absolute_error(y_test, lr1.predict(x_test))
    mae2 = mean_absolute_error(y_test, lr2.predict(x_test))

    assert mse2 < mse1 * 2 or mae2 < mae1 * 2
