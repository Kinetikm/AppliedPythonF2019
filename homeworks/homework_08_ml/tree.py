#!/usr/bin/env python
# coding: utf-8


import numpy as np


class Node:
    def __init__(self, left_child=None, right_child=None, feature=None, mark=None, val=None):
        self.left_child = left_child
        self.right_child = right_child
        self.val = val
        self.feature = feature
        self.mark = mark


class Tree:
    def __init__(self, max_depth, min_samples_leaf, criterion='mse'):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        self.criterion = criterion
        self.max_depth = max_depth
        self.depth = 0
        self.min_samples_leaf = min_samples_leaf
        self.num_feature = 0
        self.feature_imp = 0
        self.val_feature = 0
        self.threshold = 0
        self.tree = None

    def filltree(self, table):
        """
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """

        if self.depth == self.max_depth or table.shape[0] < 2 * self.min_samples_leaf:
            return Node(val=np.mean(table[:, -1]))
        else:
            max_IG = -1
            index = -1
            for feature in range(table.shape[1] - 1):
                tab_sort = table[table[:, feature].argsort()]
                y_sort = tab_sort[:, -1]
                for idx in range(self.min_samples_leaf, table.shape[0]-self.min_samples_leaf):
                    y1 = y_sort[:idx].reshape((-1, 1))
                    y2 = y_sort[idx:].reshape((-1, 1))
                    if self.IG(y1, y2) > max_IG:
                        max_IG = self.IG(y1, y2)
                        self.num_feature = feature
                        index = idx
                        self.threshold = (tab_sort[idx, feature] + tab_sort[idx+1, feature])/2

            table = table[table[:, self.num_feature].argsort()]
            self.feature_imp[self.num_feature] += 1
            self.depth += 1

            left_child = self.filltree(table[:index, :])
            right_child = self.filltree(table[index:, :])
            return Node(left_child, right_child, self.num_feature, self.threshold)

    def fit(self, X_train, y_train):
        self.feature_imp = np.zeros(X_train.shape[1])
        table = np.hstack((X_train, y_train.reshape((-1, 1))))
        self.tree = self.filltree(table)

    def metrics(self, x):
        if self.criterion == 'mse':
            return x.var()
        if self.criterion == 'mae':
            return 1/len(x) * np.sum(abs(x - x.mean()))

    def IG(self, y1, y2):
        y = np.vstack((y1, y2))
        return self.metrics(y) - len(y1)/len(y) * self.metrics(y1) - len(y2)/len(y) * self.metrics(y2)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_pred = np.zeros(X_test.shape[0])
        for i in range(X_test.shape[0]):
            node = self.tree
            while node.feature is not None:
                if X_test[i, node.feature] <= node.mark:
                    node = node.left_child
                else:
                    node = node.right_child
            y_pred[i] = node.val
        return y_pred

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        return self.feature_imp


class TreeRegressor(Tree):
    def __init__(self, max_depth=None, min_samples_leaf=1, criterion='mse'):
        """
        :param criterion: method to determine splits, 'mse' or 'mae'
        """
        super().__init__(max_depth, min_samples_leaf, criterion)


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
