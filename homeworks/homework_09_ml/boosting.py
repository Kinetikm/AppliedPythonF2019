#!/usr/bin/env python
# coding: utf-8
import numpy as np
from sklearn.tree import DecisionTreeRegressor


class MetaAlgorithm:
    def __init__(self, n_estimators, const_pred):
        self.n_estimators = n_estimators
        self._ensebmle = []
        self.const_pred = const_pred
        self._n_models = 1

    def add_model(self, model, weight):
        self._ensebmle.append((model, weight))
        self._n_models += 1

    def predict(self, X):
        # constant model prediction
        y_hat = np.full((X.shape[0], 1), self.const_pred)

        for model, weight in self._ensebmle:
            y_hat += model.predict(X).reshape(-1, 1) * weight

        return y_hat / self._n_models


class GradientBoosting:
    def __init__(self, n_estimators=100, learning_rate=1.0, max_depth=None,
                 min_samples_leaf=3, subsample=1.0, subsample_col=1.0):
        """
        :param n_estimators: number of trees in model
        :param learning_rate: discount for gradient step
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        :param subsample: the fraction of samples to be used for fitting the individual base learners
        :param subsample_col: the fraction of features to be used for fitting the individual base learners
        """
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.subsample = subsample
        self.subsample_col = subsample_col

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.meta = MetaAlgorithm(self.n_estimators, const_pred=np.mean(y_train))

        data = np.c_[X_train, y_train]

        for i in range(self.n_estimators):
            x_batch, y_batch = self.get_subsample(data)

            meta_pred = self.meta.predict(x_batch)
            residuals = y_batch - meta_pred

            tree = DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf)
            tree = tree.fit(x_batch, residuals)

            tree_pred = tree.predict(x_batch).reshape(-1, 1)
            b = self.get_algorithm_weight(residuals, tree_pred)

            self.meta.add_model(tree, b)

    def get_algorithm_weight(self, residuals, alg_pred):
        # formula acceptable only for MSE
        weight = (residuals.T @ alg_pred) / (alg_pred.T @ alg_pred)
        weight = weight.flatten()[0]
        return self.learning_rate * weight

    def get_subsample(self, data):
        # data[:,-1] - target
        n_feat = data.shape[1] - 1
        n_obj = data.shape[0]

        col_lim = int(self.subsample_col * n_feat)
        obj_lim = int(self.subsample * n_obj)

        idx_feat = np.arange(n_feat)
        idx_obj = np.arange(n_obj)

        np.random.shuffle(idx_feat)
        np.random.shuffle(idx_obj)

        obj_sub = data[idx_obj[:obj_lim], :]

        target = obj_sub[:, -1]
        feat_sub = obj_sub[:, idx_feat[:col_lim]]
        return feat_sub, target[:, np.newaxis]

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        return self.meta.predict(X_test)
