#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, lambda_coef=0.001, regulatization=None, alpha=29, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """

        # Regularization: l2, Optim: SGD
        self.lambda_coef = lambda_coef
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter

        np.random.seed(1707)

    def get_next_batch(self, X, Y, batch_size):
        index = np.random.choice(X.shape[0], batch_size, replace=False)
        x_batch = X[index]
        y_batch = Y[index]
        return x_batch, y_batch

    def stable_softmax(self, v):
        exps = np.exp(v - np.max(v))
        return exps / np.sum(exps)

    def grad(self, X, Y):
        m = Y.shape[0]
        p = self.stable_softmax(X @ self.theta)
        p[range(m), Y] -= 1

        gt = (1 / m) * X.T @ p + 2 * self.alpha * self.theta  # l2 регуляризация

        return gt

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        y_train = y_train.astype(int)
        cnum = len(np.unique(y_train))  # количество классов
        self.theta = np.random.rand(X_train.shape[1], cnum)

        conv = 10e-10  # точность, до которой хочется, чтобы алгоритм сходился
        for _ in range(self.max_iter):
            x_batch, y_batch = self.get_next_batch(X_train, y_train, self.batch_size)
            dtheta = self.lambda_coef * self.grad(x_batch, y_batch)

            # сравниваем наибольшее изменение компоненты весов весов, если оно очень небольшое,
            # то алгоритм сошелся до прохождения максимального количества итераций
            if np.max(dtheta) < conv:
                break

            self.theta = self.theta - dtheta

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return self.stable_softmax(X_test @ self.theta).argmax(axis=1)

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return self.stable_softmax(X_test @ self.theta)

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.theta
