#!/usr/bin/env python
# coding: utf-8

import numpy as np
import copy
from sklearn.tree import DecisionTreeRegressor


class GradientBoosting:
    def __init__(self, n_estimators=100, learning_rate=0.001, max_depth=None,
                 min_samples_leaf=1, subsample=0.8, subsample_col=0.8):
        """
        :param n_estimators: number of trees in model
        :param learning_rate: discount for gradient step
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        :param subsample: the fraction of samples to be used for fitting the individual base learners
        :param subsample_col: the fraction of features to be used for fitting the individual base learners
        """
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.subsample = subsample
        self.subsample_col = subsample_col
        self.coef_ = []
        self.trees = []
        self.feature_numbers = []

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.X_train = copy.deepcopy(X_train)
        self.y_train = y_train.reshape(-1, 1)

        # зададим начальный предикт как среднее арифметическое
        prediction = np.mean(y_train) * np.ones([y_train.shape[0]])

        for i in range(self.n_estimators):

            if i == 0:
                antigradient = y_train
            else:
                antigradient = y_train - prediction
            # выбираем рандомную подвыборку size = subsample*X_train.shape[0]
            X_part, antigradient_part, y_part = self._bagging(antigradient)
            # создаем новое дерево и обучаем на части выборки
            tree = DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf)
            X_part, feature_numbers = self._RMS(X_part)
            self.feature_numbers.append(feature_numbers)
            tree.fit(X_part, antigradient_part)
            a = tree.predict(self._RMS(X_train, feature_numbers)).reshape([X_train.shape[0]])
            # находим коэффициент на основе части выборки для данного дерева
            b = self._coef(X_part, antigradient_part, i, tree)
            # и добавляем дерево и коэффициент в соответсвующие списки
            self.trees.append(tree)
            self.coef_.append(b)

            prediction += b * a

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_pred = np.ones([X_test.shape[0]]) * np.mean(self.y_train)

        for i in range(self.n_estimators):
            y_pred += self.coef_[i] * self.trees[i].predict(self._RMS(X_test, self.feature_numbers[i])).reshape(
                [X_test.shape[0]])
        return y_pred

    def _bagging(self, antigradient):
        antigradient = antigradient.reshape(-1, 1)
        x_y = np.hstack((self.X_train, antigradient, self.y_train))
        x_y = np.random.permutation(x_y)
        k_subsample = int(self.subsample * self.X_train.shape[0])
        X_train_part = x_y[:k_subsample, :-2]
        antigradient_part = x_y[:k_subsample, -2]
        y_part = x_y[:k_subsample, -1]

        return X_train_part, antigradient_part, y_part

    def _RMS(self, X, feature_numbers=None):
        if feature_numbers is None:
            feature_numbers = np.random.randint(X.shape[1], size=int(X.shape[1] * self.subsample_col))
            x_part = X[:, feature_numbers]
            return x_part, feature_numbers
        else:
            return X[:, feature_numbers]

    def _coef(self, X_part, y_part, k, tree):
        b = 1
        if k == 0:
            y_pred = np.ones([X_part.shape[0]]) * np.mean(y_part)
        else:
            y_pred = np.ones([X_part.shape[0]]) * np.mean(y_part)
            for i in range(k):
                y_pred += self.coef_[i] * self.trees[i].predict(X_part).reshape([X_part.shape[0]])

        a = tree.predict(X_part)

        for i in range(30):
            grad = -(y_part - y_pred - b * a).sum()
            b -= self.learning_rate * grad / y_part.shape[0]

        return b
