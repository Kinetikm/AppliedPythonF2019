#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
from collections import Counter


class Tree:
    class Node:
        def __init__(self, depth):
            self.right = None
            self.left = None
            self.condition = None
            self.depth = depth

    class Leaf:
        def __init__(self, probs, n_samples):
            self.probs = probs
            self.n_samples = n_samples

    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=10):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion

    def imp(self, p):
        if self.criterion == 'missclass':
            return 1 - p.max(axis=0)
        if self.criterion == 'gini':
            return 1 - (p ** 2).sum(axis=0)
        if self.criterion == 'entropy':
            return -np.nansum((p*np.log2(p)), axis=0)

    def prob(self, clarray):
        # возвращает вероятность класса, например, [0.1, 0.9, 0.3, 0]
        # то есть на 0 позиции вероятность класса 0
        # на 1 вероятность класса 1 и т.д
        # если класс не встретился, то его вероятность равна 0
        return np.array([len(clarray[clarray == i]) / len(clarray) for i in range(self.n_classes)])

    def gain(self, samples, left_samples, right_samples):
        # в samples лежит список классов
        # аналогично в left_samples и right_samples
        p = self.prob(samples)
        lp = self.prob(left_samples)
        rp = self.prob(right_samples)
        return self.imp(p) - (len(left_samples) * self.imp(lp) + len(right_samples) * self.imp(rp)) / len(samples)

    def grow(self, data, depth=0):
        min_gain = self.imp(self.prob(data[:, -1]))
        last_class = None

        if depth == self.max_depth or data.shape[0] < 2 * self.min_samples_leaf:
            return self.Leaf(self.prob(data[:, -1]), data.shape[0])

        if min_gain == 0:
            return self.Leaf(self.prob(data[:, -1]), data.shape[0])

        for col in range(data.shape[1] - 1):
            data = data[data[:, col].argsort()]  # сортируем по заданной колонке

            for row in range(self.min_samples_leaf - 1, data.shape[0]):
                # начинаем не с 0, чтобы в листе не могло оказаться слишком мало элементов
                if last_class == data[row, -1]:
                    # impurance может поменяться только при переходе с одного класса на другой
                    continue

                last_class = data[row, -1]

                gain = self.gain(data[:, -1], data[0:row, -1], data[row:, -1])
                if gain < min_gain:
                    min_gain = gain
                    feature_col = col
                    feature_row = row
                    threshold = data[row, col]
                    sorted_data = data

        self.importance[feature_col] += (data.shape[0] / self.n_samples) * self.imp(self.prob(data[:, -1]))

        if depth == 0:
            self.node = self.Node(depth)
            self.node.condition = (feature_col, threshold)
            self.node.right = self.grow(sorted_data[0:feature_row], depth=depth+1)
            self.node.left = self.grow(sorted_data[feature_row:], depth=depth+1)
        else:
            node = self.Node(depth)
            node.condition = (feature_col, threshold)
            node.right = self.grow(sorted_data[0:feature_row], depth=depth+1)
            node.left = self.grow(sorted_data[feature_row:], depth=depth+1)
            return node

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.n_classes = len(np.unique(y_train))
        self.importance = np.zeros(X_train.shape[1])
        self.n_samples = X_train.shape[0]
        data = np.hstack((X_train, y_train.reshape(-1, 1)))  # присоединяем метки классов к соответствующим сэмплам
        self.grow(data)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_test = np.empty(X_test.shape[0])
        for i in range(X_test.shape[0]):
            sample = X_test[i]
            node = self.node
            while not isinstance(node, self.Leaf):
                feature_col, threshold = node.condition
                if sample[feature_col] >= threshold:
                    node = node.right
                else:
                    node = node.left
            # здесь нода уже лист
            # будем считать классом данного сэмпла тот, вероятность которого наибольшая
            y_test[i] = node.probs.argmax()

        return y_test

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        return self.importance


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
        y_test = np.empty((X_test.shape[0], self.n_classes))
        for i in range(X_test.shape[0]):
            sample = X_test[i]
            node = self.node
            while not isinstance(node, self.Leaf):
                feature_col, threshold = node.condition
                if sample[feature_col] >= threshold:
                    node = node.right
                else:
                    node = node.left
            y_test[i] = node.probs

        return y_test
