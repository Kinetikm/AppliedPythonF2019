#!/usr/bin/env python
# coding: utf-8


import numpy as np
from sklearn.utils import gen_batches


class LinearRegression:

    def __init__(self, lambda_coef=1.0, regulatization=None, alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.batch_size = batch_size
        self.max_iter = max_iter

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        N = len(y_train)
        self.weigths = np.random.rand(X_train.shape[1] + 1)
        X_train = np.append(np.ones(N).reshape(1, -1).T, X_train, axis=1)
        coef = 0.9

        old_dw, eps = 0, 0.001

        E_g, E_q = 0, 0
        # old_dw, E_q, E_g вначале не векторы (для удобства), но потом ими становятся, так что не баг а фича :)

        # так как точность измерений не указана, условием окончания является только число итераций
        for _ in range(self.max_iter):
            for batch in gen_batches(N, self.batch_size):
                X = X_train[batch]
                y = y_train[batch]
                g = self.gradient(X, y)

                E_g = coef * E_g + (1 - coef) * g ** 2
                E_q = coef * E_q + (1 - coef) * old_dw ** 2

                dw = np.sqrt(eps + E_q) / np.sqrt(eps + E_g)

                self.weigths -= dw * g

                old_dw = dw

    def gradient(self, X, y):
        coef1, coef2 = 0.1, 0.1
        alpha = coef1 + coef2
        l1_ratio = coef1 / (coef1 + coef2)

        l1_grad = alpha * l1_ratio * coef1 * np.abs(self.weigths)
        l2_grad = alpha * (1 - l1_ratio) * coef2 * self.weigths ** 2
        return X.T @ (X @ self.weigths - y) * 2 / len(self.weigths) + l1_grad + l2_grad

    def predict(self, X_test):
        return np.append(np.ones(X_test.shape[0]).reshape(1, -1).T, X_test, axis=1) @ self.weigths

    def get_weights(self):
        return self.weigths
