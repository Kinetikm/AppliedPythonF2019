#!/usr/bin/env python
# coding: utf-8
import numpy as np

# Для подбора моделей перебором гиперпараметров можно использовать GridSearchCV, RandomizedSearchCV


class LinearRegression:
    def __init__(self, lambda_coef=10, eps=0.1, alpha=0.1, batch_size=50, max_iter=1000):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param eps: smoothing parameter(ADAGRAD)
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.eps = eps

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        y_train = y_train[:, np.newaxis]
        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))

        n_samples, n_features = X_train.shape

        g_t = np.zeros((n_features, 1))
        self.w = np.zeros((n_features, 1))

        for i in range(self.max_iter):
            for batch in self.iterate_minibatches(X_train, y_train):
                x_batch, y_batch = batch
                gradient = self._get_mse_grad(x_batch, y_batch)
                g_t += gradient ** 2
                self.w -= self.lambda_coef * gradient / np.sqrt(g_t + self.eps)

    def iterate_minibatches(self, x, y):
        assert x.shape[0] == y.shape[0]
        indices = np.arange(x.shape[0])
        np.random.shuffle(indices)
        for start_idx in range(0, x.shape[0] - self.batch_size + 1, self.batch_size):
            batch_idx = indices[start_idx:start_idx + self.batch_size]
            yield x[batch_idx], y[batch_idx]

    def _get_mse_grad(self, x, y):
        return 2 * (x.T @ (x @ self.w - y) + self.alpha * self.w)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        n_samples, n_features = X_test.shape
        if n_features != self.w.shape[0]:
            X_test = np.hstack((np.ones((n_samples, 1)), X_test))
        return X_test @ self.w

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.w
