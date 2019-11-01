#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import copy


def normalize(x):
    m = x.mean(axis=1)
    sigma = np.std(x, axis=1)
    for row in range(x.shape[0]):
        if sigma[row] > 0:
            x[row, :] = (x[row, :] - m[row]) / sigma[row]


class LinearRegression:
    def __init__(self, lambda_coef=1.0, regulatization=None, alpha=0.5, batch_size=50, max_iter=100):
        """
        Loss: MSE, Regularization: elastic, Optim: Adam
        :param lambda_coef: constant coef for gradient descent step
        :param alpha: regularizarion coefficent for l1
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.weights = np.array([])

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        np.random.seed(42)
        if isinstance(X_train, np.ndarray) and isinstance(y_train, np.ndarray):
            if len(y_train.shape) == 1 and len(X_train.shape) == 2:
                X_copy = copy.deepcopy(X_train)
                normalize(X_copy)
                X_copy = np.insert(X_copy, 0, 1, axis=1)
                y_copy = np.array([copy.deepcopy(y_train)])
                self.weights = np.random.rand(1, X_copy.shape[1])
                number_of_samples = min(X_copy.shape[0], self.batch_size)
                b_1 = 0.9
                b_2 = 0.999
                e = 1e-8
                m = np.zeros((1, X_copy.shape[1]))
                v = np.zeros((1, X_copy.shape[1]))
                for i in range(self.max_iter):
                    samples = np.random.choice(X_copy.shape[0], size=number_of_samples, replace=False)
                    data = X_copy[samples, :]
                    answers = y_copy[:, samples]
                    grad = self.gradient(data, number_of_samples, answers)
                    m = b_1 * m + (1 - b_1) * grad
                    v = b_2 * v + (1 - b_2) * grad * grad
                    m_cap = m / (1 - (b_1 ** (i + 1)))
                    v_cap = v / (1 - (b_2 ** (i + 1)))
                    delta_weight = (self.lambda_coef * m_cap) / (np.sqrt(v_cap) + e)
                    self.weights = self.weights - delta_weight
                    if sum(delta_weight @ delta_weight.T) < 0.000001:
                        break
                Loss = (1 / X_copy.shape[0]) * sum(sum(abs((X_copy @ self.weights.T) - y_copy.T)) - sum(
                    self.weights ** 2) - sum(np.fabs(self.weights)))
            else:
                raise ValueError
        else:
            raise TypeError

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        return np.insert(X_test, 0, 1, axis=1) @ self.weights.T

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.weights

    def gradient(self, x, l, y):
        grad = (2 / l) * (x.T @ ((x @ self.weights.T) - y.T)).T
        return grad + 2 * self.alpha * self.weights + (1 - self.alpha) * np.sign(self.weights)
