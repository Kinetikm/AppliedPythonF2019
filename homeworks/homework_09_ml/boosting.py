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
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.subsample = subsample
        self.subsample_col = subsample_col

        self.trees = []
        self.target_mean = 0
        self.features = []

    def get_next_batch(self, X, Y, batch_size):
        index = np.random.choice(X.shape[0], batch_size, replace=False)
        x_batch = X[index]
        y_batch = Y[index]
        return x_batch, y_batch

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.target_mean = np.mean(y_train)
        pred = np.full(y_train.shape[0], np.mean(y_train))

        for _ in range(self.n_estimators):
            samples = np.random.choice(X_train.shape[0], int(X_train.shape[0]*self.subsample), replace=False)
            features = np.random.choice(X_train.shape[1], int(X_train.shape[1]*self.subsample_col), replace=False)
            self.features.append(features)
            x = X_train[np.ix_(samples, features)]

            grad = (y_train - pred)[samples]

            tree = DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf)
            tree.fit(x, grad)
            pred[samples] += self.learning_rate * tree.predict(x)
            self.trees.append(tree)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        pred = np.ones([X_test.shape[0]]) * self.target_mean
        for i in range(self.n_estimators):
            pred += self.learning_rate * self.trees[i].predict(X_test[:, self.features[i]])
        return pred
