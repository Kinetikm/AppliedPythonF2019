#!/usr/bin/env python
# coding: utf-8


import numpy as np


class Node:
    def __init__(self, left_child=None, right_child=None, feature=None, marker=None, value=None):
        self.left_child = left_child
        self.right_child = right_child
        self.value = value
        self.feature = feature
        self.marker = marker


class Tree:
    def __init__(self, criterion="mse", max_depth=None, min_samples_leaf=1):
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.feat_imp = None
        self.depth = None
        self.th = None
        self.tree = None
        self.num_feature = None

    def fit(self, x_train, y_train):
        self.feat_imp = 0
        self.depth = 0
        self.th = 0
        self.feat_imp = np.zeros(x_train.shape[1])
        table = np.hstack((x_train, y_train.reshape((-1, 1))))
        self.tree = self.subnode(table)

    def met(self, x):
        if self.criterion == 'mse':
            return np.mean((x - np.mean(x)) ** 2)
        else:
            return np.mean(np.abs(x - np.mean(x)))

    def gain(self, s1, s2):
        return self.met(np.vstack((s1, s2))) - (len(s1) / (len(s1) + len(s2)) * self.met(s1) +
                                                len(s2) / (len(s1) + len(s2)) * self.met(s2))

    def subnode(self, table):
        if self.depth != self.max_depth and table.shape[0] >= 2 * self.min_samples_leaf:
            self.depth += 1
            max_gain = -1
            index = -1
            for feature in range(table.shape[1] - 1):
                s_table = table[table[:, feature].argsort()]
                s_y = s_table[:, -1]
                for idx in range(self.min_samples_leaf, table.shape[0]-self.min_samples_leaf):
                    s1 = s_y[:idx].reshape((-1, 1))
                    s2 = s_y[idx:].reshape((-1, 1))
                    sec_gain = self.gain(s1, s2)
                    if sec_gain > max_gain:
                        self.th = (s_table[idx, feature] + s_table[idx + 1, feature]) / 2
                        self.num_feature = feature
                        max_gain = sec_gain
                        index = idx
            table = table[table[:, self.num_feature].argsort()]
            self.feat_imp[self.num_feature] += 1
            return Node(self.subnode(table[:index, :]), self.subnode(table[index:, :]), self.num_feature, self.th)
        else:
            return Node(value=np.mean(table[:, -1]))

    def predict(self, x_test):
        y = np.zeros(x_test.shape[0])
        for i in range(y.shape[0]):
            node = self.tree
            while node.feature is not None:
                if x_test[i, node.feature] <= node.marker:
                    node = node.left_child
                else:
                    node = node.right_child
            y[i] = node.value
        return y

    def get_feature_importance(self):
        return self.feature_imp


class TreeRegressor(Tree):
    def __init__(self, criterion='mse', max_depth=None, min_samples_leaf=1):
        super().__init__(criterion, max_depth, min_samples_leaf)


class TreeClassifier(Tree):
    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=1):
        super().__init__(criterion, max_depth, min_samples_leaf)
        raise NotImplementedError

    def predict_proba(self, X_test):
        pass
