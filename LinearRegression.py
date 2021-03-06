# -*- coding: utf-8 -*-
"""LinearRegressor_第二次

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iXZy3FU0kZd8eUSNbnkm5f5dDBCgG3Gw
"""

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import clear_output
from six.moves import urllib
from sklearn.model_selection import train_test_split

import tensorflow.compat.v2.feature_column as fc

import tensorflow as tf
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# Load dataset.
dataset = pd.read_csv('/content/drive/MyDrive/Toehold_Switch_Training_Library_v1.csv')
del dataset['Toehold switch number']
y = dataset.pop('ON/OFF')
x_train, x_test, y_train, y_test = train_test_split(dataset, y, test_size=0.3)


Features = ['Probability', 'loop_number', 'toehold_length', 'stem_length', 'loop_size', 'end_length', 'MFE']
feature_columns = []
for feature_name in Features:
  feature_columns.append(tf.feature_column.numeric_column(feature_name, dtype=tf.float32))


def make_input_fn(data_df, label_df, num_epochs=10, shuffle=True, batch_size=32):
  def input_function():
    ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))
    if shuffle:
      ds = ds.shuffle(1000)
    ds = ds.batch(batch_size).repeat(num_epochs)
    return ds
  return input_function

train_input_fn = make_input_fn(x_train, y_train)
eval_input_fn = make_input_fn(x_test, y_test, num_epochs=1, shuffle=False)


linear_est = tf.estimator.LinearRegressor(feature_columns=feature_columns)
linear_est.train(train_input_fn)
result = linear_est.evaluate(eval_input_fn)

clear_output()
print(result)

predictions=[]
for pred in linear_est.predict(input_fn=eval_input_fn):
    predictions.append(np.array(pred['predictions']).astype(float))


r2_score(y_test, predictions)

result = list(linear_est.predict(eval_input_fn))
print(x_test.iloc[10])
print(y_test.iloc[10])
print(result[10])