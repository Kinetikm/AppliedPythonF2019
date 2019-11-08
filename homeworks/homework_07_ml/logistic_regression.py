#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, lambda_coef=1.0, regulatization=None, alpha=0.00005, batch_size=50, max_iter=100):
        self.lambda_coef = lambda_coef
        self.regularization = regulatization
        self.alpha1 = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.alpha2 = alpha
        self.weight = 0

    def fit(self, x_train, y_train):
        y_train = y_train.reshape((-1, 1))
        t_train = np.hstack((np.ones((x_train.shape[0], 1)), x_train, y_train))
        self.weight = np.random.normal(scale=1e-5, size=(1, x_train.shape[1] + 1))
        for iter_ in range(self.max_iter):
            perm = np.random.permutation(t_train)[:self.batch_size]
            x = perm[:, :-1]
            y = perm[:, -1].reshape(-1, 1)
            self.weight += self.lambda_coef * self.gradient(x, y) / self.batch_size

    def predict(self, x_test):
        border = 0.5
        y = self.predict_proba(x_test)
        y[y >= border] = 1
        y[y < border] = 0
        return y

    def predict_proba(self, x_test):
        x_test = np.hstack((np.ones((x_test.shape[0], 1)), x_test))
        return self.sigm(x_test.dot(self.weight.T)).squeeze()

    def get_weights(self):
        return self.weight

    def gradient(self, x, y):
        grad_el = np.empty_like(self.weight)
        for j in range(self.weight.shape[1]):
            grad_el[0, j] = np.sum((y.reshape(-1, 1) - self.sigm(x.dot(self.weight.T)).reshape(-1, 1)) * x[:, j])
            grad_el[0, j] += self.alpha1 * (1 - self.alpha2) * self.weight[0, j] + (self.alpha1 *
                                                                                    self.alpha2 *
                                                                                    np.sign(self.weight[0, j]))
        return grad_el

    def sigm(self, z):
        return 1 / (1 + np.exp(-z))
