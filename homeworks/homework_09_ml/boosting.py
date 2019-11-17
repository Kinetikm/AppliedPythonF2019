#!/usr/bin/env python
# coding: utf-8


import numpy as np
from sklearn.tree import DecisionTreeRegressor


class GradientBoosting:
    def __init__(self, n_estimators=100, learning_rate=1.0, max_depth=None,
                 min_samples_leaf=1, subsample=1.0, subsample_col=1.0):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samles_leaf = min_samples_leaf
        self.subsample = subsample
        self.subsample_col = subsample_col
        self.tree_list = []
        self.features_list = []

    def fit(self, X_train, y_train):
        tree = DecisionTreeRegressor(criterion='mse', max_depth=self.max_depth, min_samples_leaf=self.min_samles_leaf)
        self.average = y_train.mean()
        h = np.full(y_train.shape, self.average)
        n_samples = int(X_train.shape[0] * self.subsample)
        n_features = int(X_train.shape[1] * self.subsample_col)

        for i in range(self.n_estimators):
            idx = np.random.randint(X_train.shape[0], size=n_samples)
            features = np.random.randint(X_train.shape[1], size=n_features)
            self.features_list.append(features)
            X_sample = X_train[idx, :]
            X_sample = X_sample[:, features]
            y_sample = y_train[idx]
            g = y_sample - h[idx]
            tree.fit(X_sample, g)
            self.tree_list.append(tree)
            h[idx] += self.learning_rate * tree.predict(X_sample)

    def predict(self, X_test):
        y_test = self.average
        for i in range(len(self.tree_list)):
            tree = self.tree_list[i]
            features = self.features_list[i]
            y_test += self.learning_rate * tree.predict(X_test[:, features])
        return y_test
