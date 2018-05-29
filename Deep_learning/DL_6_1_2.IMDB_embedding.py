#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import numpy as np
import tensorflow as tf
import keras

if __name__ == '__main__':
	from keras.datasets import imdb
	from keras import preprocessing
	max_features = 10000
	maxlen = 20
	(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)
	x_train = preprocessing.sequence.pad_sequences(x_train, maxlen=maxlen)
	x_test = preprocessing.sequence.pad_sequences(x_test, maxlen=maxlen)
	print(x_train.shape)

	from keras.models import Sequential
	from keras.layers import Flatten, Dense
	from keras.layers import Embedding
	model = Sequential()
	model.add(Embedding(10000, 8, input_length=maxlen))
	model.add(Flatten())
	model.add(Dense(1, activation='sigmoid'))
	model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
	history = model.fit(x_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

