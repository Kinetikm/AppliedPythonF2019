#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, lmbd_coef=1e-2, a=1e-3, batch_size=50, max_iter=100):
        self.coef = lmbd_coef
        # regilarization = l1
        self.a = a
        self.size = batch_size
        self.max = max_iter
        self.min_proba = 0.95

    def fit(self, X_train, y_train):
        X_train = self.normalize(X_train)
        y_train = y_train.reshape((-1, 1))
        matrix = np.hstack((np.ones((X_train.shape[0], 1)), X_train, y_train))
        self.w = np.random.normal(size=(1, X_train.shape[1] + 1))
        eps = 0.001
        for _ in range(self.max):
            ind = np.random.permutation(np.arange(matrix.shape[0]))
            for i in range(int(X_train.shape[0] / self.size)):
                perm = ind[i * self.size: (i + 1) * self.size]
                x = matrix[perm, :-1]
                y = matrix[perm, -1]
                # gradient
                cost = self.cost_func(x, y)
                old_cost = cost
                self.w -= self.coef * self.log_gradient(x, y)
                cost = self.cost_func(x, y)
                diff = old_cost - cost
                if diff > eps:
                    break

    def predict(self, X_test):
        proba = self.predict_proba(X_test)
        pred_value = np.where(proba >= self.min_proba, 1, 0)
        return np.squeeze(pred_value)

    def predict_proba(self, X_test):
        X_test = self.normalize(X_test)
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return np.squeeze(self.logistic_func(X_test))

    def get_weights(self):
        return self.w

    def logistic_func(self, x):
        pred = 1.0 / (1.0 + np.exp(-np.dot(x, self.w.T)))
        return pred

    def log_gradient(self, X, y):
        diff = self.logistic_func(X) - y.reshape(X.shape[0], -1)
        return np.dot(diff.T, X) + np.squeeze(self.a * np.sign(self.w.T))

    def cost_func(self, X, y):
        log_func_v = np.squeeze(self.logistic_func(X))
        y = np.squeeze(y)
        final = -(y * np.log(log_func_v)) - ((1-y) * np.log(1-log_func_v))
        return np.mean(final)

    def normalize(self, X):
        mins = np.min(X, axis=0)
        maxs = np.max(X, axis=0)
        rng = maxs - mins
        norm = 1 - ((maxs - X) / rng)
        return norm
