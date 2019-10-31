#!/usr/bin/env python
# coding: utf-8

import numpy as np


class LinearRegression:
    def __init__(self,
                 lambda_coef=50.0,
                 regulatization=None,
                 alpha=0.5, beta=0.5,
                 batch_size=50,
                 max_iter=100,
                 print_log=False):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2" or "elastic") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.regulatization = regulatization
        self.alpha = alpha
        self.beta = beta
        self.batch_size = batch_size
        self.max_iter = max_iter
        self._w = 0
        self.print_log = print_log
        self.loss_train = []

    def linear(self, w, x):
        return x @ w.T

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        # X_train.shape = (n, m)
        # y_train.shape = (n, 1)
        # добавляем фиктивный единичный столбец
        y_train = y_train.reshape(-1, 1)
        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))  # X_train.shape = (n, m + 1)
        self._w = np.random.normal(scale=0.001, size=(1, X_train.shape[1]))  # self._w.shape = (m + 1, 1)
        g = np.zeros_like(self._w)
        eps = 1e-7
        data = np.hstack((X_train, y_train))
        for i in range(self.max_iter):
            n_batches = X_train.shape[0] // self.batch_size  # считаем количество целый батчей в X_train
            data_perm = np.random.permutation(data)  # рандомно мешаем data
            X_train = data_perm[:, :-1]  # X_train.shape = (n, m + 1)
            y_train = data_perm[:, -1].reshape(-1, 1)  # y_train.shape = (n, 1)
            loss = 0
            for idx in range(n_batches):
                sample = X_train[idx * self.batch_size:(idx + 1) * self.batch_size]
                y_true = y_train[idx * self.batch_size:(idx + 1) * self.batch_size]
                y_pred = self.linear(self._w, sample)
                loss += self.mae(y_true, y_pred)
                gradient = self.step(self._w, sample, y_true)
                g += gradient ** 2
                self._w += - self.lambda_coef / self.batch_size * gradient / np.sqrt(g + eps)
            self.loss_train.append(loss / n_batches)
            if (abs(self.loss_train[i-1] - self.loss_train[i]) < 0.001) and i:
                if self.print_log:
                    print(f'Early Stop Training: epoch {i}, loss:{self.loss_train[i]}')
                break
            if self.print_log:
                if i % 100 == 0:
                    print(f'epoch : {i}  loss : {self.loss_train[i]}')

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return self.linear(self._w, X_test)

    @property
    def weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self._w

    def step(self, w, x, y_true):
        gradient = np.zeros_like(w)
        for j in range(x.shape[1]):
            sum_ = 0
            for i in range(x.shape[0]):
                sum_ += x[i, j] * np.sign(x[i, :] @ w.T - y_true[i])
            grad = sum_
            if self.regulatization == 'elastic':
                grad += self.alpha * (1 - self.beta) * w[0, j] + self.alpha * self.beta * np.sign(w[0, j])
            elif self.regulatization == 'L1':
                raise NotImplementedError
            elif self.regulatization == 'L2':
                raise NotImplementedError
            gradient[0, j] = grad
        return gradient

    def mae(self, y_true, y_pred):
        """
        Get mean_absolute_error loss
        :return: loss value
        """
        return (1 / y_true.shape[0]) * sum(abs(y_pred - y_true))
