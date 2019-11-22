#!/usr/bin/env python
# coding: utf-8

import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split


class GradientBoosting:
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
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        if subsample > 1 or subsample_col > 1 or not subsample or not subsample_col:
            raise ValueError
        self.subsample_coef = subsample
        self.subsample_col_coef = subsample_col
        self.constant = None
        self.trees = []
        self.features_for_estimator = []
        self.coefficients = []

    @staticmethod
    def get_constant(y):
        return np.mean(y)

    def anti_grad(self, X, y):
        return 2 * (y - self.predict(X))

    def calculate_coef(self, X, y, current_predictions):
        return np.sum(y - self.predict(X) * current_predictions) / np.sum(current_predictions ** 2)

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        n_estimators = 0
        self.constant = GradientBoosting.get_constant(y_train)
        while n_estimators < self.n_estimators:
            tree = DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf)
            x_train_i, x_test, y_train_i, y_test = train_test_split(X_train, y_train, test_size=1 - self.subsample_coef)
            columns = sorted(np.random.choice(x_train_i.shape[1], round(self.subsample_col_coef * x_train_i.shape[1]),
                                              replace=False))
            x_train_i_feature = np.hstack([x_train_i[:, i:i+1] for i in columns])
            g_train = self.anti_grad(x_train_i, y_train_i)
            tree.fit(x_train_i_feature, g_train)
            current_predictions = tree.predict(x_train_i_feature)
            b = self.calculate_coef(x_train_i, y_train_i, current_predictions)
            self.trees.append(tree)
            self.features_for_estimator.append(columns)
            self.coefficients.append(b * self.learning_rate)
            n_estimators += 1

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        result = [self.constant] * X_test.shape[0]
        for i, tree in enumerate(self.trees):
            X = np.hstack([X_test[:, k:k+1] for k in self.features_for_estimator[i]])
            result += self.coefficients[i] * tree.predict(X)
        return result
