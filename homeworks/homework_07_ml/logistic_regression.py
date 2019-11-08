#!/usr/bin/env python
# coding: utf-8


import numpy as np
from sklearn import linear_model
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split


class LogisticRegression:
    def __init__(self, coef=10 ** (-3), lambda_coef1=0.9, lambda_coef2=0.999, regulatization=None, alpha=0.2,
                 n_classes=2, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.coef = coef
        self.B1 = lambda_coef1
        self.B2 = lambda_coef2
        self.alpha = alpha
        self.cl = n_classes
        self.batch = batch_size
        self.iters = max_iter
        self.W = None

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        y_train = y_train.astype(np.int)
        b = np.ones((X_train.shape[0], 1))
        X_train = np.hstack((b, X_train))
        samples = X_train.shape[0]
        feature = X_train.shape[1]
        self.W = np.random.normal(loc=0.0, scale=10 ** (-4), size=(feature, self.cl))
        m = np.zeros((feature, self.cl))
        u = np.zeros((feature, self.cl))
        for i in range(self.iters):
            X = X_train[(i * self.batch) % samples: (i * self.batch) % samples + self.batch]
            y = y_train[(i * self.batch) % samples: (i * self.batch) % samples + self.batch]
            G = X @ self.W
            sm = np.exp(G)
            y_pred = sm / np.sum(sm, axis=1).reshape(-1, 1)
            y_pred[np.arange(self.batch), y] = y_pred[np.arange(self.batch), y] - 1
            grad = X.T @ y_pred + self.alpha * self.W
            m = self.B1 * m + (1 - self.B1) * grad
            u = self.B2 * u + (1 - self.B2) * grad ** 2
            m_go = m / (1 - self.B1 ** (i + 1))
            u_go = u / (1 - self.B2 ** (i + 1))
            self.W = self.W - self.coef * m_go / (u_go + 10 ** (-8)) ** 0.5

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        b = np.ones((X_test.shape[0], 1))
        X_test = np.hstack((b, X_test))
        G = X_test @ self.W
        sm = np.exp(G)
        y_pred = sm / np.sum(sm, axis=1).reshape(-1, 1)
        return y_pred.argmax(axis=1)

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        b = np.ones((X_test.shape[0], 1))
        X_test = np.hstack((b, X_test))
        G = X_test @ self.W
        sm = np.exp(G)
        y_pred = sm / np.sum(sm, axis=1).reshape(-1, 1)
        return y_pred

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.W
