#!/usr/bin/env python
# coding: utf-8

import numpy as np
from random import randint


class LinearRegression:
    def __init__(self, lambda_coef=1.0, alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.weights = None

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.normalize(X_train)
        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        cols = X_train.shape[1]
        self.weights = np.zeros((1, cols))
        for _ in range(self.max_iter):
            batch_n = randint(0, X_train.shape[0] - self.batch_size)
            batch_x = X_train[batch_n:batch_n + self.batch_size, ::]
            batch_y = y_train[batch_n:batch_n + self.batch_size]
            sum_w = np.empty((1, self.weights.shape[1]))
            for i in range(batch_x.shape[0]):
                sum_w += self.lambda_coef * self.grad_mse(batch_x, batch_y, i) / self.batch_size
            self.weights -= sum_w / self.batch_size

    def grad_mse(self, x, y, i):
        l_reg = self.alpha*(np.sign(self.weights))
        mb = x[i].dot(self.weights.T).reshape(-1, 1)
        grad_ms = 2 * x[i].reshape(-1, 1).dot(mb - y[i]) + l_reg.T
        return grad_ms.T

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        pred = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return pred.dot(self.weights.T)

    def normalize(self, x):
        x_mean = x.mean(axis=1)
        x_std = np.std(x, axis=1)
        for i in range(x.shape[0]):
            if x_std[i] > 0:
                x[i, :] = (x[i, :] - x_mean[i]) / x_std[i]

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.weights
