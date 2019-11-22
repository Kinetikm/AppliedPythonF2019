#!/usr/bin/env python
# coding: utf-8
import numpy as np
from sklearn.tree import DecisionTreeRegressor


class MetaAlgorithm:
    def __init__(self, n_estimators, learning_rate):
        self.n_estimators = n_estimators
        self.ensebmle = []
        self.learning_rate = learning_rate
        self.w = []

    def add_model(self, model):
        self.ensebmle.append(model)

    def predict(self, X):
        # предикт константной модели
        y_hat = np.full((X.shape[0], 1), self.const)

        for (i, tree) in enumerate(self.ensebmle):
            y_hat += tree.predict(X).reshape(-1, 1) * self.w[i]

        return y_hat / (len(self.ensebmle) + 1)


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
        self.meta = MetaAlgorithm(self.n_estimators, self.learning_rate)
        self.meta.const = np.mean(y_train, axis=0)

        data = np.c_[X_train, y_train]

        for i in range(self.n_estimators):
            x_batch, y_batch = self.get_subsample(data)

            meta_pred = self.meta.predict(x_batch)
            residuals = y_batch - meta_pred

            tree = DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf)
            tree = tree.fit(x_batch, residuals)

            self.meta.add_model(tree)

            tree_pred = tree.predict(x_batch).reshape(-1, 1)

            b = ((residuals.T @ tree_pred) / (tree_pred.T @ tree_pred)).flatten()[0]
            self.meta.w.append(self.learning_rate * b)

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
