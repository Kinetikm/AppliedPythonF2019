#!/usr/bin/env python
# coding: utf-8

import numpy as np

"""
var 3
loss: MSE
regularization: l1
optim: adam

"""


class LinearRegression:
    def __init__(self, lambda_coef=1.0, regularization=None, alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        if regularization == "L2":
            raise NotImplementedError
        self._lambda = lambda_coef
        self._regularization = regularization or "L1"
        self._alpha = alpha
        self._batch_size = batch_size
        self._max_iter = max_iter
        self._epsilon = 0.1
        self._weights = np.array([0])

    def __norm(self, vector):
        return np.sqrt(sum(vector ** 2))

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self._weights = np.random.rand(X_train.shape[1])
        X_train = self.__normalize(X_train)
        beta_1 = 0.9
        beta_2 = 0.9
        m = 0
        v = 0
        for i in range(self._max_iter):
            for x_batch, y_batch in self.__get_next_batch(X_train, y_train):
                g = self.__grad(x_batch, y_batch)
                m = beta_1 * m + (1 - beta_1) * g
                v = beta_2 * v + (1 - beta_2) * (g ** 2)
                m_hat = m / (1 - (beta_1 ** (i + 1)))
                v_hat = v / (1 - (beta_2 ** (i + 1)))
                self._weights -= self._lambda * m_hat / np.sqrt(v_hat + self._epsilon)
            if (self.predict(X_train) - y_train).all() < self._epsilon:
                break

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        return X_test @ self._weights.T

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self._weights

    def __loss(self, x, y):
        return sum(x @ self._weights.T - y) / x.shape[1]

    def __get_next_batch(self, x, y, n=[]):
        if not n:
            n.append(0)
        beg = self._batch_size * (n[0] - 1) % x.shape[0]
        end = self._batch_size * n[0] % x.shape[0]
        n[0] += 1
        yield (x[beg:end], y[beg:end])

    def __grad(self, x, y):
        return 2 * (x.T @ (x @ self._weights - y) + self._weights * self._alpha)

    def __normalize(self, vector):
        return vector / self.__norm(vector)
