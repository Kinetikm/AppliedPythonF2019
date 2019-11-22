#!/usr/bin/env python
# coding: utf-8


import numpy as np
from sklearn.tree import DecisionTreeRegressor
from random import sample


class GradientBoosting:
    def __init__(self, n_estimators=100, learning_rate=0.01, max_depth=None,
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
        self.forest = []
        self.features = []
        self.const = 0

    def samp(self, x):
        sample_idx = sample(range(x.shape[0]), int(self.subsample*x.shape[0]))
        feature_idx = sample(range(x.shape[1]), int(self.subsample_col*x.shape[1]))
        return sample_idx, feature_idx

    def fit(self, X_train, y_train):
        """
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        sample_idx, feature_idx = self.samp(X_train)
        y_train = y_train.reshape((-1, 1))
        y_tr = y_train[sample_idx, :]
        self.const = y_tr.mean()
        r = 2*(y_tr - self.const)
        f = np.full(len(y_tr), self.const)
        for _ in range(self.n_estimators):
            tr = DecisionTreeRegressor(criterion='mse', max_depth=self.max_depth,
                                       min_samples_leaf=self.min_samples_leaf)
            sample_idx, feature_idx = self.samp(X_train)
            self.features.append(feature_idx)
            y_tr = y_train[sample_idx, :]
            x_tr = X_train[sample_idx, :]
            x_tr = x_tr[:, feature_idx]
            tr.fit(x_tr, r)
            self.forest.append(tr)
            f += self.learning_rate*tr.predict(x_tr)
            r = 2*(y_tr - f.reshape((-1, 1)))

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_pred = np.full(X_test.shape[0], self.const)
        for t in range(self.n_estimators):
            y_pred += self.learning_rate*self.forest[t].predict(X_test[:, self.features[t]])
        return y_pred
