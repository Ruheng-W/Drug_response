import numpy as np
from sklearn import linear_model
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from tensorflow.keras import layers
from tensorflow.keras import regularizers
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from drug_transformer import *

epochs = 30


def shallow_nn(input_dim:float):
	"""
	Create shallow neural network benchmark for drug IC50 prediction

	Parameters:
	-----------
	input_dim: model input dimension

	Returns:
	--------
	the built model
	"""

	model = Sequential()
	model.add(Dense(500, input_dim=input_dim, activation= "relu",kernel_regularizer=regularizers.L2(1e-4)))
	model.add(Dense(100, activation= "relu",kernel_regularizer=regularizers.L2(1e-4)))
	model.add(Dense(50, activation= "relu",kernel_regularizer=regularizers.L2(1e-4)))
	model.add(Dense(1))

	model.compile(loss= "mean_squared_error" , optimizer="adam", metrics=["mean_squared_error"])

	return model


def shallow_position_wise_nn():
	"""
	Abalation study on testing baseline for single position-wise feed forward nn
	"""
	X_input = Input((130, 56))
	Y_input = Input((5842, 1))

	dense_1 = tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_2 = tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_3 = tf.keras.layers.Dense(500, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_4 = tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_5 = tf.keras.layers.Dense(1)


	flattern = tf.keras.layers.Flatten()

	#concatenation_layer = concatenation_layer()

	X = dense_1(X_input)
	Y = dense_2(Y_input)

	X = flattern(X)
	Y = flattern(Y)

	Y = tf.concat([X,Y],axis=1)

	Y = dense_3(Y)
	Y = dense_4(Y)
	Y = dense_5(Y)

	model = Model(inputs=(X_input, Y_input), outputs=Y)

	model.compile(loss= "mean_squared_error" , optimizer="adam", metrics=["mean_squared_error"])

	return model

def base_drug_transformer():
	"""
	Abalation study on basic configuration transformer
	"""
	X_input = Input((130, 56))
	Y_input = Input((5843, 1))
	enc_valid_lens = Input(())

	masked_softmax_ = masked_softmax()
	dotproductattention1 = dotproductattention(50)

	dotproductattention_deco = dotproductattention(50)

	att_embedding = attention_embedding()
	r_connection = residual_connection()

	dense_1 = tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_2 = tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_3 = tf.keras.layers.Dense(500, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_4 = tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_5 = tf.keras.layers.Dense(1)

	kernel_key = tf.keras.layers.Dense(50, activation='sigmoid', 
		kernel_regularizer=regularizers.L2(1e-4))

	kernel_query = tf.keras.layers.Dense(50, activation='sigmoid', 
		kernel_regularizer=regularizers.L2(1e-4))

	pos_encoding = positionalencoding(50,130)

	#kernel_value = tf.keras.layers.Dense(output_dim, activation='relu', 
	#	kernel_regularizer=regularizers.L2(1e-4))


	flattern = tf.keras.layers.Flatten()

	#concatenation_layer = concatenation_layer()

	X = dense_1(X_input)

	X = pos_encoding(X)

	#X_query = kernel_query(X)
	#X_key = kernel_key(X)

	#d = X.shape[-1]

	#scores = tf.matmul(X_query, X_key, transpose_b=True)/tf.math.sqrt(
	#	tf.cast(d, dtype=tf.float32))

	score, value = dotproductattention1(X,X,X, enc_valid_lens)
	att_score = masked_softmax_(score, enc_valid_lens)
	att_embedding_ = att_embedding(att_score, value)
	X = r_connection(value, att_embedding_)

	Y = dense_2(Y_input)

	X = flattern(X)
	Y = flattern(Y)

	Y = tf.concat([X,Y],axis=1)

	Y = dense_3(Y)
	Y = dense_4(Y)
	Y = dense_5(Y)

	model = Model(inputs=(X_input, Y_input, enc_valid_lens), outputs=Y)

	model.compile(loss= "mean_squared_error" , optimizer="adam", metrics=["mean_squared_error"])

	return model


def model_save(input_model, name):
	"""
	save current model, name with a tf at last
	"""
	tf.keras.saving.save_model(model,name)

def model_load(name):
	"""
	load model
	"""
	return tf.keras.saving.load_model(name)

def att_score_self_enco(input_model, name):
	"""
	Generate intermediate attention score for examination
	"""
	att_layer = input_model.get_layer(name)
	att_output = Model(inputs=input_model.input, outputs = att_layer.output)

	return att_output

def att_score_self_doce(input_model, name):
	att_layer = input_model.get_layer(name)
	att_output = Model(inputs=input_model.input, outputs = att_layer.output)

	return att_output


def double_shallow_position_wise_nn():
	"""
	Abalation study on testing double head position wise nn
	"""
	X_input = Input((130, 56))
	Y_input = Input((5843, 1))

	dense_1 = tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_1_1 = tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_2 = tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_2_2 = tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_3 = tf.keras.layers.Dense(500, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_4 = tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=regularizers.L2(1e-4))

	dense_5 = tf.keras.layers.Dense(1)


	flattern = tf.keras.layers.Flatten()

	#concatenation_layer = concatenation_layer()

	X = dense_1(X_input)
	X2 = dense_1_1(X_input)
	Y = dense_2(Y_input)
	Y2 = dense_2_2(Y_input)

	X = flattern(X)
	X2 = flattern(X)
	Y = flattern(Y)
	Y2 = flattern(Y2)

	X = tf.concat([X,X2],axis=1)
	Y = tf.concat([Y,Y2],axis=1)
	Y = tf.concat([X,Y],axis=1)

	Y = dense_3(Y)
	Y = dense_4(Y)
	Y = dense_5(Y)

	model = Model(inputs=(X_input, Y_input), outputs=Y)

	model.compile(loss= "mean_squared_error" , optimizer="adam", metrics=["mean_squared_error"])

	return model










