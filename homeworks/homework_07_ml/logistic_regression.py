#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, etta=0.001, lam_coef=2, lr1=0.01, lr2=0.01, regularization='elastic', eps_in_adam=1e-9,
                 batch_size=50, max_iter=1000):
        self.etta = etta
        self.lr1 = lr1
        self.lr2 = lr2
        self.lam_coef = lam_coef
        self.eps_in_adam = eps_in_adam
        self.regularization = regularization
        self.max_iter = max_iter
        self.batch_size = batch_size
        self.w = 0

    def fit(self, x_train, y_train):
        row, col = x_train.shape[0], x_train.shape[1]
        x_train = np.hstack([np.ones((row, 1)), x_train])
        x = np.array_split(x_train, self.batch_size)
        y = np.array_split(y_train, self.batch_size)
        list_of_index = list(range(len(x)))
        np.random.shuffle(list_of_index)
        self.w = np.random.randn(col + 1)
        beta1_in_adam, beta2_in_adam = 0.9, 0.999
        mt, vt = 0, 0
        t = 0
        for itr in range(self.max_iter):
            for i in list_of_index:
                t += 1
                gradient = self.get_l_gradient(x[i], y[i]) / x[i].shape[0]
                mt = beta1_in_adam * mt + (1 - beta1_in_adam) * gradient
                vt = beta2_in_adam * vt + (1 - beta2_in_adam) * gradient * gradient
                self.w -= self.etta / (np.sqrt(vt / (1 - beta2_in_adam ** t) + self.eps_in_adam)) * \
                          mt / (1 - beta1_in_adam ** t)

    def get_l_gradient(self, x, y):
        if self.regularization == 'elastic':
            return x.T @ (self.sigmoid(x) - y) / len(x) + self.lam_coef * self.lr2 * self.w + self.lr1 * np.sign(self.w)
        else:
            raise NotImplementedError

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z @ self.w))

    def predict(self, x_test):
        x_test = np.hstack((np.ones((x_test.shape[0], 1)), x_test))
        pred = np.sign(self.sigmoid(x_test))
        pred[pred == -1] = 0
        return pred

    def predict_proba(self, x_test):
        x_test = np.hstack((np.ones((x_test.shape[0], 1)), x_test))
        return self.sigmoid(x_test)

    @property
    def get_weights(self):
        return self.w
