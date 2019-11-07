#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, lambda_coef=1.0, alpha=0.5, batch_size=50, max_iter=100, gamma = 0.2, threshold = 0.5):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        :param gamma: parameter for NAG
        :param threshold: probability threshold to determine class 1
        """
        self.lr = lambda_coef
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.gamma = gamma
        self.threshold = threshold
        self.weights = None

    def sigmoid(self, w, x):
        print(w)
        return 1 / (1 + np.exp(-(x @ w.T)))

    def grad(self, w, x, y):
        logloss_grad = (self.sigmoid(w, x) - y) * x
        reg_grad = np.sum(2 * self.weights)
        return np.mean(logloss_grad + self.alpha * reg_grad)

    @staticmethod
    def shuffle(a, b):
        rnd_state = np.random.get_state()
        np.random.shuffle(a)
        np.random.set_state(rnd_state)
        np.random.shuffle(b)


    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        np.random.seed(1234)
        X = (X_train - np.mean(X_train)) / np.std(X_train)
        X = np.hstack((np.ones((X.shape[0], 1)), X))
        dim = X.shape[1]
        a = np.array
        print(a)
        X = np.array_split(X, self.batch_size)
        Y = np.array_split(y_train, self.batch_size)
        a = a.reshape(1, a.shape[0])
        print(a)
        i = 0
        v = 0
        while i < self.max_iter:
            LogisticRegression.shuffle(X, Y)
            for batch, res in zip(X, Y):
                print(a)
                v = self.gamma * v + self.lr * self.grad(a - self.gamma * v, batch, res)
                a = a - v
            i += 1
        self.weights = a

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        pred_val = lambda x: 1 if x >= self.threshold else 0
        predict_classes = np.vectorize(pred_val)
        return pred_val(self.predict(X_test))

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        X = (X_test - np.mean(X_test)) / np.std(X_test)
        X = np.hstack((np.ones((X_test.shape[0], 1)), X))
        return X @ self.weights.T

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.weights


print(np.array([np.random.normal(0, 10)] * 5))