#!/usr/bin/env python
# coding: utf-8

import numpy as np
from sklearn.tree import DecisionTreeRegressor


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
        self.n_est = n_estimators
        self.rate = learning_rate
        self.max_depth = max_depth
        self.min_sleaf = min_samples_leaf
        self.subsamp = subsample
        self.sub_col = subsample_col
        self.ensemble = list()
        self.featseq = list()

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        if X_train.shape[1] * self.sub_col < 1 or X_train.shape[0] * self.subsamp < 1:
            print("size of subsamples is small")
            raise ValueError
        res = y_train.sum() / y_train.shape[0]
        self.ensemble.append(lambda x: res)
        for i in range(self.n_est):
            split_j_ind = np.random.choice(a=X_train.shape[1], size=int(X_train.shape[1] * self.sub_col), replace=False)
            split_i_ind = np.random.choice(a=X_train.shape[0], size=int(X_train.shape[0] * self.subsamp), replace=False)
            self.featseq.append(split_j_ind)
            x_split = X_train[split_i_ind]
            x_split = x_split[::, split_j_ind]
            y_split = y_train[split_i_ind]
            ans = np.zeros((x_split.shape[0],))
            for ens in self.ensemble:
                ans += ens(x_split)
            grad_func = -2 * (ans - y_split) * self.rate
            h = DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=self.min_sleaf)
            h.fit(x_split, grad_func)
            b = (-1) * (ans - y_split).sum() / (h.predict(x_split) ** 2).sum()
            self.ensemble.append(lambda x: b * h.predict(x))

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_test = np.zeros((X_test.shape[0],))
        y_test += self.ensemble[0](X_test)
        for i in range(1, len(self.ensemble)):
            y_test += self.ensemble[i](X_test[::, self.featseq[i - 1]])
        return y_test
