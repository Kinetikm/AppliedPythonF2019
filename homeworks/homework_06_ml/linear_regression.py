#!/usr/bin/env python
# coding: utf-8

# Вар 14
# Loss: MAE, Regularization: elastic, Optim: Adam

import numpy as np


class LinearRegression:
    def __init__(self, lambda_coef=0.1, regulatization='elastic', alpha=0.001, loss_eps=1e-7,
                 batch_size=50, max_iter=100, eps=1e-6, l1_ratio=0.5, betta1=0.5, betta2=0.5):

        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1", "L2", "elastic") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """

        self.lambda_coef = lambda_coef
        self.regulatization = regulatization
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter

        self.loss_eps = loss_eps

        self.l1_ratio = l1_ratio

        self.eps = eps
        self.betta1 = betta1
        self.betta2 = betta2

        return

    def get_mae_loss(self, y_pred, y):
        return sum(abs(y-y_pred)) / y_pred.shape[0]

    def get_grad(self, X_train, y_pred, y):
        grad = np.zeros_like(self.weights)

        n = X_train.shape[0]
        m = X_train.shape[1]

        for j in range(m):
            grad_arr = [X_train[i, j] * np.sign(y_pred[i] - y[i]) for i in range(n)]
            jgrad = np.sum(grad_arr)
            jgrad /= n

            if self.regulatization == 'elastic':
                jgrad += self.alpha * self.l1_ratio \
                    * abs(self.weights[j]) + self.alpha * (1-self.l1_ratio)/2 * self.weights[j] ** 2

            elif self.regulatization == 'L1':
                jgrad += self.alpha * abs(self.weights[j])
            elif self.regulatization == 'L2':
                jgrad += self.alpha * (self.weights[j]) ** 2
            else:
                raise Exception("Unknown regularisation")

            grad[j] = jgrad
        return grad

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """

        n = X_train.shape[0]
        m = X_train.shape[1]

        self.weights = np.random.normal(scale=0.001, size=(m,))

        opt_m = 0
        opt_v = 0
        priv_loss = 0
        for i in range(1, self.max_iter):
            loss = 0
            for j in range(0, 1, self.batch_size):
                X_batch = X_train[j:max(n, j+self.batch_size)]
                y_batch = y_train[j:max(n, j+self.batch_size)]

                y_pred = self.predict(X_batch)
                loss += self.get_mae_loss(y_pred, y_batch)
                grad = self.get_grad(X_batch, y_pred, y_batch)

                # adam optimisation
                opt_m = self.betta1 * opt_m + (1-self.betta1) * grad
                opt_v = self.betta2 * opt_v + (1-self.betta2) * grad**2
                m_hat = opt_m / (1 - self.betta1 ** i)
                v_hat = opt_v / (1 - self.betta2 ** i)
                self.weights -= self.lambda_coef * m_hat / (np.sqrt(v_hat) + self.eps)

            if abs(priv_loss - loss) < self.loss_eps:
                print("Loss eps reached")
                break

            priv_loss = loss

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        return X_test @ self.weights.T

    def getweightseights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.weights
