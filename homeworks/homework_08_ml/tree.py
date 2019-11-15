#!/usr/bin/env python
# coding: utf-8


import numpy as np


class Node:
    def __init__(self, metric, num_samples, predicted):
        self.metric = metric
        self.num_samples = num_samples
        self.predicted = predicted
        self.feature_index = 0
        self.threshold = 0
        self.left = None
        self.right = None


class Tree:
    def __init__(self, criterion, max_depth, min_samples_leaf):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        if criterion != 'mse' and criterion != 'mae':
            raise NotImplementedError
        else:
            self._crit = criterion
        if max_depth < 2:
            raise ValueError("max depth should be 2 or more")
        else:
            self._max_depth = max_depth
        if min_samples_leaf < 1:
            raise ValueError("min samples by leaf should be more than 0")
        self._min_leaf = min_samples_leaf
        self._num_features = 0
        self._tree = None

    def _metric(self, y, y_pred):
        if self._crit == 'mse':
            return sum((n - y_pred) ** 2 for n in y)
        elif self._crit == 'mae':
            return sum(abs(n - y_pred) for n in y)
        else:
            raise NotImplementedError

    def _best_split(self, X, y):
        m = y.size
        if m <= 2 * self._min_leaf:
            return None, None
        init_metric = self._metric(y, np.median(y))
        best_metric = np.inf
        best_idx, best_treshold = None, None
        for feat_num in range(self._num_features):
            thresholds, classes = zip(*sorted(zip(X[:, feat_num], y)))
            for i in range(self._min_leaf, m - self._min_leaf):
                y_left = y[:i]
                y_right = y[i:]
                left_metric = self._metric(y_left, np.median(y_left))
                right_metric = self._metric(y_right, np.median(y_right))
                gain = init_metric - ((i / m) * left_metric + ((m - i) / m) * right_metric)
                if thresholds[i] == thresholds[i - 1]:
                    continue
                if gain < best_metric:
                    best_metric = gain
                    best_idx = feat_num
                    best_treshold = (thresholds[i] + thresholds[i - 1]) / 2
        return best_idx, best_treshold

    def _grow_tree(self, X, y, depth=0):
        predicted = np.median(y)
        node = Node(
            metric=self._metric(y, predicted),
            num_samples=y.size,
            predicted=predicted
        )
        if depth < self._max_depth:
            idx, thrh = self._best_split(X, y)
            if idx is not None:
                indices_left = X[:, idx] < thrh
                X_left, y_left = X[indices_left], y[indices_left]
                X_right, y_right = X[~indices_left], y[~indices_left]
                node.feature_index = idx
                node.threshold = thrh
                node.left = self._grow_tree(X_left, y_left, depth + 1)
                node.right = self._grow_tree(X_right, y_right, depth + 1)
        return node

    def fit(self, X_train, y_train):
        """
        Fit model
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self._num_features = X_train.shape[1]
        self._tree = self._grow_tree(X_train, y_train)

    def _predict(self, X):
        node = self._tree
        while node.left:
            if X[node.feature_index] < node.threshold:
                node = node.left
            else:
                node = node.right
        return node.predicted

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        return [self._predict(i) for i in X_test]

    def _importance(self, node):
        imp = [0 for _ in range(self._num_features)]
        if node.left.left:
            imp = [a + b for (a, b) in zip(self._importance(node.left), imp)]
        if node.right.left:
            imp = [a + b for (a, b) in zip(self._importance(node.right), imp)]
        imp[node.feature_index] += (node.num_samples / self._tree.num_samples) * \
                                   (node.metric - ((node.left.num_samples / node.num_samples) * node.left.metric +
                                                   (node.right.num_samples / node.num_samples) * node.right.metric))
        return imp

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        return self._importance(self._tree)


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
