#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LinearRegression:
    def __init__(self, lambda_coef=3.5, regulatization=None, alpha1=0.58, alpha2=0.57, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.regularizarion = 'elastic'
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.w = 0
        self.tol = 0.001
        self.begin = 0

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.w = np.zeros((1, X_train.shape[1] + 1)) + 0.00001
        X_train = np.append(np.ones((X_train.shape[0], 1)), X_train, axis=1)
        for k in range(self.max_iter):
            for p in range((X_train.shape[0] // self.batch_size) + 1):
                X, y = self.get_next_batch(X_train, y_train)
                y = np.array([y]).T
                grad = (sum((np.sign(y - X @ self.w.T) * X)) * (1 / self.batch_size)) + \
                    self.alpha1 * np.sign(self.w) + self.alpha2 * self.w
                old = self.w
                self.w = self.w - self.lambda_coef * grad
            if abs(old - self.w).all() < self.tol:
                break

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        X_test = np.append(np.ones((X_test.shape[0], 1)), X_test, axis=1)
        return (X_test @ self.w.T).T.astype(int)[0]

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.w

    def get_next_batch(self, X_train, y_train):
        if self.begin + self.batch_size <= X_train.shape[0]:
            self.begin += self.batch_size
            return X_train[self.begin - self.batch_size: self.begin], y_train[self.begin - self.batch_size: self.begin]
        else:
            begin = self.begin
            self.begin = 0
            return X_train[begin: X_train.shape[0]], y_train[begin: X_train.shape[0]]
