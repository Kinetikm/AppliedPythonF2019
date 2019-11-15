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
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.left = None
        self.right = None
        self.best_feature = None
        self.value = None
        self.val_feature = None
        self.feature_importance = None
        self.n_features = None
        self.amount = None
        self.criterion = criterion  # по варианту у мена классификатор, но я решил и регрессор сделать для красоты
        if not (criterion == np.array(['gini', 'entropy', 'mse', 'mae'])).any():
            raise ValueError

    @staticmethod
    def gini(y, value):
        y_one = y.sum()
        y_zero = y.shape[0] - y_one
        return 1 - (y_one ** 2 + y_zero ** 2) / y.shape[0] ** 2

    @staticmethod
    def entropy(y, value):
        ent = 0
        y_one = y.sum()
        y_zero = y.shape[0] - y_one
        mas = list()
        mas.append(y_zero)
        mas.append(y_one)
        for i in range(2):
            attitude = mas[i] / y.shape[0]
            if attitude != 0:
                ent += attitude * np.log2(attitude)

        return (-1) * ent

    @staticmethod
    def mse(y, value):
        return ((y - value) ** 2).sum()

    @staticmethod
    def mae(y, value):
        return np.abs(y - value).sum()

    def get_error(self, y, value):
        if self.criterion == 'gini':
            return self.gini(y, value)
        elif self.criterion == 'entropy':
            return self.entropy(y, value)
        elif self.criterion == 'mse':
            return self.mse(y, value)
        elif self.criterion == 'mae':
            return self.mae(y, value)

    def get_value(self, y):
        if self.criterion == 'gini' or self.criterion == 'entropy':
            return y.sum() / y.shape[0]
        elif self.criterion == 'mse' or self.criterion == 'mae':
            return y.mean()

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.n_features = X_train.shape[1]
        self.value = self.get_value(y_train)

        error = self.get_error(y_train, self.value)
        total_error = error

        if self.max_depth <= 1:
            return

        amount = X_train.shape[0]
        if self.amount is None:
            self.amount = amount

        for feature in range(X_train.shape[1]):
            sort_ind = np.argsort(X_train[::, feature])
            for sep in range(1, amount):  # в левое поддерево всё, что меньше sep, в правое - остальное
                num_feat = sort_ind[sep]

                y_left = np.array(y_train[sort_ind][:sep])
                y_right = np.array(y_train[sort_ind][sep:])
                left_value = self.get_value(y_left)
                right_value = self.get_value(y_right)

                error_left = self.get_error(y_left, left_value)
                error_right = self.get_error(y_right, right_value)

                left_coef = sep / amount
                right_coef = 1 - left_coef

                if (error_left * left_coef + error_right * right_coef < error) \
                        and (min(sep, amount - sep) >= self.min_samples_leaf):
                    self.best_feature = feature
                    self.val_feature = X_train[num_feat, feature]
                    error = error_left * error_left + error_right * error_right

        if self.best_feature is None:
            return

        # тот самый gain
        # amount - |Si| (из лекции)
        # self.amount - общее число сэмплов |S| (из лекции)
        self.feature_importance = amount * (total_error - error) / self.amount

        self.left = Tree(self.criterion, self.max_depth - 1, self.min_samples_leaf)
        self.right = Tree(self.criterion, self.max_depth - 1, self.min_samples_leaf)

        self.left.amount = self.amount
        self.right.amount = self.amount

        ind_left = X_train[::, self.best_feature] < self.val_feature
        ind_right = X_train[::, self.best_feature] >= self.val_feature

        self.left.fit(X_train[ind_left], y_train[ind_left])
        self.right.fit(X_train[ind_right], y_train[ind_right])

    def _predict_one(self, sample):
        if self.best_feature is None:
            return self.value
        if sample[self.best_feature] < self.val_feature:
            return self.left._predict_one(sample)
        return self.right._predict_one(sample)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_test = np.zeros((X_test.shape[0],))
        for i in range(X_test.shape[0]):
            y_test[i] = self._predict_one(X_test[i])

        if self.criterion == 'gini' or self.criterion == 'entropy':
            return y_test.round()
        return y_test

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        mas_total_errors = np.zeros((self.n_features,))
        if self.best_feature is None:
            return mas_total_errors
        left_mas = self.left.get_feature_importance()
        right_mas = self.right.get_feature_importance()
        mas_total_errors[self.best_feature] += self.feature_importance
        mas_total_errors += left_mas + right_mas
        return mas_total_errors


class TreeRegressor(Tree):
    def __init__(self, criterion='mse', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'mse' or 'mae'
        """
        if not (criterion == np.array(['mse', 'mae'])).any():
            raise ValueError

        super().__init__(criterion, max_depth, min_samples_leaf)

    def get_error(self, y, value):
        if self.criterion == 'mse':
            return self.mse(y, value)
        elif self.criterion == 'mae':
            return self.mae(y, value)

    def get_value(self, y):
        return y.mean()


class TreeClassifier(Tree):
    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'gini' or 'entropy'
        """
        if not (criterion == np.array(['gini', 'entropy'])).any():
            raise ValueError
        super().__init__(criterion, max_depth, min_samples_leaf)

    def get_error(self, y, value):
        if self.criterion == 'gini':
            return self.gini(y, value)
        elif self.criterion == 'entropy':
            return self.entropy(y, value)

    def get_value(self, y):
        return y.sum() / y.shape[0]

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        y_test = np.zeros((X_test.shape[0],))
        for i in range(X_test.shape[0]):
            y_test[i] = self._predict_one(X_test[i])

        return y_test
