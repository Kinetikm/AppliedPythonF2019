#!/usr/bin/env python
# coding: utf-8


import numpy as np


class Tree:
    class Node:
        def __init__(self, left_node=None, right_node=None):
            self.left_node = left_node
            self.right_node = right_node
            self.th = -1
            self.index = 0
            self.label = None

        def set(self, th, index):
            self.th = th
            self.index = index

    def __init__(self, criterion, max_depth, min_samples_leaf):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        self._max_depth = max_depth
        self._min_samples_leaf = min_samples_leaf
        self._criterion = self.mse if criterion == 'mse' else self.mae
        self._tree = None
        self._weight = np.array([])

    def mse(self, y):
        return np.mean((y - np.mean(y)) ** 2)

    def mae(self, y):
        return np.mean(np.abs(y - np.mean(y)))

    def split(self, X, y, i, th):
        if th is None:
            return 0

        split_ind = X[:, i] < th
        X_left = X[split_ind]
        y_left = y[split_ind]
        X_right = X[~split_ind]
        y_right = y[~split_ind]

        if len(X_left) == 0 or len(X_right) == 0:
            return 0

        return self._criterion(y) - (X_left.shape[0] / X.shape[0]) * self._criterion(y_left) - (
                X_right.shape[0] / X.shape[0]) * self._criterion(y_right)

    def fit(self, X_train, y_train, node=None, depth=1):
        """
        Fit model using gradient descent method
        :param node:
        :param depth: depth
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        cols = X_train.shape[1]
        if not node:
            node = self.Node()
            self._tree = node
            self._weight = np.zeros(cols)

        if self._min_samples_leaf and len(y_train) < self._min_samples_leaf:
            node.label = y_train
            return
        elif self._max_depth and depth > self._max_depth:
            node.label = y_train
            return

        max_gain = 0
        best_id = 0
        best_th = 0

        for i in range(cols):
            for th in np.unique(X_train[:, i]):
                gain = self.split(X_train, y_train, i, th)
                if gain > max_gain:
                    max_gain = gain
                    best_id = i
                    best_th = th

        if max_gain == 0:
            return

        if not node:
            node = self.Node()
            self._tree = node
            self._weight = np.zeros(cols)

        node.set(best_th, best_id)
        node.right_node = self.Node()
        node.left_node = self.Node()
        split_ind = X_train[:, best_id] < best_th

        self.fit(X_train[split_ind], y_train[split_ind], node.left_node, depth + 1)
        self.fit(X_train[~split_ind], y_train[~split_ind], node.right_node, depth + 1)
        self._weight[best_id] = max_gain

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """

        def predict_val(x):
            node = self._tree
            while node.left_node is not None or node.right_node is not None:
                node = node.left_node if x[node.index] < node.th else node.right_node
            return np.mean(node.label)

        return np.array([predict_val(x) for x in X_test])

    def get_feature_importance(self, normalize=False):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        return self._weight / self._weight.sum() if normalize else self._weight


class TreeRegressor(Tree):
    def __init__(self, criterion='mse', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'mse' or 'mae'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)


class TreeClassifier(Tree):
    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'gini' or 'entropy'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)
        raise NotImplementedError

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        pass
