#!/usr/bin/env python
# coding: utf-8
import numpy as np
from matplotlib import pyplot as plt


class LinearRegression:
    def __init__(self, l1_reg_coef=0.1, l2_reg_coef=0.9, gamma=0.7, alpha=0.5,
                 batch_size=50, max_iter=100):
        """
        :param l1_reg_coef: constant coef for l1 regularization
        :param l2_reg_coef: constant coef for l2 regularization
        :param gamma: parameter for adadelta
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.l1_reg_coef = l1_reg_coef
        self.l2_reg_coef = l2_reg_coef
        self.reg_coef = alpha
        self.gamma = gamma
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.weights = None
        self.loss_res = None

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

        mae_i_grad = np.vectorize(mae_i_j_grad)
        l1_grad = np.vectorize(l1_j_grad)
        l2_grad = np.vectorize(l2_j_grad)
        mae_matrix_grad = mae_i_grad(a, x, y)
        mae_grad_vec = np.mean(mae_matrix_grad, axis=0)
        l1_grad_vec = l1_grad(a) * self.reg_coef * self.l1_reg_coef
        l2_grad_vec = l2_grad(a) * self.reg_coef * self.l2_reg_coef
        return mae_grad_vec + l1_grad_vec + l2_grad_vec

    def print_plot(self):
        fig_size = plt.rcParams["figure.figsize"]
        fig_size[0] = 100
        fig_size[1] = 20
        plt.rcParams["figure.figsize"] = fig_size
        plt.plot([x for x in range(len(self.loss_res))], self.loss_res)
        plt.savefig("/home/nemo/loss.png")

    @staticmethod
    def shuffle(a, b):
        rnd_state = np.random.get_state()
        np.random.shuffle(a)
        np.random.set_state(rnd_state)
        np.random.shuffle(b)

    def loss(self, a, X, Y):
        return np.mean(np.abs(X @ a.T - Y)) + self.l1_reg_coef * self.reg_coef * np.sum(np.abs(a)) + \
                                              self.l2_reg_coef * self.reg_coef * np.sum(a ** 2)

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        np.random.seed(1234)
        X = (X_train - np.mean(X_train))/np.std(X_train)
        X = np.hstack((np.ones((X.shape[0], 1)), X))
        dim = X.shape[1]
        eps = 0.00000001
        E_g_2 = np.zeros(dim)
        E_a_2 = np.zeros(dim)
        RMS_a = np.sqrt(E_a_2 + eps)
        RMS_g = np.sqrt(E_g_2 + eps)
        a = np.array([np.random.normal(0, 10) * dim])
        X = np.array_split(X, self.batch_size)
        Y = np.array_split(y_train, self.batch_size)
        a = a.reshape(1, a.shape[0])
        i = 0
        self.loss_res = np.array([])
        while i < self.max_iter:
            LinearRegression.shuffle(X, Y)
            for batch, res in zip(X, Y):
                g_t = self.grad(a, batch, res.reshape(res.shape[0], 1))
                E_g_2 = self.gamma * E_g_2 + (1 - self.gamma) * (g_t ** 2)
                RMS_g = np.sqrt(E_g_2 + eps)
                delta_a = - (RMS_a / RMS_g) * g_t
                a = a + delta_a
                E_a_2 = self.gamma * E_a_2 + (1 - self.gamma) * (delta_a ** 2)
                RMS_a = np.sqrt(E_a_2 + eps)
                self.loss_res = np.concatenate((self.loss_res, [self.loss(a, batch, res)]))
            i += 1
        self.weights = a
        self.print_plot()

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        X = (X_test - np.mean(X_test)) / np.std(X_test)
        X = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return X @ self.weights.T

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.weights
