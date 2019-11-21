#!/usr/bin/env python
# coding: utf-8


import numpy as np
# REGULARIZATION: ELASTICNET
# OPTIMIZATION: ADAM


class LogisticRegression:
    def __init__(self, lambda_coef=0.01, penalty='elasticnet', l1=0.01, l2=0.01, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param penalty: regularizarion type ("L1" or "L2") or elasticnet
        :param l1: L1 regularizarion coefficent
        :param l2: L2 regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        assert penalty == 'elasticnet'

        self.lambda_coef = lambda_coef
        self.l1 = l1
        self.l2 = l2
        self.batch_size = batch_size
        self.max_iter = max_iter
        # adam hyper parameters
        self.beta_1 = 0.9
        self.beta_2 = 0.999
        self.eps = 1e-8

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        y_train = y_train[:, np.newaxis]
        self.K = len(np.unique(y_train))

        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        n_samples, n_features = X_train.shape

        m = np.zeros((n_features, self.K - 1), dtype=np.float128)
        v = np.zeros((n_features, self.K - 1), dtype=np.float128)
        self.w = np.zeros((n_features, self.K - 1), dtype=np.float128)

        for t in range(self.max_iter):
            for batch in self.iterate_minibatches(X_train, y_train):
                x_batch, y_batch = batch
                gradient = self._get_logloss_elasticnet_grad(x_batch, y_batch)
                m = self.beta_1 * m + (1 - self.beta_1) * gradient
                v = self.beta_2 * v + (1 - self.beta_2) * np.power(gradient, 2)

                m_hat = m / (1 - np.power(self.beta_1, t + 1))
                v_hat = v / (1 - np.power(self.beta_2, t + 1))

                old_w = self.w
                self.w = self.w - self.lambda_coef * m_hat / np.sqrt(v_hat + self.eps)

    def softmax(self, x):
        # overflow handle
        x -= np.max(x)
        return (np.exp(x).T / np.sum(np.exp(x), axis=1)).T

    def _get_indikator_array(self, y):
        """
        return: [y[i] == k] matrix of (sample_size, num_of_classes) = (m, self.K)
        Example: y = [0, 1, 2, 1] -> self.K = len([0,1,2]) == 3
                 classes = 0 1 2
                           0 1 2
                           0 1 2
                           0 1 2
                 (classes == y):
                             1 0 0
                             0 1 0
                             0 0 1
                             0 1 0
        """
        m = y.shape[0]
        tmp_cls = np.arange(self.K)
        tmp_one = np.ones((m, 1))
        # (m, K)
        classes = tmp_one * tmp_cls[np.newaxis, :]
        return (classes == y).astype(int)

    def _get_logloss_elasticnet_grad(self, x, y):
        # m == sample size
        m = x.shape[0]
        indikator = self._get_indikator_array(y)
        dy = indikator - self.softmax(x @ self.w)
        grad = - (1 / m) * (x.T @ dy) + 2 * self.l2 * self.w + self.l1 * np.sign(self.w)
        # (n, K)
        return grad

    def iterate_minibatches(self, x, y):
        assert x.shape[0] == y.shape[0]
        indices = np.arange(x.shape[0])
        np.random.shuffle(indices)
        for start_idx in range(0, x.shape[0] - self.batch_size + 1, self.batch_size):
            batch_idx = indices[start_idx:start_idx + self.batch_size]
            yield x[batch_idx], y[batch_idx]

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        n_samples, n_features = X_test.shape
        if n_features != self.w.shape[0]:
            X_test = np.hstack((np.ones((n_samples, 1)), X_test))
        # в каждой строке выбрать максимальную вероятность принадлежности к классу(axis=1)
        return np.max(self.softmax(X_test @ self.w), axis=1)

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        n_samples, n_features = X_test.shape
        if n_features != self.w.shape[0]:
            X_test = np.hstack((np.ones((n_samples, 1)), X_test))
        # (m, k) в каждой строке вероятности принадлежности к классам(колонка)
        return self.softmax(X_test @ self.w)

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return np.array(self.w)
