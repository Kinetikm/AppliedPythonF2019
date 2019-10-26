#!/usr/bin/env python
# coding: utf-8
import numpy as np


class LinearRegression:
    def __init__(self, lambda_coef=200.0, regularization=None, alpha=0.5, batch_size=50, max_iter=100, normalize=True):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.regularization = regularization
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.w = 0
        self.loss = []
        self.normalize = normalize

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        if self.normalize:
            X_train = self._normalize(X_train)

        n = X_train.shape[1]
        y_train = y_train.reshape((-1, 1))
        table = np.hstack((np.ones((X_train.shape[0], 1)), X_train, y_train))
        self.w = np.random.normal(scale=1e-5, size=(1, n+1))
        g_update = np.zeros_like(self.w)
        eps = 1e-8
        for iter_ in range(self.max_iter):
            perm = np.random.permutation(table)[:self.batch_size]
            x = perm[:, :-1]
            y = perm[:, -1].reshape(-1, 1)
            err1 = sum(abs(x.dot(self.w.T) - y))/self.batch_size
            grad = self._grad(x, y, self.w)
            g_update += grad ** 2
            self.w -= self.lambda_coef * grad / np.sqrt(g_update + eps)/self.batch_size
            err2 = sum(abs(x.dot(self.w.T) - y))/self.batch_size
            self.loss.append(err2)

    def _normalize(self, X):
        n = X.shape[1]
        for i in range(X.shape[0]):
            m = sum(X[i, :])/n
            s = np.sqrt(sum((X[i, :] - m)**2) / n)
            X[i, :] = (X[i, :] - m)/s
        return X

    def _grad(self, x, y, w):
        gr = np.empty_like(w)
        for j in range(w.shape[1]):
            gr[0, j] = sum(x[:, j].reshape(-1, 1)*np.sign(x.dot(w.T) - y)) + self.alpha*(np.sign(w[0, j]))
        return gr

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return X_test.dot(self.w.T)

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.w
