#!/usr/bin/env python
# coding: utf-8


from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split

from homeworks.homework_06_ml.linear_regression import LinearRegression


def test_simplex_method_01():
    diabetes = datasets.load_diabetes()
    x, y = diabetes["data"], diabetes["target"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    lr1 = linear_model.SGDRegressor()
    try:
        lr2 = LinearRegression(batch_size=50, max_iter=1000)
    except NotImplementedError:
        return True

    lr1.fit(x_train, y_train)
    lr2.fit(x_train, y_train)

    mse1 = mean_squared_error(y_test, lr1.predict(x_test))
    mse2 = mean_squared_error(y_test, lr2.predict(x_test))
    mae1 = mean_absolute_error(y_test, lr1.predict(x_test))
    mae2 = mean_absolute_error(y_test, lr2.predict(x_test))

    assert mse2 < mse1 * 10 or mae2 < mae1 * 10
