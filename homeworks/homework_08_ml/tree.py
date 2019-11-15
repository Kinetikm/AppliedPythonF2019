#!/usr/bin/env python
# coding: utf-8

from collections import deque
import numpy as np

def get_class(sample):
    # УБРАТЬ ИЗ КЛАССА!
    # 1 or 0
    print(sample[sample == 1])
    return len(sample[sample == 1]) > len(sample[sample == 0])
    
def get_proba(sample):
    # возвращает вероятность единичек!
    return len(sample[sample == 1]) / len(sample)    


def is_numeric(feature_column):
    return feature_column.dtype == int or feature_column.dtype == float


def gini(target_sample):
    # вероятность состояния 1 (1 класс)
    p_one = target_sample[target_sample == 1].shape[0] / target_sample.shape[0]
    return 1 - p_one ** 2 - (1 - p_one) ** 2


def entropy(target_sample):
    # вероятность состояния 1 (1 класс)
    p_one = target_sample[target_sample == 1].shape[0] / target_sample.shape[0]
    return -(p_one * np.log2(p_one) + (1 - p_one) * np.log2(1 - p_one))


# DECSISION TREE
def get_leaf_samp(observation, tree):
    # Если нет фичи, значит это лист
    if tree.feature == None:
        return tree.result
    feat_val = observation[tree.feature]
    print('feat_val', feat_val)
    if observation.dtype == int or observation.dtype == float:
        if feat_val <= tree.threshold:
            branch = tree.l_child
        else:
            branch = tree.r_child
    else:
        if feat_val == tree.threshold:
            branch = tree.l_child
        else:
            branch = tree.r_child
    return get_leaf_samp(observation, branch)


def sort_by_column(column, sample):
    sorted_idxs = sample[:, column].argsort(axis=0)
    return sample[sorted_idxs, :]


def split_by_value(is_number, row, column, data):
    value = data[row, column]
    if is_number:
        r_sample = data[data[:, column] > value]
        l_sample = data[data[:, column] <= value]
    else:
        l_sample = data[data[:, column] == value]
        r_sample = data[data[:, column] != value]
    return l_sample, r_sample


class Tree:
    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        self.criterion = gini if criterion.lower() == 'gini' else entropy ########
        self.max_depth = max_depth if max_depth else -1
        self.min_samples_leaf = min_samples_leaf
        self.tree_ = None

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        data = np.c_[X_train, y_train]
        
        self.n_features = X_train.shape[1]
        self.tree_ = DecisionTree(self.criterion, self.max_depth, self.min_samples_leaf)
        self.tree_.build_tree(sample=data, initial_size=X_train.shape[0], depth=0)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_pred = np.empty(X_test.shape[0])
        # попробовать векторайзером еще!
        for row in range(X_test.shape[0]):
            leaf_samp = get_leaf_samp(X_test[row], self.tree_)
            y_pred[row] = get_class(leaf_samp)
        return y_pred

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        self.feat_imp = np.empty(self.n_features)
        stack = deque()
        stack.appendleft(self.tree_)
        while stack:
            tree = stack.popleft()
            if tree.l_child:
                stack.appendleft(tree.l_child)
            if tree.r_child:
                stack.appendleft(tree.r_child)
            if tree.feature != None:
                self.feat_imp[tree.feature] += tree.node_importance
        self.feat_imp = self.feat_imp / np.sum(self.feat_imp)
        return self.feat_imp

class TreeRegressor(Tree):
    def __init__(self, criterion='mse', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'mse' or 'mae'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)
        raise NotImplementedError


class TreeClassifier(Tree):
    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'gini' or 'entropy'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        y_pred = np.empty(X_test.shape[0])
        for row in range(X_test.shape[0]):
            leaf_samp = get_leaf_samp(X_test[row], self.tree_)
            y_pred[row] = get_proba(leaf_samp)
        return y_pred


