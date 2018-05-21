#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import numpy as np
import tensorflow as tf
import keras
import os
import shutil

if __name__ == '__main__':
	# data prepare
	original_dataset_dir = './train'
	base_dir = 'cats_and_dogs_small'
	#os.mkdir(base_dir)
	train_dir = os.path.join(base_dir, 'train')
	#os.mkdir(train_dir)
	validation_dir = os.path.join(base_dir, 'validation')
	#os.mkdir(validation_dir)
	test_dir = os.path.join(base_dir, 'test')
	#os.mkdir(test_dir)
	train_cats_dir = os.path.join(train_dir, 'cats')
	#os.mkdir(train_cats_dir)
	train_dogs_dir = os.path.join(train_dir, 'dogs')
	#os.mkdir(train_dogs_dir)
	validation_cats_dir = os.path.join(validation_dir, 'cats')
	#os.mkdir(validation_cats_dir)
	validation_dogs_dir = os.path.join(validation_dir, 'dogs')
	#os.mkdir(validation_dogs_dir)
	test_cats_dir = os.path.join(test_dir, 'cats')
	#os.mkdir(test_cats_dir)
	test_dogs_dir = os.path.join(test_dir, 'dogs')
	#os.mkdir(test_dogs_dir)

	fnames = ['cat.{}.jpg'.format(i) for i in range(1000)]
	for fname in fnames:
		src = os.path.join(original_dataset_dir, fname)
		dst = os.path.join(train_cats_dir, fname)
		shutil.copyfile(src, dst)

	fnames = ['cat.{}.jpg'.format(i) for i in range(1000,1500)]
	for fname in fnames:
		src = os.path.join(original_dataset_dir, fname)
		dst = os.path.join(validation_cats_dir, fname)
		shutil.copyfile(src, dst)

	fnames = ['cat.{}.jpg'.format(i) for i in range(1500,2000)]
	for fname in fnames:
		src = os.path.join(original_dataset_dir, fname)
		dst = os.path.join(test_cats_dir, fname)
		shutil.copyfile(src, dst)

	fnames = ['dog.{}.jpg'.format(i) for i in range(1000)]
	for fname in fnames:
		src = os.path.join(original_dataset_dir, fname)
		dst = os.path.join(train_dogs_dir, fname)
		shutil.copyfile(src, dst)

	fnames = ['dog.{}.jpg'.format(i) for i in range(1000,1500)]
	for fname in fnames:
		src = os.path.join(original_dataset_dir, fname)
		dst = os.path.join(validation_dogs_dir, fname)
		shutil.copyfile(src, dst)

	fnames = ['dog.{}.jpg'.format(i) for i in range(1500,2000)]
	for fname in fnames:
		src = os.path.join(original_dataset_dir, fname)
		dst = os.path.join(test_dogs_dir, fname)
		shutil.copyfile(src, dst)

	print('total training cat images:', len(os.listdir(train_cats_dir)))
	print('total training dog images:', len(os.listdir(train_dogs_dir)))
	print('total validation cat images:', len(os.listdir(validation_cats_dir)))
	print('total validation dog images:', len(os.listdir(validation_dogs_dir)))
	print('total test cat images:', len(os.listdir(test_cats_dir)))
	print('total test dog images:', len(os.listdir(test_dogs_dir)))
	from keras import layers
	from keras import models
	model = models.Sequential()
	model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150,150,3)))
	model.add(layers.MaxPooling2D((2, 2)))
	model.add(layers.Conv2D(64, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D((2, 2)))
	model.add(layers.Conv2D(128, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D((2, 2)))
	model.add(layers.Conv2D(128, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D((2, 2)))
	model.add(layers.Flatten())
	model.add(layers.Dropout(0.5))
	model.add(layers.Dense(512, activation='relu'))
	model.add(layers.Dense(1, activation='sigmoid'))
	model.summary()

	from keras import optimizers
	model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=1e-4), metrics=['acc'])

	from keras.preprocessing.image import ImageDataGenerator
	train_datagen = ImageDataGenerator(rescale=1./255)
	test_datagen = ImageDataGenerator(rescale=1./255)
	train_generator = train_datagen.flow_from_directory(train_dir, target_size=(150, 150), batch_size=20, class_mode='binary')
	validation_generator = test_datagen.flow_from_directory(validation_dir, target_size=(150, 150), batch_size=20, class_mode='binary')
	for data_batch, labels_batch in train_generator:
		print('data batch shape:', data_batch.shape)
		print('labels batch shape:', labels_batch.shape)
		break
	
	history = model.fit_generator(train_generator, steps_per_epoch=100, epochs=30, validation_data=validation_generator, validation_steps=50)
	model.save('cats_and_dogs_small_1.h5')
	#model = models.load_model('cats_and_dogs_mall_1.h5')

	with matplotlib.backends.backend_pdf.PdfPages('DL_5_4.pdf') as pdf_all: 
		acc = history.history['acc']
		val_acc = history.history['val_acc']
		loss = history.history['loss']
		val_loss = history.history['val_loss']
		epochs = range(1, len(acc)+1)

		fig = plt.figure()
		plt.plot(epochs, acc, 'bo', label='Training acc')
		plt.plot(epochs, val_acc, 'b', label='Validation acc')
		plt.xlabel('Epochs', fontsize=20)
		plt.ylabel('Accuracy', fontsize=20)
		plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)
		plt.legend()
		plt.tight_layout()
		pdf_all.savefig(fig)

		fig = plt.figure()
		plt.plot(epochs, loss, 'bo', label='Training loss')
		plt.plot(epochs, val_loss, 'b', label='Validation loss')
		plt.xlabel('Epochs', fontsize=20)
		plt.ylabel('Loss', fontsize=20)
		plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)
		plt.legend()
		plt.tight_layout()
		pdf_all.savefig(fig)

	datagen = ImageDataGenerator(rotation_range=40, width_shift_range=0.2, height_shift_range=0.2, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')
	from keras.preprocessing import image
	fname = [os.path.join(train_cats_dir, fname) for fname in os.listdir(train_cats_dir)]
	img_path = fnames[3]
	img = image.load_img(img_path, target_size=(150, 150))
	x = image.img_to_array(img)
	x = x.reshape((1,) + x.shape)
	i = 0
	for batch in datagen.flow(x, batch_size=1):
		plt.figure(i)
		imgplt = plt.imshow(image.array_to_img(batch[0]))
		i += 1
		if i % 4 == 0:
			break
	#plt.show()

	from keras.preprocessing.image import ImageDataGenerator
	train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=40, width_shift_range=0.2, shear_range=0.2, zoom_range=0.2, horizontal_flip=True,)
	test_datagen = ImageDataGenerator(rescale=1./255)
	train_generator = train_datagen.flow_from_directory(train_dir, target_size=(150, 150), batch_size=32, class_mode='binary')
	validation_generator = test_datagen.flow_from_directory(validation_dir, target_size=(150, 150), batch_size=32, class_mode='binary')
	history = model.fit_generator(train_generator, steps_per_epoch=100, epochs=100, validation_data=validation_generator, validation_steps=50)
	model.save('cats_and_dogs_small_2.h5')
	#model = models.load_model('cats_and_dogs_mall_1.h5')

