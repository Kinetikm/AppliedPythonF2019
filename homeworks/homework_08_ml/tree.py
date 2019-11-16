import numpy as np


class Node:
    def __init__(self, feature=None, left=None, right=None, threshold=None, y_value=None):
        self.left = left
        self.right = right
        self.y_value = y_value
        self.threshold = threshold
        self.feature = feature


class Tree:
    def __init__(self, criterion='mse', max_depth=5, min_samples_leaf=8):
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.feature_importance = None
        self.depth = 0
        self.root = None
        self.len_x_train = 0

    def gain(self, y_l, y_r):
        y = np.vstack((y_l, y_r))
        if self.criterion == 'mae':
            return np.mean(np.abs(y - np.mean(y))) - len(y_l)/len(y) * np.mean(np.abs(y_l - np.mean(y_l))) \
                   - len(y_r)/len(y) * np.mean(np.abs(y_r - np.mean(y_r)))
        elif self.criterion == 'mse':
            return np.mean((y - np.mean(y)) ** 2) - len(y_l)/len(y) * np.mean((y_l - np.mean(y_l)) ** 2) \
                   - len(y_r)/len(y) * np.mean((y_r - np.mean(y_r)) ** 2)
        else:
            raise TypeError

    def fit(self, x_train, y_train, eps=0.000001):
        self.len_x_train = x_train.shape[0]
        self.feature_importance = np.zeros(x_train.shape[1])
        x_y_train = np.hstack((x_train, y_train.reshape((-1, 1))))
        self.root = self.build_tree(x_y_train, eps)

    def build_tree(self, x_y_train, eps):
        if (self.max_depth and self.depth == self.max_depth) or x_y_train.shape[0] < 2 * self.min_samples_leaf:
            return Node(y_value=np.mean(x_y_train[:, -1]))
        max_gain = 0
        best_feature = 0
        t = -1
        threshold = 0
        for i in range(x_y_train.shape[1] - 1):
            train_sorted = x_y_train[x_y_train[:, i].argsort()]
            y = train_sorted[:, -1]
            for j in range(self.min_samples_leaf, x_y_train.shape[0] - self.min_samples_leaf):
                y_l = y[:j].reshape((-1, 1))
                y_r = y[j:].reshape((-1, 1))
                gain = self.gain(y_l, y_r)
                if gain > max_gain:
                    max_gain = gain
                    best_feature = i
                    t = j
                    threshold = (train_sorted[j, best_feature] + train_sorted[j + 1, best_feature]) / 2
        if max_gain < eps:
            return Node(best_feature, y_value=np.mean(x_y_train[:, -1]))
        train_sorted = x_y_train[x_y_train[:, best_feature].argsort()]
        self.feature_importance[best_feature] += (x_y_train.shape[0]/self.len_x_train) * max_gain
        self.depth += 1

        left_child = self.build_tree(train_sorted[:t, :], eps)
        right_child = self.build_tree(train_sorted[t:, :], eps)
        return Node(best_feature, left_child, right_child, threshold)

    def predict(self, x_test):
        predict = np.zeros(x_test.shape[0])
        for i in range(len(predict)):
            node = self.root
            while node.left is not None:
                if x_test[i, node.feature] <= node.threshold:
                    node = node.left
                else:
                    node = node.right
            predict[i] = node.y_value
        return predict

    def get_feature_importance(self):
        return self.feature_importance / np.sum(self.feature_importance)


class TreeRegressor(Tree):
    def __init__(self, criterion='mse', max_depth=None, min_samples_leaf=1):
        super().__init__(criterion, max_depth, min_samples_leaf)


class TreeClassifier(Tree):
    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=1):
        super().__init__(criterion, max_depth, min_samples_leaf)
        raise NotImplementedError

    def predict_proba(self, x_test):
        pass
