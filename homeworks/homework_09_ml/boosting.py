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

    def fit(self, X_train, y_train):
        tree = DecisionTreeRegressor(criterion='mse', max_depth=self.max_depth, min_samples_leaf=self.min_samles_leaf)
        self.average = y_train.mean()
        h = self.average
        for i in range(self.n_estimators):
            g = y_train - h
            tree.fit(X_train, g)
            self.tree_list.append(tree)
            h += self.learning_rate * tree.predict(X_train)

    def predict(self, X_test):
        y_test = self.average
        for tree in self.tree_list:
            y_test += self.learning_rate * tree.predict(X_test)
        return y_test
