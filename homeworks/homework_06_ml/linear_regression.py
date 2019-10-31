#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib as plt


class LinearRegression:
    def __init__(self, lambda_coef=1.0, regulatization=None, alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.regulatization = regulatization
        self.alpha = alpha
        self.batch = batch_size
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
        ones = np.ones(X_train.shape[0])
        y_train = y_train.reshape(-1, 1)
        matrix = np.hstack((ones.reshape(-1, 1), X_train, y_train))
        self.weights = np.random.rand(np.shape(matrix)[1] - 1)
        eps = 1e-7
        # ADAM
        m = 0
        v = 0
        b1 = 0.8
        b2 = 0.8
        for i in range(self.max_iter):
            permatrix = np.random.permutation(matrix)[:self.batch]
            x = permatrix[:, :-1]
            y = permatrix[:, -1]
            grad = self.grad(x, y)
            m = b1 * m + (1 - b1) * grad
            v = b2 * v + (1 - b2) * (grad ** 2)
            mt = m / (1 - b1)
            vt = v / (1 - b2)
            self.weights -= self.lambda_coef * mt/((vt + eps)**(1/2))

    def normalize(self, X):
        for i in range(X.shape[0]):
            mean = sum(X[i, :]) / X.shape[1]
            std = np.sqrt(sum((X[i, :] - mean)**2) / X.shape[1])
            X[i, :] = (X[i, :] - mean) / std
        return X

    def grad(self, x, y):
        l1 = self.weights * self.alpha
        return 2 * (x.T.dot((x.dot(self.weights) - y)) + l1)

    def predict(self, X_test):
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        y_test = X_test.dot(self.weights.T)
        return y_test

    def get_weights(self):
        return self.weights
