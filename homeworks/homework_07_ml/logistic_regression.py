#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, lambda_coef=1.0, regulatization=None, alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self._lr = lambda_coef
        if regulatization == 'L2':
            raise NotImplementedError
        else:
            self._regul = regulatization
        self._alpha = alpha
        self._batch_size = batch_size
        self._miter = max_iter
        self._theta = None
        self._treshold = 0.5

    @staticmethod
    def __batch(iterable, n=1):
        current_batch = []
        for item in iterable:
            current_batch.append(item)
            if len(current_batch) == n:
                yield current_batch
                current_batch = []
        if current_batch:
            yield current_batch

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self._theta = np.random.normal(scale=0.1, size=X_train.shape[1])
        vt = np.zeros_like(self._theta)
        x_t = X_train.copy()
        y_t = y_train.copy()
        for epoch in range(self._miter):
            for xbatch, ybatch in zip(self.__batch(x_t, self._batch_size), self.__batch(y_t, self._batch_size)):
                xbatch = np.array(xbatch)
                ybatch = np.array(ybatch)
                vt = 0.2 * vt + self._lr * self.grad(xbatch, ybatch) / X_train.shape[0]
                self._theta -= vt
            sh_nums = np.arange(len(y_t))
            np.random.shuffle(sh_nums)
            sh_x_t = np.array([x_t[i] for i in sh_nums])
            x_t = sh_x_t
            sh_y_t = np.array([y_t[i] for i in sh_nums])
            y_t = sh_y_t

    def grad(self, x, y):
        grad = (x.T @ (self.predict_proba(x) - y)) / x.shape[0]
        if self._regul:
            grad += 2 * self._alpha * self._theta * np.sign(self._theta)
        return grad

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_pred = map(lambda x: 1 if x >= self._treshold else 0, self.predict_proba(X_test))
        return np.array([*y_pred])

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        y_prob = map(lambda x: 1 / (1 + np.exp(-x)), X_test @ self._theta)
        return np.array([*y_prob])

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self._theta
