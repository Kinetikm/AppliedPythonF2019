#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import csv
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model


df = pd.read_csv('Train.csv', index_col=0)
df.insert(1, 'year', pd.to_datetime(df['date']).dt.year)
df.insert(2, 'month', pd.to_datetime(df['date']).dt.month)
df.drop(columns='date', inplace=True)
df.fillna(0, inplace=True)
x = df.iloc[:,1:-1]
y = df.iloc[:,-1]
pf = PolynomialFeatures(degree=2)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)
x_poly = pf.fit_transform(x_train)
print(x.shape)
print(x_poly.shape)
lr = LinearRegression()
# lr.fit(x_train, y_train)

lr.fit(x_poly, y)
print(lr.score(x_poly, y))
print(lr.coef_)
print(lr.score(pf.fit_transform(x_test), y_test))

test_data = pd.read_csv('./Test.csv', index_col=0)
test_data.fillna(0, inplace=True)
test_data['date'] = pd.to_datetime(test_data['date']).dt.month
test_data.insert(1, 'year', pd.to_datetime(test_data['date']).dt.year)
test_data.insert(2, 'month', pd.to_datetime(test_data['date']).dt.month)
test_data.drop(columns='date', inplace=True)
print(test_data.iloc[:,1:].shape)
data_poly = pf.fit_transform(test_data.iloc[:,1:])
print(data_poly.shape)
test_price = lr.predict(data_poly)
test_data['price'] = test_price
result = test_data['price']
result.to_csv('./learn_result.csv', sep=',', header=['price'])