import numpy as np


class LogisticRegression:
    def __init__(self, adam_coef=0.001, l1=0.01, l2=0.01, regularization='elastic', batch_size=50, max_iter=1000):
        self.adam_coef = adam_coef
        self.l1 = l1
        self.l2 = l2
        self.max_iter = max_iter
        self.batch_size = batch_size
        self.coef_ = None
        self.intercept_ = None

    def grad_func(self, x_train, y_train, coef_last, regulator):
        return 1 / len(x_train) * x_train.transpose() @ (
            self.sigmoid(x_train @ coef_last) - y_train) + regulator

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def fit(self, x_train, y_train, eps=1e-5):
        assert x_train.shape[0] == y_train.shape[0], 'Invalid dimensions'
        x_train = np.hstack([np.ones((x_train.shape[0], 1)), x_train])
        self.coef_ = np.random.randn(x_train.shape[1])
        np.random.seed(346346)
        x = np.array_split(x_train, self.batch_size)
        y = np.array_split(y_train, self.batch_size)
        indexes = list(range(len(x)))
        np.random.shuffle(indexes)
        elastic = 2 * self.l2 * self.coef_ + self.l1 * np.sign(self.coef_)
        beta1 = 0.9
        beta2 = 0.999
        eps_stable = 1e-9
        t = 0
        sqrs = np.zeros(x_train.shape[1])
        vs = np.zeros(x_train.shape[1])
        for _ in range(self.max_iter):
            for idx in indexes:
                tmp_coef = np.copy(self.coef_)
                t += 1
                g = self.grad_func(x[idx], y[idx], self.coef_, elastic) / x[idx].shape[0]
                vs = beta1 * vs + (1 - beta1) * g
                sqrs = beta2 * sqrs + (1 - beta2) * np.square(g)
                v_bias_corr = vs / (1 - beta1 ** t)
                sqr_bias_corr = sqrs / (1 - beta2 ** t)
                div = self.adam_coef * v_bias_corr / (np.sqrt(sqr_bias_corr) + eps_stable)
                self.coef_ -= div
                if np.sum(np.abs(self.coef_ - tmp_coef)) < eps:
                    return
        self.intercept_ = self.coef_[0]
        self.coef_ = self.coef_[1:]

    def predict(self, x_test):
        assert self.coef_ is not None, 'Model is not fitted'
        res = np.sign(self.sigmoid(np.sum(self.intercept_ + self.coef_ * x_test, axis=1)))
        res[res == -1] = 0
        return res

    def predict_proba(self, x_test):
        assert self.coef_ is not None, 'Model is not fitted'
        return self.sigmoid(np.sum(self.intercept_ + self.coef_ * x_test, axis=1))

    def get_weights(self):
        return np.hstack((self.intercept_, self.coef_))
