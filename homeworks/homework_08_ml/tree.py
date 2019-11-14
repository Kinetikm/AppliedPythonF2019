#!/usr/bin/env python
# coding: utf-8


import numpy as np


class Tree:
    def __init__(self, criterion, max_depth, min_samples_leaf):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples = min_samples_leaf
        self.left_child = None
        self.right_child = None

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_pred = np.zeros((X_test.shape[0], self.class_num))
        for i in range(X_test.shape[0]):
            y_pred[i] = self.predict_row(X_test[i])
        return y_pred.argmax(axis=1)

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        if self.right_child and self.left_child:
            return self.imp + self.right_child.get_feature_importance + self.right_child.get_feature_importance
        else:
            return self.imp


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

    def fit(self, X_train, y, n_samples=None, depth=0):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y: target values for training data
        :return: None
        """

        if depth == 0:
            n_samples = X_train.shape[0]
        y = y.astype(int)
        self.class_num = len(np.unique(y))
        y =y.reshape((y.shape[0], 1))
        self.imp = np.zeros((1, X_train.shape[1]))
        print('Вы пробудили рекурсивного кракена')
        print(depth)
        if (X_train.shape[0] > self.min_samples) and (self.max_depth is None or depth < self.max_depth):
            row, col, value, gain_max = self.find_best_split(X_train, y)
            self.column_index = col
            self.threshold = value
            self.imp[0, col] += X_train.shape[1] / n_samples * gain_max
            matrix = np.hstack((X_train, y))
            matrix = matrix[matrix[:, col].argsort()]
            xl = matrix[:row, :-1]
            yl = matrix[:row, -1]
            yl = yl.reshape((yl.shape[0], 1))
            xr = matrix[row:, :-1]
            yr = matrix[row:, -1]
            yr = yr.reshape((yr.shape[0], 1))
            self.left_child = TreeClassifier(self.criterion, self.max_depth, self.min_samples)
            self.left_child.fit(xl, yl, n_samples, depth + 1)
            self.right_child = TreeClassifier(self.criterion, self.max_depth, self.min_samples)
            self.right_child.fit(xr, yr, n_samples, depth + 1)
        else:
            self.proba = np.zeros((1, self.class_num))
            unique, counts = np.unique(y, return_counts=True)
            dct = dict(zip(unique, counts))
            i = 0
            for key in dct.keys():
                self.proba[0, i] = dct[key] / y.shape[0]
                i += 1

    def find_best_split(self, x, y):
        matrix = np.hstack((x, y))
        S = self.get_entropy(y)
        print (S)
        gain_max = 0
        row = 0
        col = 0
        for i in range(x.shape[1]):  # в лоб ищем наибольшую убыль энтропии
            print(i)
            for j in range(x.shape[0]):
                matrix = matrix[matrix[:, i].argsort()]
                gain = S
                gain -= (j / matrix.shape[0]) * self.get_entropy(matrix[:j, -1]) + (y.shape[0] - j) / y.shape[
                    0] * self.get_entropy(matrix[j:, -1])
                if gain > gain_max:
                    gain_max = gain
                    row = j
                    col = i
        value = x[row, col]
        return (row, col, value, gain_max)

    def get_entropy(self, y):
        entropy = 0
        unique, counts = np.unique(y, return_counts=True)
        dct = dict(zip(unique, counts))
        if self.criterion == 'entropy':
            for key in dct.keys():
                p = dct[key] / y.shape[0]
                entropy += p * np.log(p)
        elif self.criterion == 'gini':
            for key in dct.keys():
                entropy += (dct[key] / y.shape[0]) ** 2
            entropy = 1 - entropy
        return entropy

    def predict_row(self,row):
        if self.left_child and self.right_child:
            if row[self.column_index] < self.threshold:
                return self.left_child.predict_row(row)
            else:
                return self.right_child.predict_row(row)
        return self.proba

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        y_pred = np.zeros((X_test.shape[0], self.class_num))
        for i in range(X_test.shape[0]):
            y_pred[i] = self.predict_row(X_test[i])
        return y_pred
