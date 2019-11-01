#!/usr/bin/env python
# coding: utf-8
import numpy as np


class LinearRegression:
    def __init__(self, lambda_coef=0.9, alpha=0.5, batch_size=50, max_iter=100):
        self.lambda_coef = lambda_coef
        self.alpha = alpha
        self.max_iter = max_iter
        self.batch_size = batch_size
        self.weight = 0

    def fit(self, x_train, y_train):
        """
        Fit model using gradient descent method
        :param x_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.weight = np.random.normal(size=(1, x_train.shape[1] + 1))
        e_g = 0
        e_w = 0
        eps = 1e-8
        lam = self.lambda_coef
        n_grad = 0
        rms_w = 100
        table = np.hstack((np.ones((x_train.shape[0], 1)), x_train, y_train.reshape(-1, 1)))
        n_grad = np.ones(x_train.shape[1] + 1)
        sample = np.arange(x_train.shape[0])
        v_i = np.zeros_like(self.weight)
        for _ in range(self.max_iter):
            np.random.shuffle(sample)
            table_batch = np.take(table, sample[:self.batch_size], axis=0)
            for i in range(table_batch.shape[0]):
                x = table[i:i + 1:, :-1]
                y = table[i:i + 1:, -1::]
                n_grad = np.sign(x.dot(self.weight.T) - y.reshape(-1, 1))
                e_g = lam * e_g + (1 - lam) * (n_grad ** 2)
                rms_g = np.sqrt(e_g + eps)
                delta_w = - (rms_w / rms_g) * n_grad
                e_w = lam * e_w + (1 - lam) * (delta_w ** 2)
                rms_w = np.sqrt(e_w + eps)
                self.weight += delta_w
            loss_mae = sum(abs(table[:, :-1:].dot(self.weight.T) - table[:, -1::])) / table.shape[0]

    def predict(self, x_test):
        x = np.hstack((np.ones((x_test.shape[0], 1)), x_test))
        return x.dot(self.weight.T)

    def get_weights(self):
        return self.weight
