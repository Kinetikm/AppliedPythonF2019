#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LinearRegression:
    def __init__(self, lmbd_coef=0.9, alpha=0.01, batch_size=50, max_iter=100):
        self.coef = lmbd_coef
        self.a = alpha
        self.max = max_iter
        self.size = batch_size

    def fit(self, X_train, y_train):
        y_train = y_train.reshape((-1, 1))
        matrix = np.hstack((np.ones((X_train.shape[0], 1)), X_train, y_train))
        self.w = np.random.normal(scale=20, size=(1, X_train.shape[1] + 1))
        # adadelta
        e_g = 0
        e_w = 0
        eps = 1e-8
        g = self.coef
        grad = 0
        rms_w = 100
        for _ in range(self.max):
            ind = np.random.permutation(np.arange(matrix.shape[0]))
            for i in range(int(X_train.shape[0] / self.size)):
                perm = ind[i * self.size: (i + 1) * self.size]
                x = matrix[perm, :-1]
                y = matrix[perm, -1]
                # gradient
                sign = np.sign(x.dot(self.w.T) - y.reshape(-1, 1))
                l2 = self.a / 2 * self.w.T
                n_grad = (np.apply_along_axis(self.gradient, 0, x, sign))
                n_grad = n_grad.reshape(-1, 1) + l2.reshape(-1, 1)
                # adadelta
                e_g = g * e_g + (1 - g) * (n_grad**2)
                rms_g = np.sqrt(e_g + eps)
                delta_w = - (rms_w / rms_g) * n_grad
                e_w = g * e_w + (1 - g) * (delta_w ** 2)
                rms_w = np.sqrt(e_w + eps)
                self.w = self.w + delta_w.T

    def predict(self, X_test):
        x = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return x @ self.w.T

    def get_weights(self):
        return self.w

    def gradient(self, x, sign):
        return np.sum(x.reshape(-1, 1) * sign)
