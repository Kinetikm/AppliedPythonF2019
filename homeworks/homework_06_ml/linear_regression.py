#!/usr/bin/env python
# coding: utf-8

import numpy as np


class LinearRegression:
    def __init__(self, lambda_coef=0.6, regulatization="L1", alpha=0.06, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self._lr = lambda_coef
        if regulatization == "L2":
            raise NotImplementedError
        else:
            self._regularization = regulatization
        self._alpha = alpha
        self._batch_size = batch_size
        self._max_iter = max_iter
        self._weights = []

    def __grad_MAE(self, w, x, y):
        f = y - x @ w.T
        if len(y) == 1:
            regs = np.zeros(len(x))
            if self._regularization:
                regs = np.array([self._alpha if w[i] > 0 else regs[i] for i in range(len(regs))])
                regs = np.array([-1 * self._alpha if w[i] < 0 else regs[i] for i in range(len(regs))])
            if f > 0:
                return np.array(-x) + regs
            elif f < 0:
                return np.array(x) + regs
            else:
                return np.zeros(len(x)) + regs
        else:
            regs = np.zeros(len(x[0]))
            if self._regularization:
                regs = np.array([self._alpha if w[i] > 0 else regs[i] for i in range(len(regs))])
                regs = np.array([-1 * self._alpha if w[i] < 0 else regs[i] for i in range(len(regs))])
            ret_lst = [np.array(x[i]) + regs if f[i] < 0 else np.array(-x[i]) + regs for i in range(len(f))]
            ret_lst = [ret_lst[i] if f[i] != 0 else np.zeros(len(x[i])) + regs for i in range(len(f))]
            return np.array(ret_lst)

    @staticmethod
    def __batch(iterable, n=1):
        current_batch = []
        for item in iterable:
            current_batch.append(item)
            if len(current_batch) == n:
                yield current_batch
                current_batch = []
        if current_batch:
            yield current_batch

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        np.random.seed(13)
        x_t, x_v = X_train[:int(0.8 * len(X_train))], X_train[int(0.8 * len(X_train)):]
        y_t, y_v = y_train[:int(0.8 * len(y_train))], y_train[int(0.8 * len(y_train)):]
        self._weights = np.random.normal(scale=0.1, size=X_train.shape[1])
        gti = np.zeros(X_train.shape[1])
        theta = np.array(self._weights.copy(), dtype=np.float32)
        for epoch in range(self._max_iter):
            loss = 0
            for batch, ybatch in zip(self.__batch(x_t, self._batch_size), self.__batch(y_t, self._batch_size)):
                grad = self.__grad_MAE(theta, np.array(batch), np.array(ybatch))
                grad = sum(grad) / self._batch_size
                gti += grad ** 2
                theta -= self._lr * grad / np.sqrt(gti + 1e-7)
                loss += abs(sum(np.array(ybatch) - np.array(batch) @ theta.T)) / self._batch_size
            sh_nums = np.arange(len(y_t))
            np.random.shuffle(sh_nums)
            sh_x_t = np.array([x_t[i] for i in sh_nums])
            x_t = sh_x_t
            sh_y_t = np.array([y_t[i] for i in sh_nums])
            y_t = sh_y_t
        self._weights = theta.copy()

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        return X_test @ self._weights.T

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self._weights
