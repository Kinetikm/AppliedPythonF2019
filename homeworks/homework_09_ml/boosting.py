#!/usr/bin/env python
# coding: utf-8


import numpy as np
from sklearn.tree import DecisionTreeRegressor


class GradientBoosting:
    def __init__(self, n_estimators=100, learning_rate=1.0, max_depth=None,
                 min_samples_leaf=1, subsample=1.0, subsample_col=1.0):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.subsample = subsample
        self.subsample_col = subsample_col
        self.estimators = []
        self.mean = None

    def fit(self, X_train, y_train):
        y_pred = np.ones_like(y_train) * np.mean(y_train)
        self.mean = np.mean(y_train)
        for i in range(self.n_estimators):
            if i == 0:
                antigradient = y_train
            else:
                antigradient = y_train - y_pred
            estimator = DecisionTreeRegressor(max_depth=self.max_depth,
                                              min_samples_leaf=self.min_samples_leaf)
            X_batch, antigradient_batch = self.split_data(X_train, antigradient)
            estimator.fit(X_batch, antigradient_batch)
            prediction = estimator.predict(X_train)
            y_pred += self.learning_rate * prediction
            self.estimators.append(estimator)

    def predict(self, X_test):
        if not self.mean:
            raise NotFittedError
        else:
            y_test = self.mean * np.ones(X_test.shape[0])
            for est in self.estimators:
                y_test += self.learning_rate * est.predict(X_test)
            return y_test

    def split_data(self, X, y):
        num_measures = X.shape[0]
        num_features = X.shape[1]
        row_indices = np.arange(num_measures)
        col_indices = np.arange(num_features)
        np.random.shuffle(row_indices)
        np.random.shuffle(col_indices)
        row_batch_size = int(self.subsample * num_measures)
        col_batch_size = int(self.subsample_col * num_features)
        X_batch = np.take(X, row_indices[:row_batch_size], axis=0)
        X_batch[:, ~col_indices[:col_batch_size]] = 0
        y_batch = np.take(y, row_indices[:row_batch_size])
        return X_batch, y_batch
