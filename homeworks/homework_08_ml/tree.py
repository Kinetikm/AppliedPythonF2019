#!/usr/bin/env python
# coding: utf-8


import numpy as np


class Node:
    def __init__(self, x, y, idxs, min_leaf):
        self.x = x
        self.y = y
        self.idxs = idxs
        self.min_leaf = min_leaf
        self.row_count = len(idxs)
        self.col_count = x.shape[1]
        self.val = np.mean(y[idxs])
        self.score = float('inf')
        self.feature_importance_ = {}
        self.split()

    def split(self):
        for col in range(self.col_count):
            x = self.x[self.idxs, col]
            for row in range(self.row_count):
                lhs = x <= x[row]
                rhs = x > x[row]
                if rhs.sum() < self.min_leaf or lhs.sum() < self.min_leaf:
                    continue
                curr_score = self.find_score(lhs, rhs)
                if curr_score < self.score:
                    self.var_idx = col
                    self.score = curr_score
                    self.split = x[row]
        if self.is_leaf:
            return
        x = self.split_col
        lhs = np.nonzero(x <= self.split)[0]
        rhs = np.nonzero(x > self.split)[0]
        self.lhs = Node(self.x, self.y, self.idxs[lhs], self.min_leaf)
        self.rhs = Node(self.x, self.y, self.idxs[rhs], self.min_leaf)

    def find_score(self, lhs, rhs):
        y = self.y[self.idxs]
        lhs_std = y[lhs].std()
        rhs_std = y[rhs].std()
        return lhs_std * lhs.sum() + rhs_std * rhs.sum()

    @property
    def split_col(self):
        return self.x[self.idxs, self.var_idx]

    @property
    def is_leaf(self):
        return self.score == float('inf')

    def predict(self, x):
        return np.array([self.predict_row(xi) for xi in x])

    def predict_row(self, x_i):
        if self.is_leaf:
            return self.val
        node = self.lhs if x_i[self.var_idx] <= self.split else self.rhs
        return node.predict_row(x_i)


class Tree:
    def __init__(self, criterion='mse', max_depth=6, min_samples_leaf=5):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.tree = Node(X_train, y_train, np.array(np.arange(len(y_train))), self.min_samples_leaf)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        return self.tree.predict(X_test)

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        pass


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
