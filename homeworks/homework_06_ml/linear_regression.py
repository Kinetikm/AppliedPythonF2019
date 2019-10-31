#!/usr/bin/env python
# coding: utf-8
import numpy as np
from sklearn import preprocessing


class LinearRegression:
    def __init__(self, lambda_coef=50.0, regularization=None, alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.regularization = regularization
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.weights = np.array([0])
        self.costs = []

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        X_train = self.normalization(X_train)
        y_train = y_train.reshape((-1, 1))
        data = np.hstack(np.ones((X_train.shape[0], 1)), X_train, y_train)
        grad_new = np.zeros_like(self.weights)
        self.weights = np.random.normal(scale=1e-8, size=(1, X_train.shape[1]))
        eps = 1e-8
        for _ in range(self.max_iter):
            validated_mat = np.random.permutation(data)[:self.batch_size]
            x = validated_mat[:, :-1]
            y = validated_mat[:, -1].reshape(-1, 1)
            grad = self.gradient(x, y)
            grad_new += grad ** 2
            self.weights -= self.lambda_coef * grad / np.sqrt(grad_new + eps) / self.batch_size
            flaw = self.MAE(x, y)
            self.costs.append(flaw)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        if X_test.shape[0] == 1:
            X_test = np.reshape(X_test, (-1, 1))
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        y_test = np.dot(X_test, self.weights.T)
        return y_test

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.weights

# Нормализация матрицы
    def normalization(self, mat_of_features):
        mat_scaled = preprocessing.scale(mat_of_features)
        return mat_scaled

    def MAE(self, x, y):
        if x.shape[0] == 1:
            x = np.reshape(x, (-1, 1))
        a_x = np.dot(x, self.weights.T)
        difference = abs(y - a_x) / self.batch_size
        return difference.sum()

    def gradient(self, x, y):
        grad = np.zeros_like(self.weights)
        for i in range(self.weights.shape[1]):
            l1 = self.alpha*(np.sign(self.weights[0][i]))
            grad[0, i] = sum(x[:, i].reshape(-1, 1)*np.sign(x.dot(self.weights.T) - y)) + l1
        return grad
