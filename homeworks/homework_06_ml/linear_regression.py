#!/usr/bin/env python
# coding: utf-8

import numpy as np


class LinearRegression:

    def __init__(self, lambda_coef=700.0, regulatization=None, alpha=0.5, batch_size=50, max_iter=100):
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

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        num_measures = X_train.shape[0]
        num_features = X_train.shape[1]
        indices = np.arange(num_measures)
        self.theta = np.zeros(num_features)
        gt = np.zeros_like(self.theta)
        e = 0.0000001
        for i in range(self.max_iter):
            np.random.shuffle(indices)
            X_batch = np.take(X_train, indices[:self.batch_size], axis=0)
            y_batch = np.take(y_train, indices[:self.batch_size])
            grad = self.grad(X_batch, y_batch, self.theta)
            gt += grad ** 2
            self.theta = self.theta - self.lambda_coef * grad / self.batch_size / np.sqrt(gt + e)

    def grad(self, x, y, theta):
        grad = np.empty_like(theta)
        num_features = x.shape[1]
        for j in range(num_features):
            grad[j] = sum(x[:, j] * 2 * (x.dot(theta) - y)) + self.alpha * np.sign(theta[j]) + 2 * (1 - self.alpha) * \
                      theta[j] * np.sign(theta[j])
        return grad

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        if X_test.shape[1] != self.theta.shape[0]:
            X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        y_test = X_test @ self.theta
        return y_test

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.theta
