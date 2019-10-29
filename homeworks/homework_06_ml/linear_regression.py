#!/usr/bin/env python
# coding: utf-8

import numpy as np
import copy


class LinearRegression:
    def __init__(self, lambda_coef=1.0, regulatization='L1', alpha=0.5, batch_size=50, max_iter=100, norm=True):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        # ВАРИАНТ 3 Loss: MSE, Regularization: l1, Optim: Adam
        self.lambda_coef = lambda_coef
        self.regulatization = regulatization
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.norm = True
        self.Loss = [0]

    def fit(self, X_train, y_train, beta1=0.9, beta2=0.99, eps=1e-8, count=5):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """

        X_train = self._check_type(X_train)
        if X_train.shape == 1:
            X_train = np.reshape(X_train, (-1, 1))
        X_train = np.insert(X_train, 0, np.ones((X_train.shape[0])), axis=1)

        X_tr_y_tr = copy.deepcopy(X_train)
        X_tr_y_tr = np.insert(X_tr_y_tr, X_tr_y_tr.shape[1], y_train, axis=1)

        y_train = np.reshape(self._check_type(y_train), (-1, 1))

        if X_train.shape[0] != y_train.shape[0]:
            print("не соответствуют размеры X_train и y_train")
            raise ValueError

        if self.norm:
            X_train = self._normalization(X_train)

        self.w = np.zeros((X_train.shape[1], 1))
        mt = 0
        vt = 0
        Loss_prev = 0
        flag = 0

        for i in range(1, (self.max_iter + 1)):
            k = X_train.shape[0] // self.batch_size
            # X_y = np.random.permutation(X_tr_y_tr)[:self.batch_size]
            set_of_batch = self._split_into_batch(X_tr_y_tr)
            for j in range(k):
                x = set_of_batch[j][:, :-1]
                y = set_of_batch[j][:, -1].reshape(-1, 1)

                gt = self._gradient(x, y)
                mt = beta1 * mt + (1 - beta1) * gt
                vt = beta2 * vt + (1 - beta2) * gt * gt
                mt_ = mt / (1 - beta1 ** i)
                vt_ = vt / (1 - beta2 ** i)

                self.w -= self.alpha * mt_ / np.sqrt(vt_ + eps)
            x = X_tr_y_tr[:, :-1]
            y = X_tr_y_tr[:, -1].reshape(-1, 1)
            Loss = self._loss_MSE(x, y)
            # условие на выход из цикла
            if Loss - Loss_prev < 0 and i != 1:
                flag = 0
            else:
                flag += 1
            # если count раз не уменьшилась функция потерь, тогда выход
            if flag == count:
                return self.w
            Loss_prev = Loss

    def _split_into_batch(self, x_y):
        x_y = np.random.permutation(x_y)
        k = x_y.shape[0] // self.batch_size
        result = []
        for i in range(k):
            result.append(x_y[i * self.batch_size:(i + 1) * self.batch_size])
        return result

    def _gradient(self, x, y):
        g = np.empty_like(self.w)

        for i in range(x.shape[1]):
            c = 0
            for j in range(self.batch_size):
                c += 2 * (self.predict(x[i], flag='tr') - y[i]) * x[j][i]
            g[i][0] = int(c) / self.batch_size + self.alpha * np.sign(self.w[i][0])
        return g

    def predict(self, X_test, flag='test'):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        X_test = self._check_type(X_test)
        if X_test.shape == 1:
            X_test = np.reshape(X_test, (-1, 1))

        if flag == 'test':
            X_test = np.insert(X_test, 0, np.ones((X_test.shape[0])), axis=1)
        y_test = X_test @ self.w
        return y_test

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self.w

    def _normalization(self, x):
        mean_ = x.mean(axis=0)
        scale_ = np.sqrt(x.var(axis=0))
        if len(x.shape) == 1:
            x = np.array(list(map(lambda t: (t - mean_) / scale_, x)))
            return x
        else:
            x = x.T
            for i in range(x.shape[0]):
                x[i] = np.array(list(map(lambda t: (t - mean_[i]) / scale_[i], x[i])))
        return x.T

    def _check_type(self, x):
        # проверка на то, что пользователь загрузил выборки типа list или np.darray
        if isinstance(x, np.ndarray):
            return x
        elif isinstance(x, list):
            return np.array(x)
        else:
            raise TypeError

    def _loss_MSE(self, X_train, y_train):
        a_x = self.predict(X_train, flag='tr')
        differ = a_x - y_train
        x = np.array(list(map(lambda t: (t ** 2) / self.batch_size, differ))).sum()
        return x
