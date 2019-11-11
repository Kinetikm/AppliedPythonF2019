#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, lambda_coef=0.00125, regulatization="L1", alpha=0.8, batch_size=50, max_iter=100):
        self.lambda_coef = lambda_coef
        self.regulatization = regulatization
        self.alpha = alpha
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.w = None

    def sigmoida(self, X, w):
        return 1 / (1 + np.exp(- X @ w.T))

    def count_gradient(self, X, w, y):
        return - (1 / X.shape[0]) * ((X.T @ (self.sigmoida(X, w) - y)).T + self.alpha * np.sign(w))

    def log_loss(self, X, w, y):
        a = self.sigmoida(X, w)
        return np.mean(- y * np.log(a) - (1 - y) * np.log(1 - a))

    def fit(self, X_train, y_train):
        X_train = np.append(np.ones((X_train.shape[0], 1)), X_train, axis=1)
        y_train = y_train.reshape((X_train.shape[0], 1))
        w = np.zeros((1, X_train.shape[1]))
        n_samples = min(X_train.shape[0], self.batch_size)

        m_t = 0
        v_t = 0
        E = 1e-8
        beta_1 = 0.1
        beta_2 = 0.99
        tol = 0.1
        i = 1
        log_loss = 100
        loss_change = 100

        while i <= self.max_iter and np.abs(loss_change) > tol:
            idx = np.random.randint(X_train.shape[0], size=n_samples)
            batch = X_train[idx, :]
            y_batch = y_train[idx, :]

            g_t = self.count_gradient(batch, w, y_batch)
            m_t = beta_1 * m_t + (1 - beta_1) * g_t
            v_t = beta_2 * v_t + (1 - beta_2) * (g_t ** 2)

            m_t_hat = m_t / (1 - np.power(beta_1, i))
            v_t_hat = v_t / (1 - np.power(beta_2, i))
            w -= (self.lambda_coef / (np.sqrt(v_t_hat + E))) * m_t_hat

            i += 1
            loss_change = self.log_loss(X_train, w, y_train) - log_loss
            log_loss = self.log_loss(X_train, w, y_train)
        self.w = w

    def predict(self, X_test):
        X_test = np.append(np.ones((X_test.shape[0], 1)), X_test, axis=1)
        g = (X_test @ self.w.T).T
        return np.where(g > 0, 1, 0).reshape(X_test.shape[0])

    def predict_proba(self, X_test):
        X_test = np.append(np.ones((X_test.shape[0], 1)), X_test, axis=1)
        sigma = (self.sigmoida(X_test, self.w))
        return np.concatenate((sigma, 1 - sigma), axis=1)

    def get_weights(self):
        return self.w
