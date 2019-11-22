#!/usr/bin/env python
# coding: utf-8

import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split


class GradientBoosting:
    def __init__(self, n_estimators=100, learning_rate=1.0, max_depth=None,
                 min_samples_leaf=1, subsample=1.0, subsample_col=1.0):
        """
        :param n_estimators: number of trees in model
        :param learning_rate: discount for gradient step
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        :param subsample: the fraction of samples to be used for fitting the individual base learners
        :param subsample_col: the fraction of features to be used for fitting the individual base learners
        """
        self._n_trees = n_estimators
        self._lr = learning_rate
        self._max_depth = max_depth
        self._min_leafs = min_samples_leaf
        self._subsample = subsample
        self._subsample_col = subsample_col
        self._init_preds = None
        self._trees = []
        self._feat_tree = []
        self._b = []

    def _crit_grad(self, pred, y_train):
        return [2*(pred[i] - y_train[i]) for i in range(len(pred))]

    def _calc_b(self, preds, agrad, y_tr):
        chisl = sum([(y_tr[i] - preds[i]) * agrad[i] for i in range(len(agrad))])
        znam = sum([agrad[i] * agrad[i] for i in range(len(agrad))])
        return chisl / znam

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        preds = np.mean(y_train) * np.ones([y_train.shape[0]])
        a = [*range(len(preds))]
        self._init_preds = np.mean(y_train)
        for i in range(self._n_trees):

            x_tr, _, y_tr, _, preds_tr, _, a_tr, _ = train_test_split(X_train, y_train, preds, a,
                                                                      train_size=self._subsample)
            a_feat = [*range(len(x_tr[0]))]
            x_tr = x_tr.T
            if self._subsample_col != 1.0:
                x_tr_tr, _, a_feat_tr, _ = train_test_split(x_tr, a_feat, train_size=self._subsample_col)
            else:
                x_tr_tr = x_tr.copy()
                a_feat_tr = a_feat.copy()
            x_tr_tr = x_tr_tr.T
            self._feat_tree.append(a_feat_tr.copy())
            agrad = self._crit_grad(preds_tr, y_tr)
            tree = DecisionTreeRegressor(criterion='mse', max_depth=self._max_depth, min_samples_leaf=self._min_leafs)
            tree.fit(x_tr_tr, agrad)
            self._trees.append(tree)
            b = self._calc_b(preds_tr, agrad, y_tr)
            self._b.append(b)
            temp_preds = self._lr * b * tree.predict(x_tr_tr)
            for num, i in enumerate(a_tr):
                preds[i] += temp_preds[num]
        return self

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        pred = self._init_preds * np.ones([X_test.shape[0]])
        for i in range(self._n_trees):
            X_curr = X_test[:, self._feat_tree[i]]
            pred += self._lr * self._b[i] * self._trees[i].predict(X_curr)
        return pred
