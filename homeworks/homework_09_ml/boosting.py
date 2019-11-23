# coding: utf-8


import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split


class GradientBoosting:
    def __init__(self, n_estimators=100, learning_rate=1.0, max_depth=None,
                 min_samples_leaf=1, subsample=1.0, subsample_col=1.0):
        self.quantity = n_estimators
        self.lr = learning_rate
        self.depth = max_depth
        self.leafs = min_samples_leaf
        self.trees = list()
        self.subsample = subsample

    def fit(self, X_train, y_train):
        self.y_mean = np.mean(y_train)
        y_pred = np.ones(X_train.shape[0], ) * self.y_mean
        for i in range(self.quantity):
            grad = (y_train - y_pred)
            tree = DecisionTreeRegressor(max_depth=self.depth, min_samples_leaf=self.leafs)
            tree.fit(X_train, grad)
            predictions = tree.predict(X_train)
            y_pred += self.lr * predictions
            self.trees.append(tree)

    def predict(self, X_test):
        if (len(self.trees) < 1):
            raise NotImplementedError
        y_pred = np.ones(X_test.shape[0], ) * self.y_mean
        for tree in self.trees:
            y_pred += self.lr * tree.predict(X_test)
        return y_pred
