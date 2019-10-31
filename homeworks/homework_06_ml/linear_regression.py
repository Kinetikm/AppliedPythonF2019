#!/usr/bin/env python
# coding: utf-8
import numpy as np


class LinearRegression:
    def __init__(self, lambda_coef=0.1, alpha=0.5, l1_ratio=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self._lc = lambda_coef
        self._alpha = alpha
        self._l1_ratio = l1_ratio
        self._batch_size = batch_size
        self._max_iter = max_iter
        self._weight = np.array([])
        self._loss = []

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        if X_train.shape[0] != y_train.shape[0]:
            raise AssertionError

        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        rows = X_train.shape[0]
        cols = X_train.shape[1]
        self._weight = np.random.normal(size=cols)
        for epoch in range(self._max_iter):
            data = np.hstack((X_train, y_train.reshape((-1, 1))))
            np.random.shuffle(data)
            X_train = data[:, : -1]
            y_train = data[:, -1].flatten()
            for i in np.arange(0, rows, self._batch_size):
                batch = X_train[i:i + self._batch_size]
                y = y_train[i:i + self._batch_size]
                pred = batch @ self._weight.T
                f_error = pred - y
                gradient = 2 * f_error.dot(batch) + self._alpha * self._l1_ratio * np.sign(
                    self._weight) + self._alpha * (1 - self._l1_ratio) * self._weight
                self._weight -= self._lc * gradient / batch.shape[0]
            self._loss.append(self.mse(X_train @ self._weight.T, y_train))

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        data = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        if data.shape[1] != self._weight.T.shape[0]:
            raise AssertionError
        return data @ self._weight.T

    def mse(self, y1, y2):
        return np.mean((y1 - y2) ** 2)

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self._weight
