#!/usr/bin/env python
# coding: utf-8
import numpy as np
from itertools import cycle


class LinearRegression:
    def __init__(self, lambda_coef=1.0, regulatization=None, alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.regularization = regulatization
        self.reg_coef = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.weights = None

    def grad(self, a, x, y):
        def mae_i_j_grad(a_j, x_i_j, y_i):
            if a_j * x_i_j - y_i > 0:
                return x_i_j
            elif a_j * x_i_j - y_i < 0:
                return -x_i_j
            else:
                return 0

        def l1_j_grad(a_j):
            if a_j > 0:
                return 1
            elif a_j < 0:
                return -1
            else:
                return 0

        def l2_j_grad(a_j):
            return 2 * a_j

        l1_coef = 0.9
        l2_coef = 0.1
        mae_i_grad = np.vectorize(mae_i_j_grad)
        l1_grad = np.vectorize(l1_j_grad)
        l2_grad = np.vectorize(l2_j_grad)
        mae_matrix_grad = mae_i_grad(a, x, y)
        mae_grad_vec = np.mean(mae_matrix_grad, axis=0)
        l1_grad_vec = l1_grad(a) * self.reg_coef * l1_coef
        l2_grad_vec = l2_grad(a) * self.reg_coef * l2_coef
        return mae_grad_vec + l1_grad_vec + l2_grad_vec

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        X = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        dim = X.shape[1]
        gamma = 0.9
        eps = 0.00000001
        E_g_2 = np.zeros(dim)
        E_a_2 = np.zeros(dim)
        RMS_a = np.sqrt(E_a_2 + eps)
        RMS_g = np.sqrt(E_g_2 + eps)
        a = np.zeros(dim)
        X = np.array_split(X, self.batch_size)
        Y = np.array_split(y_train, self.batch_size)
        a = a.reshape(1, a.shape[0])
        i = 0
        for batch, res in zip(cycle(X), cycle(Y)):
            g_t = self.grad(a, batch, res.reshape(res.shape[0], 1))
            E_g_2 = gamma * E_g_2 + (1 - gamma) * (g_t ** 2)
            RMS_g = np.sqrt(E_g_2 + eps)
            delta_a = - (RMS_a / RMS_g) * g_t
            a = a + delta_a
            E_a_2 = gamma * E_a_2 + (1 - gamma) * (delta_a ** 2)
            RMS_a = np.sqrt(E_a_2 + eps)
            i += 1
            if i == self.max_iter:
                break
        self.weights = a
        print(self.weights.shape)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        X = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return X @ self.weights.T

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.weights
