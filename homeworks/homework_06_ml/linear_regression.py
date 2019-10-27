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
    @staticmethod
    def grad(a, x, y):
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

        mae_i_grad = np.vectorize(mae_i_j_grad)
        l1_grad = np.vectorize(l1_j_grad)
        l2_grad = np.vectorize(l2_j_grad)
        x = np.hstack((np.ones((x.shape[0], 1)), x))
        a = a.reshape(1, a.shape[0])
        y = y.reshape(y.shape[0], 1)
        mae_matrix_grad = mae_i_grad(a, x, y)
        mae_grad_vec = np.mean(mae_matrix_grad, axis=0)
        l1_grad_vec = l1_grad(a)
        l2_grad_vec = l2_grad(a)
        print(l2_grad_vec)
        return mae_grad_vec + l1_grad_vec + l2_grad_vec

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        dim = X_train.shape[1]
        gamma = 0.9
        l1_coef = 0.9
        l2_coef = 0.1
        E_g_2 = np.zeros(dim)
        eps = 0.00000001
        a = np.zeros(dim)
        X = np.array_split(X_train, self.batch_size)
        for batch in cycle(X):
            g_t = LinearRegression.grad(a, batch, y_train)
            E_g_2 = gamma * E_g_2 + (1 - gamma)


    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        pass

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        pass

a = LinearRegression()
xx = np.array([[1, 3], [6, 9]])
a.grad(np.array([1, 2, -5]), xx, np.array([8, 9]))
