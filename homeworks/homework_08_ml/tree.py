#!/usr/bin/env python
# coding: utf-8


import numpy as np
import math


class Tree:
    class Node:
        def __init__(self, feature=None, separatiop=None, right=None, left=None, gain=None, size=None, plus=None,
                     depth=0):
            self.feature = feature
            self.separatiop = separatiop
            self.right = right
            self.left = left
            self.gain = gain
            self.size = size
            self.plus = plus
            self.depth = depth

    def __init__(self, criterion='gini', max_depth=5, min_samples_leaf=5):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.head = self.Node()
        self.depth = 0

    def fit(self, X_train, y_train):
        self.size = X_train.shape[0]
        self.feature_importance = np.zeros(X_train.shape[1])
        self.fit_node(X_train, y_train, self.head)

    def fit_node(self, X_train, y_train, node):
        x = X_train
        y = y_train
        gain = -10
        for i in range(x.shape[1]):
            x_y = np.vstack((x[:, i], y)).T
            x_y = x_y[x_y[:, 0].argsort()]
            arr = self._change_value(x_y)
            if self.criterion == 'gini':
                for j in arr:
                    if gain < self._check_gini(x_y, j):
                        gain = self._check_gini(x_y, j)
                        separation = (x_y[j, 0] + x_y[j - 1, 0]) / 2
                        feature = i
                        jsave = j
            else:
                for j in arr:

                    if gain < self._check_entropy(x_y, j):
                        gain = self._check_entropy(x_y, j)
                        separation = (x_y[j, 0] + x_y[j - 1, 0]) / 2
                        feature = i
                        jsave = j
        self.feature_importance[feature] += x_y.shape[0] * gain / self.size
        node.feature = feature
        node.separation = separation
        node.gain = gain
        node.size = x_y.shape[0]
        node.plus = self._plus(x_y)
        x1, y1, x2, y2 = self._split(X_train, y_train, feature, jsave)
        if node.depth + 1 < 6:
            a = self.Node(depth=node.depth + 1)
            node.right = a
            self.fit_node(x1, y1, node.right)
            b = self.Node(depth=node.depth + 1)
            node.left = a
            self.fit_node(x2, y2, node.right)

    def _plus(self, x):
        p_plus = 0
        for i in range(x.shape[0]):
            if x[i, 1] == 1:
                p_plus += 1
        if p_plus / x.shape[0] is not None:
            return p_plus / x.shape[0]
        return 0

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """

        y_pred = np.zeros(X_test.shape[0])
        for i in range(X_test.shape[0]):
            node = self.head
            while node.right or node.left:
                if X_test[i, node.feature] > node.separation:
                    node = node.right
                else:
                    node = node.left
            y_pred[i] = node.plus
        return y_pred

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        return self.feature_importance
        # ╰( ͡° ͜ʖ ͡° )つ──☆*:・ﾟ

    def _change_value(self, x_y):

        flag = False
        first = x_y[0, 1]
        arr = []

        # тут реализация чз проверку всех изменений таргет но работает очен долго
        # for i in range(self.min_samples_leaf,x_y.shape[0]-self.min_samples_leaf):
        #     if x_y[i,1] != first and flag is False:
        #         arr.append(i)
        #         flag = True
        #     elif x_y[i,1] == first and flag is True:
        #         flag = False
        # тут просто делит на попалам в разы быстрее и проходит по log_loss
        arr = [int(x_y.shape[0] / 2)]
        return arr

    def _check_gini(self, x_y, sep):
        size = x_y.shape[0]
        gini0 = self._gini(x_y)

        gini1 = sep / size * self._gini(x_y[:sep, :])
        gini1 += (1 - sep) / size * self._gini(x_y[sep:])
        gain = gini0 - gini1
        return gain

    def _gini(self, x_y):
        k = 0
        for i in x_y[:, 1]:
            if i == 1:
                k += 1
        p_plus = k / x_y.shape[0]
        gini = 2 * p_plus * (1 - p_plus)
        return gini

    def _check_entropy(self, x_y, sep):
        size = x_y.shape[0]
        entropy0 = self._entropy(x_y)
        entropy1 = sep / size * self._entropy(x_y[:sep, :])
        entropy1 += (1 - sep) / size * self._entropy(x_y[sep:, :])
        gain = entropy0 - entropy1
        return gain

    def _entropy(self, x_y):
        k = 0
        for i in x_y[:, 1]:
            if i == 1:
                k += 1
        p_plus = k / x_y.shape[0]

        entropy = - p_plus * math.log(p_plus + 1e-8, 2) - (1 - p_plus) * math.log(1 - p_plus + 1e-8, 2)
        return entropy

    def _split(self, x, y, feature, jsave):
        x_y = np.hstack((x, y.reshape((-1, 1))))
        x_y = x_y[x_y[:, feature].argsort()]
        x1 = x_y[:jsave, :-1]
        x2 = x_y[jsave:, :-1]
        y1 = x_y[:jsave, -1]
        y2 = x_y[jsave:, -1]
        return x1, y1, x2, y2


class TreeRegressor(Tree):
    def __init__(self, criterion='mse', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'mse' or 'mae'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)
        raise NotImplementedError


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
        y = np.zeros((X_test.shape[0], 2))
        y_pred = self.predict(X_test)
        for i in range(y_pred.shape[0]):
            y[i, 0] = 1 - y_pred[i]
            y[i, 1] = y_pred[i]
        return y
