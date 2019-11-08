#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, gamma=0.9, lambda_coef=1.0, regularization=None,
                 alpha=0.5, batch_size=50, max_iter=100, random_seed=42):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.gamma = gamma
        self.lambda_coef = lambda_coef
        self.regularization = regularization
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.w = np.array([])
        self.random_seed = random_seed

    def sigmoid(self, X, w):
        return 1 / (1 + np.exp(-np.dot(X, self.w)))

    def sigmoid(self, X, w):
        mul = np.dot(X, self.w).astype(np.float128)
        a = np.exp(-mul)
        return 1.0 / (1.0 + a)

    def gradient(self, X, y):
        X_t = np.transpose(X)
        return (1/X.shape[0]*np.dot(X_t, self.sigmoid(X, self.w) - y) +
                self.alpha*np.sign(self.w) + 2*self.alpha*self.w)

    def batch_generator(self, X, y):
        M = self.batch_size
        if y.shape[0] % M != 0:
            for k in range(y.shape[0] // M):
                yield (X[M*k:M*k + M], y[M*k:M*k + M])
            yield (X[-M:], y[-M:])
        else:
            for k in range(int(y.shape[0] / M)):
                yield (X[M*k:M*k + M], y[M*k:M*k + M])

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        np.random.seed(self.random_seed)
        velocity = 0
        self.w = np.zeros(X_train.shape[1] + 1)
        X_train, y_train = np.hstack((np.ones((X_train.shape[0], 1)), np.array(X_train))), np.array(y_train)
        minibatches = list(self.batch_generator(X_train, y_train))
        indexes = np.arange(len(minibatches))
        np.random.shuffle(indexes)
        for iteration in range(1, self.max_iter + 1):
            for idx in indexes:
                x, y = minibatches[idx][0], minibatches[idx][1]
                grad = self.gradient(x, y)
                velocity = self.gamma*velocity + self.alpha*grad/x.shape[0]  # grad_nag=1/n*grad 
                self.w -= velocity

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        ans = np.array([1 if el > 0.5 else 0 for el in self.sigmoid(np.hstack((np.ones((X_test.shape[0], 1)),
                       np.array(X_test))), self.w)])
        return ans

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        return self.sigmoid(np.hstack((np.ones((X_test.shape[0], 1)), np.array(X_test))), self.w)

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.w
