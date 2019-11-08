#!/usr/bin/env python
# coding: utf-8


import numpy as np
from sklearn.utils import gen_batches


def sigmoid(x):
    return 1/(1 + np.exp(-x))


class LogisticRegression:

    def __init__(self, batch_size=50, max_iter=10):
        self.batch_size = batch_size
        self.max_iter = max_iter

    def fit(self, X_train, y_train):
        N = len(y_train)
        self.weigths = np.random.rand(X_train.shape[1] + 1)
        X_train = np.append(np.ones(N).reshape(1, -1).T, X_train, axis=1)
        eps = 1e-4
        learning_rate = 1e-4
        m, v = 0, 0
        b1, b2 = 0.9, 0.99
        for i in range(self.max_iter):
            for j, batch in enumerate(gen_batches(N, self.batch_size)):
                X = X_train[batch]
                y = y_train[batch]
                g = self.gradient(X, y)

                m = b1 * m + (1 - b1) * g
                v = b2 * v + (1 - b2) * np.square(g)

                t = i * int(N / self.batch_size) + j + 1

                m_mean = m / (1 - np.power(b1, t))
                v_mean = v / (1 - np.power(b2, t))
                self.weigths -= learning_rate * m_mean / (np.sqrt(v_mean) + eps)

    def gradient(self, X, y):
        coef_l1 = 1
        res = X.T @ (sigmoid(X @ self.weigths) - y) / len(y) + coef_l1 * np.abs(self.weigths)
        return res

    def predict(self, X_test):
        return np.int64(self.predict_proba(X_test) > 0.5)

    def predict_proba(self, X_test):
        return sigmoid(np.append(np.ones(X_test.shape[0]).reshape(1, -1).T, X_test, axis=1) @ self.weigths)

    def get_weights(self):
        return self.weigths
