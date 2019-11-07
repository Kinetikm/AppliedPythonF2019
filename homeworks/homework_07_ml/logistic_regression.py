#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, lambda_coef=1e-5, regularization="elastic_net", beta=0.5, alpha=0.5, batch_size=50,
                 max_iter=1000):
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
        self.beta = beta
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.loss = []
        self.w = 0

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        n = X_train.shape[1]
        y_train = y_train.reshape((-1, 1))
        table = np.hstack((np.ones((X_train.shape[0], 1)), X_train, y_train))
        self.w = np.random.normal(scale=1e-5, size=(1, n+1))
        for iter_ in range(self.max_iter):
            perm = np.random.permutation(table)[:self.batch_size]
            x = perm[:, :-1]
            y = perm[:, -1].reshape(-1, 1)
            grad = self._grad(x, y, self.w)
            self.w += self.lambda_coef * grad/self.batch_size
            err = self.log_loss(x, y, self.w)/self.batch_size
            self.loss.append(err)

    def sigmoid(self, z):
        return 1/(1 + np.exp(-np.clip(z, -250, 250)))

    def _grad(self, x, y, w):
        gr = np.empty_like(w)
        for j in range(w.shape[1]):
            gr[0, j] = np.sum((y.reshape(-1, 1) - self.sigmoid(x.dot(w.T)).reshape(-1, 1))*x[:, j])
            if self.regularization == 'elastic_net':
                gr[0, j] += self.alpha * (1 - self.beta) * w[0, j] + self.alpha * self.beta * np.sign(w[0, j])
        return gr

    def log_loss(self, x, y, w):
        return -np.sum(y*np.log(self.sigmoid(x.dot(w.T))) + (1-y)*np.log(1 - self.sigmoid(x.dot(w.T))))

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        border = 0.5
        y = self.predict_proba(X_test)
        y[y >= border] = 1
        y[y < border] = 0
        return y

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return self.sigmoid(X_test.dot(self.w.T)).squeeze()

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.w

    def get_loss(self):
        return self.loss[1:]


class Multiclass(LogisticRegression):

    def __init__(self, lambda_coef=0.001, beta=0.5, alpha=0.5, batch_size=50, max_iter=1000):
        super().__init__()
        self.w_matrix = 0
        self.lambda_coef = lambda_coef
        self.alpha = alpha
        self.beta = beta
        self.batch_size = batch_size
        self.max_iter = max_iter

    def multi_fit(self, X_train, y_train):
        classes = np.unique(y_train)
        n_classes = len(classes)
        y = y_train
        y = np.eye(n_classes)[y]
        n = X_train.shape[1]
        self.w_matrix = np.random.normal(scale=1e-5, size=(n_classes, n+1))
        for i in range(n_classes):
            self.w = self.w_matrix[i, :]
            self.fit(X_train, y[:, i])
            self.w_matrix[i, :] = self.w

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """

        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        probability = sigmoid(X_test.dot(self.w_matrix.T))
        for i in range(probability.shape[0]):
            probability[i, :] = probability[i, :]/np.sum(probability[i, :])
        return probability

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y = np.empty_like(X_test[:, 0])
        y_prob = self.predict_proba(X_test)
        for i in range(y_prob.shape[0]):
            y[i] = y_prob[i, :].argmax()
        return y

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.w_matrix
