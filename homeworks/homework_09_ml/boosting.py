#!/usr/bin/env python
# coding: utf-8
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
        self.h_step = None
        self.trees = []
        self.mean = 0

    def fit(self, x_train, y_train):
        tree = DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf)
        self.mean = np.mean(y_train)
        self.h_step = np.full_like(y_train, np.mean(y_train))
        n_features = int(self.subsample_col * x_train.shape[1])
        n_samples = int(self.subsample * x_train.shape[0])
        for i in range(self.n_estimators):
            samples = np.random.randint(x_train.shape[0], size=n_samples)
            features = np.random.randint(x_train.shape[1], size=n_features)
            x_train_boost = x_train[samples]
            x_train_boost = x_train_boost[:, features]
            tree = tree.fit(x_train_boost, y_train[samples] - self.h_step[samples])
            self.h_step[samples] += self.learning_rate * tree.predict(x_train_boost)
            self.trees.append((tree, features))

    def predict(self, x_test):
        y_test = np.full((1, x_test.shape[0]), self.mean)
        for i in range(len(self.trees)):
            x_train_boost = x_test[:, self.trees[i][1]]
            y_test += self.learning_rate * self.trees[i][0].predict(x_train_boost)
        return y_test[0]
