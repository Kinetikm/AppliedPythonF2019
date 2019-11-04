#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, c=1, gamma=0.8, etta=0.6, regulatization='elastic', alpha=0.3, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.c = c
        self.gamma = gamma
        self.etta = etta
        self.alpha = alpha
        self.reg = regulatization
        self.batch = batch_size
        self.max_iter = max_iter
        self.theta = []

    def add_penalty(self):
        return self.alpha * np.sign(self.get_weights()) + 0.6 * self.get_weights()

    def get_next_batch(self, X, Y, batch):
        index = np.random.choice(self.n_samples, batch, replace=False)
        x_batch = X[index]
        y_batch = Y[index]
        return x_batch, y_batch

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.y = y_train
        self.X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        self.n_samples, self.n_features = self.X_train.shape
        self.theta = np.random.rand(self.n_features, 1)
        if self.c > 1:  # Здесь должна быть реализация softmax'a
            pass
        else:
            self.binary_gradient_descent()

    def binary_gradient_descent(self):
        speed_l = 0
        for i in range(self.max_iter):
            batch_X, batch_y = self.get_next_batch(self.X_train, self.y, self.batch)
            # Считаем градиент и обновляем тетту
            gr = self.gradient(self.theta, batch_X.T, batch_y)
            gr += self.add_penalty()
            speed_n = self.gamma * speed_l + self.etta * gr
            self.theta -= speed_n
            speed_l = speed_n

    @staticmethod
    def sigmoid(z):
        return 1 / (1 + np.exp(z))

    def gradient(self, w, X, Y):
        z = np.dot(w.T, X)
        A = self.sigmoid(z)
        grad = 1 / X.shape[1] * np.dot(X, (A - Y).T)
        return grad

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        y_test = np.squeeze(0.5 * (np.tanh(0.5 * X_test.dot(self.theta)) + 1))  # аналог сигмоиды
        for i in range(y_test.shape[0]):
            if y_test[i] > 0.5:
                y_test[i] = 1
            else:
                y_test[i] = 0
        return y_test

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return 1 - 1/(1 + np.exp(X_test.dot(self.theta)))

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.theta
