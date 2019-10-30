#!/usr/bin/env python
# coding: utf-8


import numpy as np
from sklearn.linear_model import ElasticNet


class LinearRegression:
    def __init__(self, lambda_coef=1.0, regulatization=None, alpha=0.5, batch_size=50, max_iter=100):
        self.lambda_coef = lambda_coef
        self.regularization = regulatization
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.w = None

    def count_mse(self, y, x, w, n_samples):
        mse = (y - x @ w.T) ** 2
        return np.mean(mse) + self.alpha * (0.5 * np.linalg.norm(w) + 0.25 * np.linalg.norm(w, ord=1))

    def count_gradient(self, x, w, y, l1_ratio=0.5):
        d_mse_dw = 2 * (x @ w.T - y) / x.shape[0]
        gradient = d_mse_dw @ x + self.alpha * l1_ratio * np.sign(w) + self.alpha * (1 - l1_ratio) * w
        return gradient

    def fit(self, X_train, y_train):
        X_train = np.append(np.ones((X_train.shape[0], 1)), X_train, axis=1)
        w = np.zeros(X_train.shape[1])
        n_samples = min(self.batch_size, X_train.shape[0])
        for i in range(self.max_iter):
            if n_samples != X_train.shape[0]:
                idx = np.random.randint(X_train.shape[0], size=n_samples)
                batch = X_train[idx, :]
            else:
                batch = X_train
            d_mse_d_w = self.count_gradient(X_train, w, y_train)
            rms = np.sqrt(sum(d_mse_d_w ** 2) / n_samples)
            w = w - (self.lambda_coef / rms) * d_mse_d_w
        self.w = w.T

    def predict(self, X_test):
        if self.w is not None:
            X_test = np.append(np.ones((X_test.shape[0], 1)), X_test, axis=1)
            y_test = X_test @ self.w
            return y_test

    def get_weights(self):
        if self.w is not None:
            return self.w