class DecisionTree:
    def __init__(self, criterion, max_depth, min_samples_leaf):
        # описать!
        self.criterion = criterion#self._gini if criterion.lower() == 'gini' else self._entropy
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        # закомментировать!
        # колонка фичи, которая разделила
        self.feature = None
        # значение фичи
        self.threshold = None
        # entropy or gini score
        self.score = None
        # результат работы дерева(лист)
        # заполняется только если ЛИСТ!
        self.result = None
        self.l_child = None
        self.r_child = None
        
    def build_tree(self, sample, initial_size, depth=1):
        self.score = self.criterion(sample[:, -1])
        self.sample_size = sample.shape[0]

        is_leaf = (self.score == 0 or 
                   (depth == self.max_depth and self.max_depth != -1) or 
                   sample.shape[0] < 2 * self.min_samples_leaf)
        
        if is_leaf:
            # sample[:, 1] - целевая переменная!
            self.result = sample[:, -1]
            return
        
        best_gain, l_samp, r_samp, best_criteria = self.get_best_params(sample)
        
        is_leaf = (best_gain <= 0)
        
        if not is_leaf:
            self.feature = best_criteria[0]
            self.threshold = best_criteria[1]
            
            self.l_child = DecisionTree(self.criterion, self.max_depth, self.min_samples_leaf)
            self.l_child.build_tree(l_samp, initial_size, depth=depth+1)
            
            self.r_child = DecisionTree(self.criterion, self.max_depth, self.min_samples_leaf)
            self.r_child.build_tree(r_samp, initial_size, depth=depth+1)
            
            self.node_importance = self.get_ni(initial_size)
        else:
            self.result = sample[:, -1]
    
    def get_ni(self, initial_size):
        """ node_j_importance = j_samples_size / initial_samples * node_j_impurity - 
             - node_j_Lchild_samples_size / initial_samples * node_j_Lchild_impurity
             - node_j_Rchild_samples_size / initial_samples * node_j_Rchild_impurity.
        """
        ni = self.sample_size / initial_size * self.score
        ni_l = self.l_child.sample_size / initial_size * self.l_child.score
        ni_r = self.r_child.sample_size / initial_size * self.r_child.score
        return ni - ni_l - ni_r
    
    def get_best_params(self, sample):
        # описать функцию!
        rows_number = sample.shape[0]
        columns_number = sample.shape[1]
        
        best_gain = 0.0
        # -1 так как последняя колонка - target
        for col in range(columns_number - 1):
            col_is_num = is_numeric(sample[0, col])
            sample = sort_by_column(col, sample)
        
            for row in range(self.min_samples_leaf - 1, rows_number - 1):
                target_curr = sample[row, -1]
                target_next = sample[row + 1, -1]
                # считаем IG только при переходе через класс
                if target_next != target_curr:
                    value = sample[row, col]
                    l_sample, r_sample = split_by_value(col_is_num, row, col, sample)
                    
                    bad_split = (l_sample.shape[0] < self.min_samples_leaf or
                                 r_sample.shape[0] < self.min_samples_leaf)
                    
                    info_gain = self.get_gain(l_sample, r_sample) if not bad_split else 0.0
                    
                    if info_gain > best_gain:
                        best_gain = info_gain
                        best_l_samp = l_sample
                        best_r_samp = r_sample
                        best_criteria = (col, value)
                        
        return best_gain, best_l_samp, best_r_samp, best_criteria
    
    def get_gain(self, l_sample, r_sample):
        # описать переменные!
        l_size = l_sample.shape[0]
        r_size = r_sample.shape[0]
        
        l_weight = l_size / (l_size + r_size)
        l_score = self.criterion(l_sample[:, 1])
        r_score = self.criterion(r_sample[:, 1])
        gain = self.score - l_weight * l_score - (1 - l_weight) * r_score
        return gain


#X_train = np.arange(20)
#X_train = X_train[:, np.newaxis]
#y_train = np.array([0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1]).T

#tree = TreeClassifier()
#tree.fit(X_train, y_train)

#print(tree.predict(y_train))
#print(tree.predict_proba(y_train))
#print(tree.get_feature_importance())
