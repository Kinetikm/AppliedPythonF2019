#!/usr/bin/env python
# coding: utf-8
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split


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
        self._mean = np.array([])
        self._n_estimators = n_estimators
        self._learning_rate = learning_rate
        self._max_depth = max_depth
        self._min_samples_leaf = min_samples_leaf
        self._subsample = subsample
        self._subsample_col = subsample_col
        self._trees = []
        self._features = []

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self._mean = np.mean(y_train)
        y_train = np.array(y_train)
        _, _, y, _ = train_test_split(X_train, y_train, train_size=self._subsample)
        gradient = 2 * (y - self._mean)
        predict = np.full((y.shape[0],), self._mean)
        for i in range(self._n_estimators):
            features = np.random.choice(X_train.shape[1], int(X_train.shape[1] * self._subsample_col))
            x, _, y, _ = train_test_split(X_train, y_train, train_size=self._subsample)
            tree = DecisionTreeRegressor(max_depth=self._max_depth, min_samples_leaf=self._min_samples_leaf)
            tree.fit(x[:, features], gradient)
            self._features.append(features)
            self._trees.append(tree)
            predict += self._learning_rate * tree.predict(x[:, features])
            gradient = 2 * (y - predict)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        predict = self._mean
        for i in range(self._n_estimators):
            predict += self._learning_rate * self._trees[i].predict(X_test[:, self._features[i]])
        return predict
