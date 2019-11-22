#!/usr/bin/env python
# coding: utf-8
from sklearn import tree
import numpy as np


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
        self.subsample = subsample
        self.subsample_col = subsample_col
        self.trees = []
        self.h = None
        self.m = 0

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.m = np.mean(y_train)
        self.h = np.zeros_like(y_train)
        self.h[:] = self.m
        for i in range(self.n_estimators):
            t = tree.DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf)
            n_samples = int(self.subsample * X_train.shape[0])
            if n_samples == 0:
                n_samples += 1
            n_features = int(self.subsample_col * X_train.shape[1])
            if n_features == 0:
                n_features += 1
            samples = np.random.choice(X_train.shape[0], size=n_samples, replace=False)
            features = np.random.choice(X_train.shape[1], size=n_features, replace=False)
            X_t = X_train[samples]
            X_t = X_t[:, features]
            t = t.fit(X_t, y_train[samples] - self.h[samples])
            self.h[samples] += self.learning_rate * t.predict(X_t)
            self.trees.append((t, features))

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        if len(self.trees) > 0:
            y_test = np.zeros((1, X_test.shape[0]))
            y_test[:] = self.m
            for i in range(self.n_estimators):
                X_t = X_test[:, self.trees[i][1]]
                y_test += self.learning_rate * self.trees[i][0].predict(X_t)
            return y_test[0]
        else:
            raise NotImplementedError
