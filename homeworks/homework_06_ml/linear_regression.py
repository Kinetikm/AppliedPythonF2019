#!/usr/bin/env python
# coding: utf-8

import numpy as np


class LinearRegression:
    def __init__(self, lambda_coef=0.9, regulatization="L1", alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.regul = regulatization
        self.alpha = alpha
        self.bs = batch_size
        self.iters = max_iter
        self.w = None

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        # MSE, Adadelta, L1
        epsilon = 10 ** (-6)
        b = np.ones((X_train.shape[0], 1))
        X_train = np.hstack((b, X_train))
        y_train = y_train.reshape((y_train.shape[0], 1))
        self.w = np.random.rand(X_train.shape[1], 1)
        E_Loss = np.zeros((X_train.shape[1], 1))
        E_w = np.zeros((X_train.shape[1], 1))
        for i in range(self.iters):
            batch_X = X_train[i * self.bs % X_train.shape[0]:i * self.bs % X_train.shape[0] + self.bs]
            batch_y = y_train[i * self.bs % y_train.shape[0]:i * self.bs % y_train.shape[0] + self.bs]
            pred = batch_X@self.w
            grad = batch_X.T@(pred - batch_y) + self.alpha*np.sign(self.w)
            E_Loss = self.lambda_coef*E_Loss + (1 - self.lambda_coef)*(grad**2)
            del_w = (-1)*((E_w + epsilon)**0.5)*grad/((E_Loss+epsilon)**0.5)
            self.w += del_w
            E_w = self.lambda_coef*E_w + (1 - self.lambda_coef)*(del_w**2)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        b = np.ones((X_test.shape[0], 1))
        X_test = np.hstack((b, X_test))
        return X_test@self.w

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.w
