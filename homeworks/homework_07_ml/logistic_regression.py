#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, gamma=0.5, etta=0.9, regulatization='elastic', alpha=0, beta=10, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.gamma = gamma
        self.etta = etta
        self.alpha = alpha
        self.beta = beta
        self.reg = regulatization
        self.batch = batch_size
        self.max_iter = max_iter
        self.theta = []

    def add_penalty(self):
        return self.alpha * np.sign(self.get_weights()) + self.beta * self.get_weights()

    def get_next_batch(self, X, Y):
        index = np.random.choice(self.n_samples, size=self.batch, replace=False)
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
        self.y = y_train.astype(int)
        self.class_num = len(np.unique(self.y))
        self.X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        self.n_samples, self.n_features = self.X_train.shape
        # self.theta = np.zeros((self.n_features, self.class_num))
        self.theta = np.random.rand(self.n_features, self.class_num)
        self._gradient_descent()

    def _gradient_descent(self):
        speed = np.zeros(self.theta.shape)
        for i in range(self.max_iter):
            batch_X, batch_y = self.get_next_batch(self.X_train, self.y)
            # Считаем градиент и обновляем тетту
            gr = self.gradient(batch_X, batch_y)
            speed = self.gamma * speed + self.etta * gr
            self.theta -= speed

    def gradient(self, x, y):
        self.n_samples = x.shape[0]
        p = self.softmax(x @ self.theta)
        p[range(self.n_samples), y] -= 1
        #  gr = x.T @ self.softmax(x @ self.theta)
        return (gr + self.add_penalty()) / self.n_samples

    def softmax(self, z):
        return np.exp(z - np.max(z)) / np.sum(np.exp(z - np.max(z)))

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return self.softmax(X_test @ self.theta()).argmax(axis=1)

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        if X_test.shape[1] != self.theta.shape[0]:
            X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return self.softmax((X_test @ self.theta()))

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.theta
