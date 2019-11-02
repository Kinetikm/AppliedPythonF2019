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
        self.n_samples, self.n_features = X_train.shape
        self.theta = np.random.sample((self.n_features+1, 1))
        self.X_train = np.hstack((np.ones((self.n_samples, 1)), X_train))
        self._gradient_descent()

    def _gradient_descent(self):  # Adadelta
        eps = 10**(-5)
        E_g = np.zeros((self.n_features + 1, 1))
        E_t = np.zeros((self.n_features + 1, 1))
        for i in range(self.max_iter):
            batch_X, batch_y = self.get_next_batch(self.X_train, self.y, self.batch)
            batch_y.reshape(-1, 1)
            y_pred = batch_X@self.theta
            print(y_pred.shape)
            # Считаем градиент и обновляем тетту
            gr = batch_X.T@(y_pred - batch_y)
            gr += self.add_penalty()
            print(batch_y.shape)
            print((y_pred - batch_y).shape)
            print(gr.shape)
            E_g = self.gamma*E_g + (1 - self.gamma)*(gr**2)
            delta = (-1)*((E_t + eps)**0.5)*gr/((E_g + eps)**0.5)
            self.theta += delta
            E_t = self.self.gamma * E_t + (1 - self.gamma)*(delta**2)

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

    def get_next_batch(self, X, Y, batch):
        index = np.random.choice(self.n_samples, batch, replace=False)
        x_batch = X[index]
        y_batch = Y[index]
        return x_batch, y_batch

    def add_penalty(self):
        return self.alpha*np.linalg.norm(self.theta)
