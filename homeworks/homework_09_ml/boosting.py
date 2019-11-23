#!/usr/bin/env python
# coding: utf-8

import random
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from collections import namedtuple


class GradientBoosting:

    Estimator = namedtuple('Estimator' , 'model gamma')

    def __init__(self, n_estimators=100, learning_rate=1.0, max_depth=None,
                 min_samples_leaf=1, subsample=1.0, subsample_col=1.0):
        """
        :param n_estimators: number of trees in model
        :param learning_rate: discount for gradient step
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        :param subsample: the fraction of samples to be used for fitting the individual base learners
        :param subsample_col: the fraction of features to be used for fitting the individual base learners
        """

        self.max_depth = max_depth
        self.subsample = subsample

        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.subsample_col = subsample_col

        self.min_samples_leaf = min_samples_leaf

        self._ensebmle = []
        self.const_value = None

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """

        self.const_value = np.mean(y_train)

        for _ in range(self.n_estimators):
            x_sample, y_sample = self.subsampleXY(X_train, y_train)
            old_pred = self.predict(x_sample)
            # print("old_pred:", old_pred)
            pseudo_residual = y_sample - old_pred

            tree = DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf)
            tree.fit(x_sample, pseudo_residual)

            estim_pred = tree.predict(x_sample)
            gamma = self.learning_rate * self.get_gamma(pseudo_residual, estim_pred)

            self._ensebmle.append(self.Estimator(model=tree, gamma=gamma))

    def get_gamma(self, pseudo_residual, estim_pred):
        return np.mean(pseudo_residual/estim_pred)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """

        y_pred = np.full((X_test.shape[0],), self.const_value)

        for est in self._ensebmle:
            y_pred += est.gamma * est.model.predict(X_test)

        return y_pred / (len(self._ensebmle) + 1)

    def subsampleXY(self, X_train, y_train):

        n_samples, n_cols = X_train.shape

        max_n_samples = int(n_samples * self.subsample)
        max_n_cols = int(n_cols * self.subsample_col)

        idx_sample = np.random.choice(n_samples, max_n_samples, replace=False)
        cols_sample = np.random.choice(n_cols, max_n_cols, replace=False)

        x_sample = X_train[idx_sample]
        x_sample = x_sample[:, cols_sample]

        y_sample = y_train[idx_sample]
        return x_sample, y_sample
