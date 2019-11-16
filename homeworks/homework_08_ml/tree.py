#!/usr/bin/env python
# coding: utf-8


import numpy as np


class Tree:
    def __init__(self, criterion, max_depth, min_samples_leaf, tree_type):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.value = None
        self.left, self.right = None, None
        self.tree_type = tree_type

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.eps = 1e-3
        N, features = X_train.shape
        S_0 = self.entropy(y_train)
        if S_0 < self.eps or self.max_depth == 0:
            self.value = self.get_value(y_train)
            return

        else:
            feature = None
            best_dS = 0
            for i in range(features):
                data = np.argsort(X_train[:, i])
                N_board = 0
                for n in range(
                        self.min_samples_leaf + 1,
                        N - self.min_samples_leaf):

                    if y_train[data[n - 1]] == y_train[data[n]]:
                        continue

                    left_entropy = self.entropy(y_train[data[0:n]])
                    right_entropy = self.entropy(y_train[data[n:N]])

                    dS = S_0 - (left_entropy * (n / N) +
                                right_entropy * (N - n) / N)

                    if dS > best_dS:
                        best_dS = dS
                        feature, board = i, n
                    N_board += 1

            if feature is None:
                self.value = self.get_value(y_train)
                return
        self.feature = feature
        self.board = X_train[board, self.feature]

        data = np.argsort(X_train[:, feature])

        self.left = self.tree_type(
            self.criterion,
            self.max_depth - 1,
            self.min_samples_leaf)
        self.right = self.tree_type(
            self.criterion,
            self.max_depth - 1,
            self.min_samples_leaf)

        self.left.fit(X_train[data[0:board]], y_train[data[0:board]])
        self.right.fit(X_train[data[board:N]], y_train[data[board:N]])

        pass

    def one_predict(self, x):
        if self.value is None:
            direction = False if x[self.feature] < self.board else True
            if direction:
                return self.right.one_predict(x)
            else:
                return self.left.one_predict(x)
        else:
            return self.value

    def predict(self, X_test):
        return np.array([self.one_predict(X_test[i, :])
                         for i in range(X_test.shape[0])])

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        pass


class TreeRegressor(Tree):
    def __init__(self, criterion='mse', max_depth=np.inf, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'mse' or 'mae'
        """
        super().__init__(criterion, max_depth, min_samples_leaf, TreeRegressor)

    def entropy(self, y):
        return ((y - y.mean()) ** 2).sum() / len(y)

    def get_value(self, y):
        return y.mean()


class TreeClassifier(Tree):
    def __init__(self, criterion='gini', max_depth=np.inf, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'gini' or 'entropy'
        """
        super().__init__(criterion, max_depth, min_samples_leaf, TreeClassifier)

    def entropy(self, y):
        H = 0
        for elem in np.unique(y):
            p = np.sum(y == elem)
            H += p * p / len(y)
        return 1 - H

    def get_value(self, y):
        p_max, value = 0, None
        unique = np.unique(y)
        for elem in unique:
            p = np.sum(y == elem)
            if p > p_max:
                p_max, value = p, elem
        return (p_max / len(y), value)

    def predict(self, X_test):
        return np.array([self.one_predict(X_test[i, :])[1]
                         for i in range(X_test.shape[0])])

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        return np.array([self.one_predict(X_test[i, :])[0]
                         for i in range(X_test.shape[0])])
