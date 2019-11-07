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
        self._weights = [[]]
        self._classnum = 1

        raise NotImplementedError

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        '''
        implement softmax
        if y_train.shape[1] > 1:
            *softmax*


        '''
        self._classnum = y.shape[1]
        self._weights = [_ for _ in range(self._classnum)]
        beta_1 = 0.9
        beta_2 = 0.9

        for i in range(self._classnum):
            self._weights[i] = np.random.rand(X_train.shape[1])
            m = 0
            v = 0
            for j in range(self._max_iter):
                for x_batch, y_batch in self.__batches(X_train, y_train[:,j]):
                    g = self.__grad()

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        return [X_test @ self._weights[i].T for i in range(self._classnum)]

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

    def __batches(self, x, y, n=[]):
        if not n:
            n.append(0)
        beg = self._batch_size * (n[0] - 1) % x.shape[0]
        end = self._batch_size * n[0] % x.shape[0]
        n[0] += 1
        yield (x[beg:end], y[beg:end])