#!/usr/bin/env python
# coding: utf-8


import numpy as np
import math


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
        self.y = y_train
        self.init_cost()
        self.n_samples, self.n_features = X_train.shape
        self.theta = np.random.normal(size=(self.n_features + 1), scale=0.5)
        self.X_train = self._add_intercept(X_train)
        self.theta, self.errors = self._gradient_descent()
        logging.info(" Theta: %s" % self.theta.flatten())

    def _add_penalty(self, loss, w):
        """Добавляю регуляризацию"""
        loss += self.alpha * np.abs(w[1:]).sum()
        return loss

    def _gradient_descent(self):  # Adadelta
        eps = 1
        theta = self.theta
        errors = [self._cost(self.X_train, self.y, theta)]
        E_g = 0
        E_t = 0
        rms_t = math.sqrt(E_g + eps)
        for i in range(1, self.max_iter + 1):
            # Считаем градиент и обновляем тетту
            E_g = self.gamma * E_g + (1 - self.gamma) * (np.linalg.norm(self.cost_func(theta)))
            rms_g = math.sqrt(E_g + eps)
            delta = rms_t * cost_d(theta) / rms_g
            E_t = self.gamma * E_t + (1 - self.gamma) * (np.linalg.norm(delta))
            rms_t = math.sqrt(E_t[i] + eps)
            theta -= delta
            errors.append(self._cost(self.X_train, self.y, theta))
        return theta, errors

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

    def grad_mse(self, X, y):
        grad = np.zeros(len(self.weights))
        grad[0] = np.mean((self.predict(X) - y)**2)
        grad[1:] = np.mean(X*sign[:, None], axis=0)
        return grad

    def stochastic_descent(A, Y, speed=0.1):
        theta = np.array(INITIAL_THETA.copy(), dtype=np.float32)
        previous_cost = 10 ** 6
        current_cost = cost_function(A, Y, theta)
        while np.abs(previous_cost - current_cost) > EPS:
            previous_cost = current_cost
            # --------------------------------------
            # for i in range(len(Y)):
            i = np.random.randint(0, len(Y))
            derivatives = [0] * len(theta)
            for j in range(len(theta)):
                derivatives[j] = (Y[i] - A[i] @ theta) * A[i][j]
            theta[0] += speed * derivatives[0]
            theta[1] += speed * derivatives[1]
            current_cost = cost_function(A, Y, theta)
            print("Stochastic cost:", current_cost)
            plt.plot(theta[0], theta[1], 'ro')
            # --------------------------------------
            current_cost = cost_function(A, Y, theta)
        return theta