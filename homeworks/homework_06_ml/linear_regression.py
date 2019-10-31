#!/usr/bin/env python
# coding: utf-8
import numpy as np


class LinearRegression:
    def __init__(self, lambda_coef=1.0, regulatization='elastic', alpha=0.5, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.lambda_coef = lambda_coef
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter

        np.random.seed(1707)

    def get_next_batch(self, X, Y, batch_size):
        index = np.random.choice(X.shape[0], batch_size, replace=False)
        x_batch = X[index]
        y_batch = Y[index]
        return x_batch, y_batch

    def grad(self, X, Y):
        gt = (2 / X.shape[1]) * X.T @ (X @ self.theta - Y)

        l1 = self.alpha
        l2 = self.alpha
        gt = gt + l1 * np.sign(self.theta) + l2 * self.theta  # регуляризация

        return gt

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        # ADAM

        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        self.theta = np.random.rand(X_train.shape[1], 1)
        beta1 = 0.9
        beta2 = 0.999
        eps = 10e-8
        m = np.zeros(self.theta.shape)
        v = np.zeros(self.theta.shape)

        conv = 10e-10  # точность, до которой хочется, чтобы алгоритм сходился
        for i in range(self.max_iter):
            x_batch, y_batch = self.get_next_batch(X_train, y_train, self.batch_size)
            grad = self.grad(x_batch, y_batch.reshape(-1, 1))

            m = beta1 * m + (1 - beta1) * grad
            v = beta2 * v + (1 - beta2) * (grad ** 2)
            m_hat = m / (1 - pow(beta1, i+1))
            v_hat = v / (1 - pow(beta2, i+1))

            dtheta = (self.lambda_coef / np.sqrt(v_hat + eps)) * m_hat

            # сравниваем изменение модуля вектора весов, если оно очень небольшое,
            # то алгоритм сошелся до прохождения максимального количества итераций
            if np.sqrt(np.dot(dtheta, dtheta.T))[0][0] < conv:
                break

            self.theta = self.theta - dtheta

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return X_test @ self.theta

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.theta
