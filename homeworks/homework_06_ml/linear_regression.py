#!/usr/bin/env python
# coding: utf-8
import numpy as np
from random import randint


class LinearRegression:
    def __init__(self, lambda_coef=1.0, regulatization=None, alpha=0.5, batch_size=50, max_iter=100):
        self.lambda_coef = lambda_coef
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.weights = np.array([])

    def grad_mae(self, x, y):
        x_n = np.hstack([x, np.ones((self.batch_size, 1))])
        w = np.transpose(self.weights)
        grad = np.zeros((1, x_n.shape[1]))
        for i in range(x_n.shape[1]):
            for j in range(x_n.shape[0]):
                grad[0, i] -= np.sign(y[j] - (x_n[j, ::] @ w)) * x_n[j, i] / self.batch_size
            grad[0, i] -= np.sign(w[i, 0]) * self.alpha
        return grad

    def fit(self, X_train, y_train):
        m = np.zeros((1, X_train.shape[1] + 1))
        v = np.zeros((1, X_train.shape[1] + 1))
        w = np.zeros((1, X_train.shape[1] + 1))
        self.weights = w
        self.normal(X_train)
        b_n = randint(0, X_train.shape[0] - self.batch_size)
        batch_x = X_train[b_n:b_n + self.batch_size, ::]
        batch_y = y_train[b_n:b_n + self.batch_size]

        for t in range(1, self.max_iter):
            g = self.grad_mae(batch_x, batch_y)
            m = 0.9 * m + (1 - 0.9) * g
            v = 0.999 * v + (1 - 0.999) * np.power(g, 2)
            m_hat = m / (1 - np.power(0.9, t))
            v_hat = v / (1 - np.power(0.999, t))
            w = w - self.lambda_coef * m_hat / (np.sqrt(v_hat) + 0.00000001)
            self.weights = w

    def normal(self, x):
        mean = x.mean(axis=1)
        std = np.std(x, axis=1)
        for j in range(x.shape[0]):
            if std[j] > 0:
                x[j, :] = (x[j, :] - mean[j]) / std[j]

    def predict(self, X_test):
        X = np.hstack([X_test, np.ones((X_test.shape[0], 1))])
        w_t = np.transpose(self.weights)
        return X @ w_t

    def get_weights(self):
        return self.weights
