#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self,
                 lambda_coef=0.001,
                 regulatization=None,
                 alpha=0.5,
                 ro=0.5,
                 batch_size=50,
                 max_iter=100,
                 print_logs=False):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        Regularization: l1, Optim: Adadelta
        """
        self.lambda_coef = lambda_coef
        self.ro = ro
        self.regulatization = regulatization
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self._w = 0
        self.print_logs = print_logs
        self.loss_train = []

    def sigmoid(self, x, w):
        return 1. / (1. + np.exp(-(x @ w.T)))

    def log_loss(self, y_true, y_pred):
        return -np.sum(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)) / y_true.shape[0]

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        # X_train.shape = (n, m)
        # y_train.shape = (n, )
        # Добавляем фиктивный единичный столбец
        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))  # X_train.shape = (n, m + 1)
        self._w = np.random.normal(scale=1e-6, size=(X_train.shape[1]))  # self._w.shape = (m + 1, )
        y_train = y_train.reshape(-1, 1)  # y_train.shape = (1, n)

        # Инициализируем вектор для Adadelta
        g = np.zeros_like(self._w)
        eps = 1e-7

        data = np.hstack((X_train, y_train))
        for i in range(self.max_iter):
            n_batches = X_train.shape[0] // self.batch_size  # считаем количество целый батчей в X_train
            data_perm = np.random.permutation(data)  # рандомно мешаем data
            X_train = data_perm[:, :-1]  # X_train.shape = (n, m + 1)
            y_train = data_perm[:, -1]  # y_train.shape = (n, )
            loss = 0
            for idx in range(n_batches):
                sample = X_train[idx * self.batch_size:(idx + 1) * self.batch_size]
                y_true = y_train[idx * self.batch_size:(idx + 1) * self.batch_size]
                y_pred = self.sigmoid(sample, self._w)

                gradient = self.step(sample, y_true)
                g = self.ro * g + (1 - self.ro) * gradient ** 2
                self._w += self.lambda_coef * gradient / np.sqrt(g + eps)

                loss += self.log_loss(y_true, y_pred)
            self.loss_train.append(loss / n_batches)
            if self.print_logs:
                if i % 100 == 0:
                    print(f'epoch : {i}  loss : {self.loss_train[i]}')

    def step(self, x, y_true):
        grad = np.zeros_like(self._w)
        for j in range(x.shape[1]):
            grad[j] += np.sum((y_true - self.sigmoid(x, self._w)) * x[:, j])
            if self.regulatization == 'L1':
                grad[j] += self.alpha * np.sign(self._w[j])
            if self.regulatization == 'L2':
                raise NotImplementedError
        return grad / x.shape[1]

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return np.where(self.sigmoid(self._w, X_test) >= 0.5, 1, 0)

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return self.sigmoid(self._w, X_test)

    @property
    def weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self._w
