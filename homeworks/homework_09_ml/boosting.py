#!/usr/bin/env python
# coding: utf-8

import numpy as np
from sklearn.tree import DecisionTreeRegressor


class GradientBoosting:
    def __init__(self, n_estimators=100, learning_rate=0.5, max_depth=None,
                 min_samples_leaf=1, subsample=1.0, subsample_col=1.0):
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
        self.const = 0
        self.trees = []
        self.features = []
        self.coef_b = []

    def get_batch(self, shape, batch_size):
        all_index = np.arange(shape)
        np.random.shuffle(all_index)
        return all_index[:int(batch_size * shape)]

    def fit(self, x_train, y_train):
        """
        :param x_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.const = np.mean(y_train)
        for i in range(self.n_estimators):
            tree = DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf)
            rows = self.get_batch(x_train.shape[0], self.subsample)
            cols = self.get_batch(x_train.shape[1], self.subsample_col)
            x_train_i = x_train[rows]
            x_train_i_without_feature = x_train_i[:, cols]
            y_train_i = y_train[rows]
            antigradient = y_train_i - self.predict(x_train_i)
            tree.fit(x_train_i_without_feature, antigradient)
            a_i = tree.predict(x_train_i_without_feature)
            b_i = np.sum((antigradient - self.predict(x_train_i)) * a_i) / np.sum(a_i ** 2)
            self.trees.append(tree)
            self.features.append(cols)
            self.coef_b.append(b_i * self.learning_rate)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        h = [self.const] * X_test.shape[0]
        for i, tree in enumerate(self.trees):
            x_test = X_test[:, self.features[i]]
            h += self.coef_b[i] * tree.predict(x_test)
        return h
