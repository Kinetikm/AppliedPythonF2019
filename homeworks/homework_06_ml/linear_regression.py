#!/usr/bin/env python
# coding: utf-8
import numpy as np


class LinearRegression:
    """
    Основные идеи честно взяты отсюда https://wiseodd.github.io/techblog/2016/06/22/nn-optimization/
    """
    def __init__(self, lambda_coef=1.0, regularization=None, alpha=0.5, batch_size=50, max_iter=100, random_seed=42,
                 beta1=0.9, beta2=0.999, eps=1e-8):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.eps = eps
        self.beta2 = beta2
        self.beta1 = beta1
        self.lambda_coef = lambda_coef
        self.regularization = regularization
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.w = np.array([])
        self.random_seed = random_seed

    def gradient(self, X, y):
        X_t = np.transpose(X)
        return 2 * np.dot(X_t, np.dot(X, self.w) - y) + self.alpha*np.sign(self.w)

    def batch_generator(self, X, y):
        M = self.batch_size
        if y.shape[0] % M != 0:
            for k in range(y.shape[0] // M):
                yield (X[M*k:M*k + M], y[M*k:M*k + M])
            yield (X[-M:], y[-M:])
        else:
            for k in range(y.shape[0] / M):
                yield (X[M*k:M*k + M], y[M*k:M*k + M])

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        np.random.seed(self.random_seed)
        m, r = 0, 0
        self.w = np.zeros(X_train.shape[1]+1)
        X_train, y_train = np.hstack((np.ones((X_train.shape[0], 1)), np.array(X_train))), np.array(y_train)
        minibatches = list(self.batch_generator(X_train, y_train))
        indexes = np.arange(len(minibatches))
        np.random.shuffle(indexes)
        for iteration in range(1, self.max_iter + 1):
            for idx in indexes:
                x, y = minibatches[idx][0], minibatches[idx][1]
                grad = self.gradient(x, y)
                m = self.beta1 * m + (1 - self.beta1) * grad
                r = self.beta2 * r + (1 - self.beta2) * grad ** 2
                m_hat = m / (1 - self.beta1 ** iteration)
                r_hat = r / (1 - self.beta1 ** iteration)
                self.w -= self.lambda_coef * m_hat/(np.sqrt(r_hat) + self.eps)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        return np.dot(np.array(X_test), self.w[:][1:])

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.w[:][1:]
