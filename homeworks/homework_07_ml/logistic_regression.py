#!/usr/bin/env python
# coding: utf-8


import numpy as np
from sklearn import linear_model
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split


class LogisticRegression:
    def __init__(self, lambd_coef=1, alpha=0.001, batch_size=50, max_iter=100):
        self.coef = lambd_coef
        # regilarization = l1
        self.a = alpha
        self.size = batch_size
        self.max = max_iter
        self.min_proba = 0.9

    def fit(self, X_train, y_train):
        y_train = y_train.reshape((-1, 1))
        matrix = np.hstack((np.ones((X_train.shape[0], 1)), X_train, y_train))
        self.w = np.random.normal(size=(1, X_train.shape[1] + 1))
        eps = 0.001
        for _ in range(self.max):
            ind = np.random.permutation(np.arange(matrix.shape[0]))
            for i in range(int(X_train.shape[0] / self.size)):
                perm = ind[i * self.size: (i + 1) * self.size]
                x = matrix[perm, :-1]
                y = matrix[perm, -1]
                # gradient
                '''cost = self.cost_func(x, y)
                old_cost = cost'''
                self.w -= self.coef * self.log_gradient(x, y)
                '''cost = self.cost_func(x, y)
                diff = old_cost - cost
                if diff > eps:
                    break'''

    def predict(self, X_test):
        proba = self.predict_proba(X_test)
        pred_value = np.where(proba >= self.min_proba, 1, 0)
        return np.squeeze(pred_value)

    def predict_proba(self, X_test):
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return np.squeeze(self.logistic_func(X_test))

    def get_weights(self):
        return self.w

    def logistic_func(self, x):
        pred = 1.0 / (1.0 + np.exp(-np.dot(x, self.w.T)))
        return pred

    def log_gradient(self, X, y):
        diff = self.logistic_func(X) - y.reshape(X.shape[0], -1)
        return np.dot(diff.T, X) + np.squeeze(self.a * np.sign(self.w.T))

    def cost_func(self, X, y):
        log_func_v = np.squeeze(self.logistic_func(X))
        y = np.squeeze(y)
        step1 = y * np.log(log_func_v)
        step2 = (1-y) * np.log(1-log_func_v)
        final = -step1 - step2
        return np.mean(final)


size = 5000
n_feat = 20

np.random.seed(0)

C1 = np.random.randn(n_feat, n_feat) * 5
C2 = np.random.randn(n_feat, n_feat) * 5
gauss1 = np.dot(np.random.randn(size, n_feat) + np.random.randn(n_feat) * 0.3, C1)
gauss2 = np.dot(np.random.randn(size, n_feat) + np.random.randn(n_feat) * 0.3, C2)

x = np.vstack([gauss1, gauss2])
y = np.r_[np.ones(size), np.zeros(size)]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

lr1 = linear_model.LogisticRegression()
lr2 = LogisticRegression(batch_size=500, max_iter=1000)

lr1.fit(x_train, y_train)
lr2.fit(x_train, y_train)

# check predict works
assert lr2.predict(x_test).shape == y_test.shape

loss1 = log_loss(y_test, lr1.predict_proba(x_test))
loss2 = log_loss(y_test, lr2.predict_proba(x_test))
proba = lr2.predict_proba(x_test)
predict = np.where(lr2.predict_proba(x_test) != y_test, 1, 0)
su = 0
for i in predict:
    if i == 1:
        su += 1
print(su)

assert loss2 < loss1 * 2
