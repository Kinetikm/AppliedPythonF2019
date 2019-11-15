#!/usr/bin/env python
# coding: utf-8

from collections import deque
import numpy as np
import time


def get_proba(sample):
    # возвращает вероятность единичек!
    return len(sample[sample == 1]) / len(sample)


def gini(target_sample):
    # вероятность состояния 1 (1 класс)
    p_one = target_sample[target_sample == 1].shape[0] / target_sample.shape[0]
    return 1 - p_one ** 2 - (1 - p_one) ** 2


def entropy(target_sample):
    # вероятность состояния 1 (1 класс)
    p_one = target_sample[target_sample == 1].shape[0] / target_sample.shape[0]
    return -(p_one * np.log2(p_one) + (1 - p_one) * np.log2(1 - p_one))


def classify(observation, tree):
    # Если нет фичи, значит это лист
    if tree.feature is None:
        return tree.proba
    feat_val = observation[tree.feature]
    if feat_val <= tree.threshold:
        branch = tree.l_child
    else:
        branch = tree.r_child
    return classify(observation, branch)


def sort_by_column(column, sample):
    sorted_idxs = sample[:, column].argsort(axis=0)
    return sample[sorted_idxs, :]


def split_by_value(value, column, data):
    mask = data[:, column] <= value
    l_sample = data[mask]
    r_sample = data[~mask]
    return l_sample, r_sample


class DecisionTree:
    def __init__(self):
        self.feature = None
        self.threshold = None
        self.score = None
        self.proba = None
        self.l_child = None
        self.r_child = None


class Tree:
    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        self.criterion = gini if criterion.lower() == 'gini' else entropy
        self.max_depth = max_depth if max_depth else -1
        self.min_samples_leaf = min_samples_leaf

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        data = np.c_[X_train, y_train]

        self.n_objects = X_train.shape[0]
        self.n_features = X_train.shape[1]
        self.tree_ = DecisionTree()
        self.build_tree(data, self.tree_)

    def build_tree(self, sample, node, depth=1):
        target = sample[:, -1]
        node.score = self.criterion(target)
        is_leaf = (node.score == 0 or
                   (depth == self.max_depth and self.max_depth != -1) or
                   sample.shape[0] < 2 * self.min_samples_leaf)
        if is_leaf:
            node.proba = get_proba(target)
            return

        best_gain, l_samp, r_samp, best_criteria = self.get_best_params(sample, node.score)

        if best_gain > 0:
            node.feature = best_criteria[0]
            node.threshold = best_criteria[1]

            node.l_child = DecisionTree()
            node.r_child = DecisionTree()

            self.build_tree(l_samp, node.l_child, depth=depth + 1)
            self.build_tree(r_samp, node.r_child, depth=depth + 1)

            node.node_importance = sample.shape[0] / self.n_objects * best_gain
        else:
            node.proba = get_proba(target)

    def get_best_params(self, sample, node_score):
        columns_number = sample.shape[1]
        best_gain = 0.0
        # -1 так как последняя колонка - target
        for col in range(columns_number - 1):
            sample = sort_by_column(col, sample)
            u, indices = np.unique(sample[:, col], return_index=True)
            for i in range(len(indices) - 1):
                idx = indices[i]
                idx_next = indices[i + 1]
                value = sample[idx, col]

                target_curr = sample[idx, -1]
                target_next = sample[idx_next, -1]
                # считаем IG только при переходе через класс
                if target_next != target_curr:
                    l_sample, r_sample = split_by_value(value, col, sample)
                    bad_split = (l_sample.shape[0] < self.min_samples_leaf or r_sample.shape[0] < self.min_samples_leaf)
                    info_gain = self.get_gain(l_sample, r_sample, node_score) if not bad_split else 0.0

                    if info_gain > best_gain:
                        best_gain = info_gain
                        best_l_samp = l_sample
                        best_r_samp = r_sample
                        best_criteria = (col, value)

        return best_gain, best_l_samp, best_r_samp, best_criteria

    def get_gain(self, l, r, score):
        weight = l.shape[0] / (l.shape[0] + r.shape[0])
        l_score = self.criterion(l[:, -1])
        r_score = self.criterion(r[:, -1])
        return score - weight * l_score - (1 - weight) * r_score

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_pred = np.empty(X_test.shape[0])
        # попробовать векторайзером еще!
        for row in range(X_test.shape[0]):
            y_pred[row] = int(classify(X_test[row], self.tree_) >= 0.5)
        return y_pred

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        self.feat_imp = np.empty(self.n_features)
        stack = deque()
        stack.appendleft(self.tree_)
        while stack:
            tree = stack.popleft()
            if tree.l_child:
                stack.appendleft(tree.l_child)
            if tree.r_child:
                stack.appendleft(tree.r_child)
            if tree.feature is not None:
                self.feat_imp[tree.feature] += tree.node_importance
        self.feat_imp = self.feat_imp / np.sum(self.feat_imp)
        return self.feat_imp


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
        y_pred = np.empty(X_test.shape[0])
        for row in range(X_test.shape[0]):
            y_pred[row] = classify(X_test[row], self.tree_)
        return y_pred
