#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LinearRegression:
    def __init__(self, lambda_coef=1.0, regulatization=None, alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.regularization = regulatization
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.w = None

    def fit(self, X_train, y_train):
        for i in range(self.max_iter):
            
        if self.regularization is None:
            w = (np.linalg.inv((X_train.T @ X_train)) @ X_train.T) @ y_train.reshape((y_train.shape[0], -1))
            self.w = w.flatten()
        elif self.regularization == "Elastic":

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        pass

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        if self.w is not None:
            return self.w
