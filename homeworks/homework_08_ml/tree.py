#!/usr/bin/env python
# coding: utf-8


import numpy as np


class Tree:
    def __init__(self, criterion, max_depth, min_samples_leaf=1):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.fitted_tree = None
        self.unique_values = None
        self.feature_importances = None
        self.data_shape = None

    def fit(self, X_train, y_train):
        data = np.hstack((X_train, y_train.reshape(-1, 1)))
        self.feature_importances = np.zeros(X_train.shape[1])
        self.data_shape = X_train.shape
        self.fitted_tree = self.build_tree(data)

    def build_tree(self, data, depth=0):
        if depth == 0:
            self.unique_values = np.unique(data[:, -1])
        if self.max_depth and depth == self.max_depth:
            return self.get_probs(data[:, -1])
        if self.is_pure(data[:, -1]):
            return self.get_probs(data[:, -1])
        else:
            depth += 1
            split_column, split_value = self.find_best_split(data)
            if split_column is None:
                return self.get_probs(data[:, -1])
            data_true, data_false = self.split_data(data, split_column, split_value)
            tree = {(split_column, split_value): []}
            true_branch = self.build_tree(data_true, depth)
            false_branch = self.build_tree(data_false, depth)
            tree[(split_column, split_value)].append(true_branch)
            tree[(split_column, split_value)].append(false_branch)
        return tree

    def is_pure(self, data):
        unique = np.unique(data)
        if len(unique) == 1:
            return True
        else:
            return False

    def get_probs(self, data):
        values, counts = np.unique(data, return_counts=True)
        probs = np.zeros_like(self.unique_values)
        d = dict(zip(values, counts))
        for i in range(len(self.unique_values)):
            if self.unique_values[i] not in values:
                continue
            else:
                probs[i] = d[self.unique_values[i]] / counts.sum()
        return probs

    def predict_example(self, example, tree):
        question = tuple(tree.keys())[0]
        col_index, value = question[0], question[1]
        if (value.dtype == np.float64 or value.dtype == np.int64): 
            if example[col_index] >= value:
                answer = tree[question][0]
            else:
                answer = tree[question][1]
        else:
            if example[col_index] == value:
                answer = tree[question][0]
            else:
                answer = tree[question][1]
        if not isinstance(answer, dict):
            return answer
        else:
            return self.predict_example(example, answer)

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        if any(self.feature_importances):
            return self.feature_importances
        else:
            raise NotFittedError

    def get_potential_splits(self, data):
        potential_splits = {}
        for col_index in range(data.shape[1]-1):
            potential_splits[col_index] = []
            values = np.unique(data[:, col_index])
            if (values.dtype == np.float64 or values.dtype == np.int64): 
                for i in range(1, len(values)):
                    split = (values[i] + values[i-1]) / 2
                    potential_splits[col_index].append(split)
            else:
                potential_splits[col_index].append(values)
        return potential_splits

    def split_data(self, data, col_index, value):
        if (data[:, col_index].dtype == np.float64 or data[:, col_index].dtype == np.int64):
            data_true = data[data[:, col_index] >= value]
            data_false = data[data[:, col_index] < value]
            return data_true, data_false
        else:
            data_true = data[data[:, col_index] == value]
            data_false = data[data[:, col_index] != value]
            return data_true, data_false

    def entropy(self, data):
        classes = data[:, -1]
        vals, counts = np.unique(classes, return_counts=True)
        probs = counts / counts.sum()
        s = -sum(probs * np.log2(probs))
        return s

    def gini(self, data):
        classes = data[:, -1]
        vals, counts = np.unique(classes, return_counts=True)
        probs = counts / counts.sum()
        g = 1 - (probs ** 2).sum()
        return g

    def find_best_split(self, data):
        potential_splits = self.get_potential_splits(data)
        max_gain = -999
        if self.criterion == 'gini':
            initial_impurity = self.gini(data)
        else:
            initial_impurity = self.entropy(data)
        best_split_column = None
        best_split_value = None
        for col_index in potential_splits:
            for value in potential_splits[col_index]:
                data_true, data_false = self.split_data(data, col_index, value)
                if len(data_true) < self.min_samples_leaf or len(data_false) < self.min_samples_leaf:
                    continue
                if self.criterion == 'gini':
                    impurity_1, impurity_2 = self.gini(data_true), self.gini(data_false)
                    gain = initial_impurity - (len(data_true) * impurity_1 / len(data) +
                                             len(data_false) * impurity_2 / len(data))
                else:
                    impurity_1, impurity_2 = self.entropy(data_true), self.entropy(data_false)
                    gain = initial_impurity - (len(data_true) * impurity_1 / len(data) +
                                             len(data_false) * impurity_2 / len(data))
                if gain > max_gain:
                    best_split_column = col_index
                    best_split_value = value
                    max_gain = gain
        if best_split_column is not None:
            self.feature_importances[best_split_column] += (len(data) / self.data_shape[0]) * max_gain
            return best_split_column, best_split_value
        else:
            return None, None

class TreeClassifier(Tree):
    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'gini' or 'entropy'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)

    def predict_proba(self, X_test):
        """
        Predict probability using model
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        if self.fitted_tree:
            y_proba = np.apply_along_axis(self.predict_example, 1, X_test, self.fitted_tree)
        else:
            raise NotFittedError
        return y_proba

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_proba = self.predict_proba(X_test)
        y_pred = self.unique_values[np.argmax(y_proba, axis=1)]
        return y_pred

class TreeRegressor(Tree):
    def __init__(self, criterion='mse', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'mse' or 'mae'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)
        raise NotImplementedError

