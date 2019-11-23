#!/usr/bin/env python
# coding: utf-8

import numpy as np
from sklearn.tree import DecisionTreeRegressor


class GradientBoosting:
    def __init__(
        self,
        n_estimators=100,
        learning_rate=0.01,
        max_depth=None,
        min_samples_leaf=1,
        subsample=1.0,
        subsample_col=1.0,
    ):
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
        self.trees = []
        self.features = []

    def _get_random_sample(self, x):
        s, s_col = x.shape
        sample_idx = np.random.choice(s, int(self.subsample * s))
        sample_col_idx = np.random.choice(s_col, int(self.subsample_col * s_col))
        return sample_idx, sample_col_idx

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        self.y = y_train

        y_train = y_train.reshape(-1, 1)

        sample_idx, _ = self._get_random_sample(X_train)

        prediction = np.mean(y_train[sample_idx, :])

        for i in range(self.n_estimators):
            sample_idx, sample_col_idx = self._get_random_sample(X_train)

            y_fit = y_train[sample_idx, :]
            X_fit = X_train[sample_idx, :][:, sample_col_idx]

            if not i:
                anti_grad = y_fit
            else:
                anti_grad = y_fit - prediction.reshape(-1, 1)

            tree = DecisionTreeRegressor(
                criterion="mse",
                max_depth=self.max_depth,
                min_samples_leaf=self.min_samples_leaf,
            )

            tree.fit(X_fit, anti_grad)

            self.trees.append(tree)
            self.features.append(sample_col_idx)

            prediction += self.learning_rate * tree.predict(X_fit)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        prediction = np.mean(self.y)

        for i in range(self.n_estimators):
            prediction += self.learning_rate * self.trees[i].predict(X_test[:, self.features[i]])

        return prediction
