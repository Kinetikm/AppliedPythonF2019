#!/usr/bin/env python
# coding: utf-8


import numpy as np


'''
var 13
regularization: elastic
optim: adagrad

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
        self._weights = []

        raise NotImplementedError

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        pass

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        pass

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        pass

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self._weights
