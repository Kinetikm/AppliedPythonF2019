#!/usr/bin/env python
# coding: utf-8

import numpy as np


class LinearRegression:
    def __init__(self, alpha=0.5, etta=0.9,  batch_size=50, max_iter=100):
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.w = np.array([])
        self.loss = []
        self.etta = etta

    def fit(self, x_train, y_train):
        """
        Fit model using gradient descent method
        :param x_train: training data
        :param y_train: target values for training data
        :return: None
        """
        row = x_train.shape[0]
        col = x_train.shape[1]
        table = np.hstack((np.ones((row, 1)), x_train, y_train.reshape(-1, 1)))
        self.w = np.random.normal(size=(1, col + 1))
        v_i = np.zeros_like(self.w)
        for itr in range(self.max_iter):
            table = np.random.permutation(table)
            for i in np.arange(0, row, self.batch_size):
                x = table[i:i + self.batch_size, 0:-1]
                y = table[i:i + self.batch_size, -1].reshape((-1, 1))
                v_i = self.etta * v_i + self.alpha * self.nag(x, y, v_i)
                self.w -= v_i
            self.loss.append(sum(abs(table[:, 0:-1].dot(self.w.T) - table[:, -1])) / row)

    def nag(self, x, y, v_i):
        gradient = np.empty_like(self.w)
        for i in range(self.w.shape[1]):
            gradient[0, i] = (sum(x[:, i].reshape(-1, 1) * np.sign(x.dot((self.w - self.etta * v_i).T) - y))) /\
                             x.shape[0] + self.alpha * np.sign(self.w[0, i] - self.etta * v_i[0, i])
        return gradient

    def predict(self, x_test):
        """
        Predict using model.
        :param x_test: test data for predict in
        :return: y_test: predicted values
        """
        x_test = np.hstack((np.ones((x_test.shape[0], 1)), x_test))
        return x_test.dot(self.w.T)

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.w
