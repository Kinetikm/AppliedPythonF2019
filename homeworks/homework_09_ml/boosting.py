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
        self.subsample = subsample
        self.sub_col = subsample_col
        self.trees = []
        self.features_lst = []

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.y_mean = np.mean(y_train)
        y_pred = np.zeros(X_train.shape[0], )
        y_pred[:] = np.mean(y_train)
        n_samples = int(X_train.shape[0] * self.subsample)
        n_features = int(X_train.shape[1] * self.sub_col)
        for i in range(self.n_estimators):
            samples = np.random.choice(np.arange(0, X_train.shape[0]), size=(n_samples,), replace=False)
            features = np.random.choice(np.arange(0, X_train.shape[1]), size=(n_features,), replace=False)
            self.features_lst.append(features)
            x = X_train[np.ix_(samples, features)]
            y = y_train[np.ix_(samples, )]
            if i == 0:
                grad = y
            else:
                grad = (y_train - y_pred) * 2
                grad = grad[np.ix_(samples, )]
            tree = DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf)
            tree.fit(x, grad)
            predictions = tree.predict(x)
            y_pred[np.ix_(samples, )] += self.learning_rate * predictions
            self.trees.append(tree)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_pred = np.ones(X_test.shape[0], ) * self.y_mean
        for i, tree in enumerate(self.trees):
            lst = [i for i in range(X_test.shape[0])]
            x = X_test[np.ix_(lst, self.features_lst[i])]
            y_pred += self.learning_rate * tree.predict(x)
        return y_pred
