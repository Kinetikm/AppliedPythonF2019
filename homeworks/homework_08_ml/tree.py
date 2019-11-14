#!/usr/bin/env python
# coding: utf-8


import numpy as np
from sklearn.metrics import mean_squared_error


class Tree:
    def __init__(self, criterion, max_depth, min_samples_leaf=1):
        self.max_depth = max_depth  # максимальная глубина
        self.min_size = 1  # минимальный размер поддерева
        self.value = 0  # значение в поддереве (среднее по всем листьям)
        self.feature_idx = -1  # номер лучшего признака
        self.feature_threshold = 0  # значение лучшего признака
        self.left = None  # левый потомок
        self.right = None  # правый потомок

    def fit(self, X, y):
        self.value = y.mean()
        base_error = ((y - self.value) ** 2).sum()
        error = base_error
        flag = 0
        prev_error_left = base_error
        prev_error_right = 0
        if self.max_depth <= 1:
            return
        dim_shape = X.shape[1]
        left_value = 0
        right_value = 0
        for feat in range(dim_shape):
            idxs = np.argsort(X[:, feat])
            N = X.shape[0]
            N1, N2 = N, 0
            thres = 1
            while thres < N - 1:
                N1 -= 1
                N2 += 1
                idx = idxs[thres]
                x = X[idx, feat]
                if thres < N - 1 and x == X[idxs[thres + 1], feat]:
                    thres += 1
                    continue
                target_right = y[idxs][:thres]
                target_left = y[idxs][thres:]
                mean_right = y[idxs][:thres].mean(),
                mean_left = y[idxs][thres:].mean()
                left_shape = target_left.shape[0]
                right_shape = target_right.shape[0]
                mean_left_array = [mean_left for _ in range(left_shape)]
                mean_right_array = [mean_right for _ in range(right_shape)]
                prev_error_left = N1 / N * mean_squared_error(target_left, mean_left_array)
                prev_error_right = N2 / N * mean_squared_error(target_right, mean_right_array)
                if (prev_error_left + prev_error_right < error):
                    if (min(N1, N2) > self.min_size):
                        self.feature_idx = feat
                        self.feature_threshold = x
                        left_value = mean_left
                        right_value = mean_right
                        flag = 1
                        error = prev_error_left + prev_error_right
                thres += 1
        if self.feature_idx == -1:
            return
        a = self.max_depth - 1
        self.left = TreeRegressor(max_depth=a)
        self.left.value = left_value
        self.right = TreeRegressor(max_depth=a)
        self.right.value = right_value
        idxs_l = (X[:, self.feature_idx] > self.feature_threshold)
        idxs_r = (X[:, self.feature_idx] <= self.feature_threshold)
        self.left.fit(X[idxs_l, :], y[idxs_l])
        self.right.fit(X[idxs_r, :], y[idxs_r])


class TreeRegressor(Tree):
    def __init__(self, criterion='mse', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'mse' or 'mae'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)

    def __predict(self, x):
        if self.feature_idx == -1:
            return self.value
        if x[self.feature_idx] > self.feature_threshold:
            return self.left.__predict(x)
        else:
            return self.right.__predict(x)

    def predict(self, X):
        y = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            y[i] = self.__predict(X[i])
        return y


class TreeClassifier(Tree):
    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'gini' or 'entropy'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)
        raise NotImplementedError
