#!/usr/bin/env python
# coding: utf-8


import numpy as np

# Классификация


class Tree:

    class Node:
        def __init__(self, feature_idx=None, treshhold=None, left=None,
                     right=None, feature_importance=None, leaf=False, parts=None):
            self.left = left
            self.right = right
            self.leaf = leaf
            self.feature_idx = feature_idx
            self.treshhold = treshhold
            self.feature_importance = feature_importance
            self.parts = parts

            if self.leaf != bool(self.parts is not None):
                raise ValueError(
                    "cant use leaf without parts and xor this condition")

            return

        def predict(self, x):
            if self.leaf:
                return self.parts

            if self.treshhold > x[self.feature_idx]:
                return self.left.predict(x)

            return self.right.predict(x)

    def __init__(self, criterion, max_depth, min_samples_leaf):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """

        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf

        return

    def gain(self, left_enth, right_enth, enthropy=None,
             len_left=None, len_right=None):
        return enthropy - (len_left * left_enth + len_right * right_enth) / (len_left + len_right)

    def split(self, XY, depth=0, enthropy=None):
        print(depth)
        if depth >= self.max_depth:
            return self.Node(leaf=True, parts=self.get_parts(XY[:, -1]))
        depth += 1

        if enthropy is None:
            enthropy = self.get_enthropy_from_y(XY[:, -1])

        XY_n_samples = len(XY)

        gain = 0
        best_feature = 0
        best_feature_row = 0
        best_enthropy_left = 0
        best_enthropy_right = 0
        treshold = 0
        XY_sorted_by_best_feature = XY

        for feature_idx in range(self.n_features):
            XY = np.array(sorted(XY, key=lambda x: x[feature_idx]))

            y_cur = XY[0, -1]
            for idx in range(self.min_samples_leaf, XY_n_samples - self.min_samples_leaf):

                left_enthropy = self.get_enthropy_from_y(XY[:idx, -1])
                right_enthropy = self.get_enthropy_from_y(XY[idx:, -1])
                new_gain = self.gain(left_enthropy, right_enthropy, enthropy=enthropy,
                                     len_left=idx+1, len_right=XY_n_samples-idx-1)
                if gain < new_gain:
                    gain = new_gain
                    best_enthropy_left = left_enthropy
                    best_enthropy_right = right_enthropy
                    best_feature = feature_idx
                    best_feature_row = idx
                    treshold = (XY[idx, feature_idx] +
                                XY[idx - 1, feature_idx]) / 2
                    XY_sorted_by_best_feature = XY

        # или мало данных или только увеличивается энтропия
        if gain == 0:
            return self.Node(leaf=True, parts=self.get_parts(XY[:, -1]))

        left_node = self.split(XY_sorted_by_best_feature[:best_feature_row], depth=depth,
                               enthropy=best_enthropy_left)
        right_node = self.split(XY_sorted_by_best_feature[best_feature_row:], depth=depth,
                                enthropy=best_enthropy_right)

        feature_importance = (XY_n_samples / self.n_samples) * gain
        return self.Node(feature_idx=best_feature, treshhold=treshold,
                         leaf=False, left=left_node, right=right_node,
                         feature_importance=feature_importance)

    def get_enthropy_from_y(self, y):
        parts = self.get_parts(y)
        return self.get_enthropy(parts)

    def get_parts(self, Y):
        '''
        Получаем распределение по классам
        Хотя, возможно, это стоило бы отнести не в базоывй класс,
        а в класс классификатора
        '''
        res = np.zeros_like(self.classes, dtype=float)
        for i, yclass in enumerate(self.classes):
            res[i] = len(Y[Y == yclass]) / Y.shape[0]
        return res

    def fit(self, X_train, y_train):
        """
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """

        self.n_samples, self.n_features = X_train.shape
        self.classes = np.unique(y_train)  # он и сортирует тоже

        XY = np.append(X_train, np.reshape(y_train, (-1, 1)), axis=1)
        self.tree = self.split(XY)

        return

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """

        res = np.zeros((X_test.shape[0],))

        for i, x in enumerate(X_test):
            res[i] = np.argmax(self.tree.predict(x))

        return res

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
        raise NotImplementedError


class TreeClassifier(Tree):
    AVAILABLE_CRITERION = ['gini', 'entropy']

    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'gini' or 'entropy'
        """

        if criterion not in self.AVAILABLE_CRITERION:
            raise ValueError("Unknown criterion value: ", criterion)

        super().__init__(criterion, max_depth, min_samples_leaf)

        return

    # то, что обозначалось I(s) в ноутбуке
    def get_enthropy(self, parts):
        if self.criterion == 'gini':
            return 1 - (parts ** 2).sum()
        elif self.criterion == 'enthropy':
            return - np.nansum((parts * np.log2(parts)), axis=1)
        else:
            # вот тут линтер подсказал, а раньше не замечал, потому что нет тестов на этот кейс
            raise ValueError("Unknown criterion value: ", self.criterion)

        return

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """

        res = np.zeros((X_test.shape[0], len(self.classes)))

        for i, x in enumerate(X_test):
            res[i] = self.tree.predict(x)
        return res
