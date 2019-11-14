#!/usr/bin/env python
# coding: utf-8


import numpy as np

'''
var 13
regularization: elastic
optim: adagrad
loss: log loss

'''


class LogisticRegression:
    def __init__(self, lambda_coef=1.0, regulatization=None, alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self._lambda = lambda_coef
        self._alpha = alpha
        self._batch_size = batch_size
        self._max_iter = max_iter
        self._beta = alpha
        self._eps = 1e-7
        self._threshold = 0.5
        self._weights = None

    def grad(self, x, y):
        # grad = np.empty_like(self._weights)

        grad = x.T @ (self.predict_proba(x) - y) + self._alpha * np.sign(self._weights)
        grad += 2 * self._beta * self._weights * np.sign(self._weights)
        grad /= x.shape[0]
        return grad

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        G = 0
        self._weights = np.random.rand(X_train.shape[1])
        for j in range(self._max_iter):
            for x_batch, y_batch in self.__batches(X_train, y_train):
                gt = self.grad(x_batch, y_batch)
                G += gt ** 2
                self._weights -= self._lambda / np.sqrt(G + self._eps) * gt

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        return (self.predict_proba(X_test) >= self._threshold).astype(np.int)

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        if X_test.shape[1] != self._weights.shape[0]:
            X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return self.sigmoid(X_test @ self._weights)

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self._weights

    def __batches(self, x, y, n=[]):
        if not n:
            n.append(0)
        beg = self._batch_size * (n[0] - 1) % x.shape[0]
        end = self._batch_size * n[0] % x.shape[0]
        n[0] += 1
        yield (x[beg:end], y[beg:end])

    @staticmethod
    def sigmoid(z):
        return 1 / (1 + np.exp(-z))


class SoftmaxLogisticRegression(LogisticRegression):

    @staticmethod
    def softmax(x):
        e = np.exp(x - np.max(x))
        return e / np.sum(e)

    def __init__(self, n):
        super().__init__()
        self._n_cls = n
        self._weights = [[] for _ in range(n)]

    def fit(self, x_train, y_train):
        x_train = np.hstack((np.ones((x_train.shape[0], 1)), x_train))
        for i in range(n):
            G = 0
            self._weights[i] = np.random.rand(x_train.shape[1] + 1)
            for j in range(self._max_iter):
                for x_batch, y_batch in self.__batches(x_train, y_train[:, j]):
                    gt = self.grad(x_batch, y_batch)
                    G += gt ** 2
                    self._weights[i] -= self._lambda_coef / np.sqrt(G + self._eps) * gt


    def predict_proba(self, X_test):
        pr = super().predict_proba(X_test)
        return softmax(pr)


# import numpy as np
from sklearn import linear_model
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split

size = 5000
n_feat = 20

np.random.seed(0)

C1 = np.random.randn(n_feat, n_feat) * 5
C2 = np.random.randn(n_feat, n_feat) * 5
gauss1 = np.dot(np.random.randn(size, n_feat) + np.random.randn(n_feat) * 0.3, C1)
gauss2 = np.dot(np.random.randn(size, n_feat) + np.random.randn(n_feat) * 0.3, C2)

x = np.vstack([gauss1, gauss2])
y = np.r_[np.ones(size), np.zeros(size)]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

lr1 = linear_model.LogisticRegression()
lr2 = LogisticRegression(batch_size=500, max_iter=1000)

lr1.fit(x_train, y_train)
lr2.fit(x_train, y_train)

# check predict works

loss1 = log_loss(y_test, lr1.predict_proba(x_test))
loss2 = log_loss(y_test, lr2.predict_proba(x_test))



