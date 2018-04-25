#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

def build_classifier(data, labels, n_classes=2):
	data_shape = data.get_shape().as_list()
	weights = tf.get_variable(name='weigths', shape=(data_shape[1], n_classes), dtype=tf.float32)
	bias = tf.get_variable(name='bias', initializer=tf.zeros(shape=n_classes))
	logits = tf.add(tf.matmul(data, weights), bias, name='logits')
	return logits, tf.nn.softmax(logits)

def build_generator(data, n_hidden):
	data_shape = data.get_shape().as_list()
	w1 = tf.Variable(tf.random_normal(shape=(data_shape[1], n_hidden)), name='w1')
	b1 = tf.Variable(tf.zeros(shape=n_hidden), name='b1')
	hidden = tf.add(tf.matmul(data, w1), b1, name='hidden_pre-activation')
	hidden = tf.nn.relu(hidden, 'hidden_activation')
	
	w2 = tf.Variable(tf.random_normal(shape=(n_hidden, data_shape[1])), name='w2')
	b2 = tf.Variable(tf.zeros(shape=data_shape[1]), name='b2')
	output=tf.add(tf.matmul(hidden, w2), b2, name='output')
	return output, tf.nn.sigmoid(output)

if __name__ == '__main__':
	batch_size = 64
	g = tf.Graph()
	with g.as_default():
		tf_X = tf.placeholder(shape=(batch_size, 100), dtype=tf.float32, name='tf_X')
		# build the generator
		with tf.variable_scope('generator'):
			gen_out1 = build_generator(data=tf_X, n_hidden=50)

		# build the classifier
		with tf.variable_scope('classifier'):
			# classifier for the original data:
			cls_out1 = build_classifier(data=tf_X, labels=tf.ones(shape=batch_size))
		with tf.variable_scope('classifier', reuse=True):
			# reuse the classifier for generated data
			cls_out2 = build_classifier(data=gen_out1[1], labels=tf.zeros(shape=batch_size))
