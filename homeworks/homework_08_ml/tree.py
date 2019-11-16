#!/usr/bin/env python
# coding: utf-8


import numpy as np


class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, stor_val=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.stor_val = stor_val


class Tree:
    def __init__(self, criterion, max_depth, min_samples_leaf):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        if criterion not in {"mse", "mae"}:
            raise NotImplementedError
        self.optim = criterion
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.root = None
        self.feature_importance = None
        self.n_train = None

    def I(self, y):
        if self.optim == 'mae':
            return np.mean(np.abs(y - np.mean(y)))
        elif self.optim == 'mse':
            return np.mean((y - np.mean(y)) ** 2)
        else:
            raise RuntimeError

    def gain(self, X_train, feature, val):
        mask = X_train[:, feature] <= val
        left = X_train[mask]
        right = X_train[~mask]
        if left.shape[0] < self.min_samples_leaf or right.shape[0] < self.min_samples_leaf:
            return None, None, None
        return self.I(X_train[:, -1]) - ((left.shape[0]/X_train.shape[0]) * self.I(left[:, -1]) +
                                         (right.shape[0] / X_train.shape[0]) * self.I(right[:, -1])), left, right

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        def recursive_fit(X_train, depth):
            if (self.max_depth and depth + 1 > self.max_depth) or X_train.shape[0] < 2 * self.min_samples_leaf:
                return Node(stor_val=np.mean(X_train[:, -1]))
            best_gain = None
            best_feature = None
            best_threshold = None
            left_subset = None
            right_subset = None
            for feature in range(X_train.shape[1] - 1):
                unique_feature_values = np.unique(X_train[:, feature])
                for val in unique_feature_values:
                    g, l, r = self.gain(X_train, feature, val)
                    if not best_gain or (g and g > best_gain):
                        best_gain = g
                        best_feature = feature
                        best_threshold = val
                        left_subset = l
                        right_subset = r
            self.feature_importance[best_feature] += (X_train.shape[0]/self.n_train) * best_gain
            l_node = recursive_fit(left_subset, depth + 1)
            r_node = recursive_fit(right_subset, depth + 1)
            return Node(best_feature, best_threshold, l_node, r_node)

        self.feature_importance = [0] * X_train.shape[1]
        X_train = np.hstack((X_train, y_train.reshape((y_train.shape[0], 1))))
        self.n_train = X_train.shape[0]
        self.root = recursive_fit(X_train, 0)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        def pred(line):
            node = self.root
            while node.feature is not None:
                if line[node.feature] <= node.threshold:
                    node = node.left
                else:
                    node = node.right
            return node.stor_val
        return np.apply_along_axis(pred, 1, X_test)

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        return self.feature_importance / np.sum(self.feature_importance)


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

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        pass
