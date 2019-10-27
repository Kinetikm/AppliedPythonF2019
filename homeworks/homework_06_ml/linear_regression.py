#!/usr/bin/env python
# coding: utf-8


import numpy as np
import math


class LinearRegression:  # Реализация для варианта 1
    def __init__(self, lambda_coef=1.0, regulatization=None, alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        regulatization = 'l1'
        self.coef = lambda_coef
        self.reg = regulatization
        self.alpha = alpha
        self.bath = batch_size
        self.max_iter = max_iter
        self.errors = []
        self.theta = []
        self.grad_lst = []

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.init_cost()
        self.n_samples, self.n_features = X_train.shape
        self.theta = np.random.normal(size=(self.n_features + 1), scale=0.5)
        X_train = self._add_intercept(X_train)
        self.theta, self.errors = self._gradient_descent()
        logging.info(" Theta: %s" % self.theta.flatten())

    def _add_penalty(self, loss, w):
        """Добавляю регуляризацию"""
        loss += self.alpha * np.abs(w[1:]).sum()
        return loss

    def _gradient_descent(self):  # Adadelta
        eps = 1
        theta = self.theta
        errors = [self._cost(self.X, self.y, theta)]
        # берем производную от функции потерь
        cost_d = grad(self._loss)
        E_g = [0]
        E_t = [0]  # Немного не понял как нужно высчитывать E[del(theta)]t для нулевого шага
        rms_t = 1  # поэтому просто определил RMS[del(theta)]t как единицу,
        # а нулевой элемент E[del(theta)]t определил как ноль. По идее, в дальнейшем все должно нормально работать
        # ( но это не точно)
        for i in range(1, self.max_iter + 1):
            # Считаем градиент и обновляем тетту
            E_g.append(self.coef * E_g[i - 1] + (1 - self.coef) * (np.linalg.norm(cost_d(theta))))
            rms_g = math.sqrt(E_g[i] + eps)
            delta = rms_t * cost_d(theta) / rms_g
            E_t.append(self.coef * E_t[i-1] + (1 - self.coef) * (np.linalg.norm(delta)))
            rms_t = math.sqrt(E_t[i] + eps)
            theta -= delta
            errors.append(self._cost(self.X, self.y, theta))
        return theta, errors

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        X_test = self._add_intercept(X_test)
        return X_test.dot(self.theta)

    @staticmethod
    def _add_intercept(X):
        b = np.ones([X.shape[0], 1])
        return np.concatenate([b, X], axis=1)

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

    def grad(self, x, y, w):
        gr = np.zeros(w.shape)
        for i in range(w.shape[1]):
            gr[0, i] = sum(x[:, j].reshape(-1, 1)*np.sign(x.dot(w.T) - y)) + self.coef*(np.sign(w[0, j]))
        return gr
