#!/usr/bin/env python
# coding: utf-8


import numpy as np
import copy


class LogisticRegression:
    def __init__(self, lambda_coef=1, regulatization='L2', alpha=0.5, batch_size=50, max_iter=1000):
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
        self.regulatization = regulatization

    def fit(self, X_train, y_train, eps=1e-8, tol=1e-4):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        # method='ADAGRAD'

        y_train = self._encode_labels(y_train)
        self.n_labels = y_train.shape[1]
        self.w = np.zeros((X_train.shape[1] + 1, self.n_labels))

        X_tr_y_tr = copy.deepcopy(X_train)
        X_tr_y_tr = np.hstack((np.ones((X_tr_y_tr.shape[0], 1)), X_tr_y_tr))
        X_tr_y_tr = np.hstack((X_tr_y_tr, y_train))

        G_t = np.zeros(self.w.shape)
        w_prev = np.zeros(self.w.shape)

        k = X_train.shape[0] // self.batch_size
        for i in range(self.max_iter):
            set_of_batch = self._split_into_batch(X_tr_y_tr)
            for j in range(k):
                x = set_of_batch[j][:, :-self.n_labels]
                y = set_of_batch[j][:, x.shape[1]:x.shape[1] + self.n_labels]
                gt = self._gradient(x, y)
                G_t += gt * gt
                self.w -= self.alpha * gt / (eps + np.sqrt(G_t))

            if i != 0 and self._dist(self.w, w_prev, tol) is True:
                return None
            w_prev = copy.deepcopy(self.w)

    def _dist(self, v1, v2, tol):
        if v1.shape == 1:
            result = []
            for i in range(len(v1)):
                result.append((v1[i] - v2[i]) ** 2)
            r = sum(result)
            return r < tol
        else:
            result = np.zeros(v1.shape[0])
            for i in range(v1.shape[0]):
                x = 0
                for j in range(len(v1[0])):
                    x += ((v1[i, j] - v2[i, j]) ** 2)
                result[i] = x
            return result.all() < tol

    def _split_into_batch(self, x_y):
        x_y = np.random.permutation(x_y)
        k = x_y.shape[0] // self.batch_size
        result = []
        for i in range(k):
            result.append(x_y[i * self.batch_size:(i + 1) * self.batch_size])
        return result

    def _check_type(self, x):
        # проверка на то, что пользователь загрузил выборки типа list или np.darray
        if isinstance(x, np.ndarray):
            return x
        elif isinstance(x, list):
            return np.array(x)
        else:
            raise TypeError

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        return self.predict_proba(X_test).argmax(axis=1)

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        if X_test.shape[1] != self.w.shape[0]:
            X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))

        return self._softmax(X_test @ self.w)

    def _softmax(self, x):
        return (np.exp(x).T / np.sum(np.exp(x), axis=1)).T

    def _gradient(self, x, y):
        return (x.T @ (self.predict_proba(x) - y)) / x.shape[0] + 2 * self.alpha * self.w

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.w

    def _encode_labels(self, y):
        return (np.arange(np.max(y) + 1) == y[:, None]).astype(float)
