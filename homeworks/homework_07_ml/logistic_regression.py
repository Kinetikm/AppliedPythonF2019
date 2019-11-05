#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, lambda_coef=0.001, regulatization=None, alpha=0.5, batch_size=100, max_iter=100, threshold=0.5):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self._fitted = False
        self.thr = threshold
        self.gamma = 0.1

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        if X_train.shape[0] != y_train.shape[0]:
            raise ValueError
        self._fitted = True
        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        num_measures = X_train.shape[0]
        num_features = X_train.shape[1]
        indices = np.arange(num_measures)
        self.theta = np.zeros(num_features)
        vt = np.zeros_like(self.theta)
        for i in range(self.max_iter):
            np.random.shuffle(indices)
            X_batch = np.take(X_train, indices[:self.batch_size], axis=0)
            y_batch = np.take(y_train, indices[:self.batch_size])
            y_proba = self.predict_proba(X_batch)
            vt = self.gamma * vt + self.lambda_coef * self.grad(X_batch, y_batch)
            self.theta -= vt

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def grad(self, x, y):
        grad = np.empty_like(self.theta)
        num_features = x.shape[1]
        num_measures = x.shape[0]
        grad = (x.T @ (self.predict_proba(x) - y) + 2 * self.alpha * self.theta * np.sign(self.theta)) / num_measures
        return grad

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        if self._fitted is False:
            raise NotFittedError
        if X_test.shape[1] != self.theta.shape[0]:
            X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return (self.predict_proba(X_test) >= self.thr).astype(np.int)

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        if self._fitted is False:
            raise NotFittedError
        if X_test.shape[1] != self.theta.shape[0]:
            X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        y_proba = self._sigmoid(X_test @ self.theta)
        return y_proba

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        if self._fitted is False:
            raise NotFittedError
        return self.theta
