#!/usr/bin/env python
# coding: utf-8

import numpy as np
from sklearn.utils import shuffle


class LinearRegression:
    def __init__(self, lambda_coef=1.0, alpha=1, batch_size=50, max_iter=100):
        self.L = lambda_coef
        self.alpha = alpha
        self.b = batch_size
        self.max_iter = max_iter
        self.weights = None

    def fit(self, X_train, y_train):
        np.random.seed(1)
        self.normalization(X_train)
        y_train = y_train.reshape(-1, 1)
        table = np.hstack((np.ones((X_train.shape[0], 1)), X_train, y_train))
        self.weights = 2 * np.random.random((1, np.shape(X_train)[1] + 1)) - 1
        eps = 1e-3
        for _ in range(self.max_iter):
            table = shuffle(table)
            for i in range(0, X_train.shape[0], self.b):
                sample = table[i: i + self.b]
                x = sample[:, : -1]
                y = sample[:, -1].reshape(-1, 1)
                for i in range(x.shape[0]):
                    old_w = np.copy(self.weights)
                    self.weights -= self.L * self.grad_step(x, y, i) / self.b
                ex = True
                for i in range(len(self.weights)):
                    if ex:
                        ex = abs(self.weights[0, i] - old_w[0, i]) < eps
                    else:
                        break
                if ex:
                    break

    def normalization(self, X):
        means, stds = np.mean(X, axis=0), np.std(X, axis=0)
        for num in range(len(X)):
            for i in range(X.shape[1]):
                X[num, i] = (X[num, i] - means[i])/stds[i]

    def grad_step(self, x, y, i):
        L1 = self.alpha*(np.sign(self.weights))
        pred = x[i].dot(self.weights.T).reshape(-1, 1)
        grad = 2 * x[i].reshape(-1, 1).dot(pred - y[i]) + L1.T
        return grad.T

    def predict(self, X_test):
        test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return test.dot(self.weights.T)

    def get_weights(self):
        return self.weights
