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
        self.min_samples_leaf = min_samples_leaf
        self.depth = 0
        self.mean = None
        self.param = None  # Параметр, по которому будет проводиться проверка
        self.condition_num = None  # Число, с которым будет сравниваться
        self.left = None   # False
        self.right = None  # True

    def fit(self, X_train, y_train):
        """
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        if isinstance(X_train, np.ndarray) and isinstance(y_train, np.ndarray):
            if len(X_train.shape) == 2 and len(y_train.shape) == 1:
                self.mean = np.mean(y_train)
                if self.max_depth > 1 and y_train.shape[0] > 2 * self.min_samples_leaf:
                    num_of_parameters = X_train.shape[1]
                    num_of_samples = X_train.shape[0]
                    ssr = []  # Мин суммы квадратов (модулей) отклонений для каждого параметра (squared residuals)
                    for par in range(num_of_parameters):
                        temp_data = []
                        for i in range(num_of_samples):
                            temp_data.append((X_train[i, par], y_train[i]))
                        y_par = np.asarray(sorted(temp_data, key=lambda w: w[0])[:])[:, 1]
                        splitter = 1
                        se = []  # Суммы квадратов (модулей) отклонений от среднего для параметра с наименьшим ssr
                        while splitter < num_of_samples - 1:
                            y_left = y_par[:splitter]
                            y_right = y_par[splitter:]
                            aver_left = np.mean(y_left)
                            aver_right = np.mean(y_right)
                            se_left = self.sum_of_errors(y_left, aver_left)
                            se_right = self.sum_of_errors(y_right, aver_right)
                            se.append(se_left + se_right)
                            splitter += 1
                        se = np.asarray(se)
                        ssr.append((np.argmin(se), np.min(se)))
                    split = int((min(ssr, key=lambda r: r[1])[0])) + 1  # оптимальный сплит
                    ssr = np.asarray(ssr)
                    self.param = np.argmin(ssr[:, 1])
                    x_par = sorted(X_train[:, self.param])
                    self.condition_num = (x_par[split] + x_par[split + 1]) / 2
                    self.left = Tree(self.criterion, self.max_depth - 1, self.min_samples_leaf)
                    self.right = Tree(self.criterion, self.max_depth - 1, self.min_samples_leaf)
                    left_X_train = []
                    left_y_train = []
                    right_X_train = []
                    right_y_train = []
                    for sample in range(num_of_samples):
                        if X_train[sample, self.param] < self.condition_num:
                            left_X_train.append(X_train[sample])
                            left_y_train.append(y_train[sample])
                        else:
                            right_X_train.append(X_train[sample])
                            right_y_train.append(y_train[sample])
                    left_X_train = np.asarray(left_X_train)
                    left_y_train = np.asarray(left_y_train)
                    right_X_train = np.asarray(right_X_train)
                    right_y_train = np.asarray(right_y_train)
                    self.left.fit(left_X_train, left_y_train)
                    self.right.fit(right_X_train, right_y_train)
                    self.depth = max(self.left.depth, self.right.depth) + 1
                else:
                    return
            else:
                return
        else:
            raise TypeError

    def sum_of_errors(self, a, b):
        l = len(a)
        if self.criterion == "mse":
            return np.sum((a - b) ** 2) / l
        if self.criterion == "mae":
            return np.sum(np.fabs(a - b)) / l

    def predict_one(self, x_i):
        if self.condition_num is None:
            return self.mean
        else:
            if x_i[self.param] < self.condition_num:
                return self.left.predict_one(x_i)
            elif x_i[self.param] >= self.condition_num:
                return self.right.predict_one(x_i)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        output = []
        for sample in X_test:
            output.append(self.predict_one(sample))
        return np.asarray(output)

    def print_tree(self, level=0):
        ret = "\t" * level + "mean: " + repr(self.mean) + " cond: " + repr(self.condition_num) +  \
              " param: " + repr(self.param) + "\n"
        if self.left is not None:
            ret += self.left.print_tree(level + 1)
        if self.right is not None:
            ret += self.right.print_tree(level + 1)
        return ret


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
