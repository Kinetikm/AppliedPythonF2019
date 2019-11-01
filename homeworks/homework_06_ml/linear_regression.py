#!/usr/bin/env python
# coding: utf-8


import numpy as np
from random import shuffle


class LinearRegression:  # Реализация для варианта 1
    def __init__(self, lambda_coef=0.9, regulatization='l1', alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.gamma = lambda_coef
        self.reg = regulatization
        self.alpha = alpha
        self.batch = batch_size
        self.max_iter = max_iter
        self.theta = []

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.y = y_train
        self.init_cost()
        self.n_samples, self.n_features = X_train.shape
        self.theta = np.random.normal(size=(self.n_features + 1), scale=0.5)
        self.X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        A_train = np.zeros((self.X_train.shape[0], self.X_train.shape[1]+1))
        A_train[:, :-2] = X_train[:, :]
        A_train[:, -1] = self.y
        shuffle(self.A_train[:])
        self._gradient_descent()

    def _add_penalty(self, loss, w):
        """Добавляю регуляризацию"""
        loss += self.alpha * np.abs(w[1:]).sum()
        return loss

    def _gradient_descent(self):  # Adadelta
        eps = 10**(-5)
        E_g = np.zeros((X_train.shape[1], 1))
        E_t = np.zeros((X_train.shape[1], 1))
        for i in range(1, self.max_iter + 1):
            batch_X, batch_y = self.get_next_batch(self.X_train, self.y, self.batch, i)
            # Считаем градиент и обновляем тетту
            y_pred = batch_X@self.theta
            gr = self.grad_mse(batch_X, batch_y, y_pred)
            E_g = self.gamma*E_g + (1 - self.gamma)*(gr**2)
            delta = (-1)*((E_t + eps)**0.5)*gr/((E_g + eps)**0.5)
            self.theta += delta
            E_t = self.self.gamma * E_t + (1 - self.gamma)*(delta**2)

    def _cost(self, X, y, theta):
        pred = X.dot(theta)
        error = self.cost_func(y, pred)
        return error

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        return X_test.T * self.get_weights()[1:] + self.get_weights()[0]

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.theta

    def _loss(self, w):
        loss = self.cost_func(self.y, np.dot(self.X, w))
        return self._add_penalty(loss, w)

    def init_cost(self):
        def squared_error(actual, predicted):
            return (actual - predicted) ** 2

        def mean_squared_error(actual, predicted):
            return np.mean(squared_error(actual, predicted))
        self.cost_func = mean_squared_error

    def get_next_batch(self, X, Y, batch, i):
        x = X[(i-1)*batch:batch*i]
        y = Y[(i-1)*batch:batch*i]
        return (x, y)
