#!/usr/bin/env python
# coding: utf-8


import numpy as np


class Node:
    def __init__(self, left_node=None, right_node=None, feature=None, threshold=None, value=None):
        self.left_node = left_node
        self.right_node = right_node
        self.value = value
        self.feature = feature
        self.threshold = threshold


class Tree:
    def __init__(self, criterion, max_depth, min_samples_leaf):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.depth = 0
        self.tree = None
        self.feature_importance = 0

    def metric(self, y):
        if self.criterion == 'mse':
            return np.mean((y - np.mean(y)) ** 2)
        elif self.criterion == 'mae':
            return np.mean(np.abs(y - np.mean(y)))
        else:
            raise ValueError

    def gain(self, y, index):
        return self.metric(y) - len(y[:index]) / len(y) * \
               self.metric(y[:index]) - len(y[index:]) / len(y) * self.metric(y[index:])

    def fit(self, X_train, y_train):
        """
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.feature_importance = np.zeros(X_train.shape[1])
        table = np.hstack((X_train, y_train.reshape((-1, 1))))
        self.tree = self.build_tree(table)

    def build_tree(self, table):
        if self.depth == self.max_depth or table.shape[0] < 2 * self.min_samples_leaf:
            return Node(value=np.mean(table[:, -1]))
        gain_max = 0
        for feature in range(table.shape[1] - 1):
            table = np.array(sorted(table, key=lambda x: x[feature]))
            for row in range(self.min_samples_leaf - 1, table.shape[0] - self.min_samples_leaf):
                gain = self.gain(table[:, -1], row)
                if gain > gain_max:
                    gain_max = gain
                    index = row
                    best_feature = feature
        table = np.array(sorted(table, key=lambda x: x[best_feature]))
        threshold = (table[index, best_feature] + table[index + 1, best_feature]) / 2
        self.depth += 1
        self.feature_importance[best_feature] += 1
        left_ = self.build_tree(table[:index, :])
        right_ = self.build_tree(table[index:, :])
        return Node(left_, right_, best_feature, threshold)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y = np.empty(X_test.shape[0])
        for row in range(X_test.shape[0]):
            node = self.tree
            while node.feature is not None:
                if X_test[row, node.feature] <= node.threshold:
                    node = node.left_node
                else:
                    node = node.right_node
            y[row] = node.value
        return y

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        return self.feature_importance


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
