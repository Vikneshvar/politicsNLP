import pandas as pd
import numpy as np
import tensorflow as tf
from sqlalchemy import create_engine
from django.db import connection
import sys
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

def run(): 	
	try:
		engine = create_engine("mysql+mysqldb://root:vik123@localhost:3306/nlp")
		connection = engine.connect()
		sql_query="""select * from nlp.politicsApp_nndata"""
		nlp_df_t = pd.read_sql_query(con=engine,sql=sql_query)
		connection.close()
		engine.dispose()
	except:
		e = sys.exc_info()[0]
		print('Exception occured', e)
	finally:
		print('Successfully read the table')

#	print('nlp_df_t \n',nlp_df_t)
#	print('Shape of nlp_df_t got from db',nlp_df_t.shape)

	# Transpose to original dataframe
	nlp_df=nlp_df_t.transpose()

#	print('nlp_df - original ****** \n',nlp_df)
#	print('Shape of nlp_df_t after transpose',nlp_df.shape)

	# Split data into train and test - 70:30
	msk = np.random.rand(len(nlp_df)) < 0.7
	train_df = nlp_df[msk]
#	print(train_df)
	test_df = nlp_df[~msk]
#	print(test_df)

	def batch(df, trainFlag):
		if trainFlag == 1:
			print('Training -------------- 1')
			new_batch = df.sample(n=25,replace=False)
			x_input = np.array(new_batch.iloc[:,0:len(new_batch.columns)-2])
			y_output = np.array(new_batch.iloc[:,len(new_batch.columns)-2:])
		else:
			print('Test -------------- 0')			
			x_input = np.array(df.iloc[:,0:len(df.columns)-2])
			y_output = np.array(df.iloc[:,len(df.columns)-2:])
		return x_input,y_output

	# Each layer hidden nodes
	nodes_1st=int(len(nlp_df.columns)-2)
	nodes_2st=int(len(nlp_df.columns)/100)
	nodes_3rd=int(len(nlp_df.columns)/1000)
	nodes_output=2

	# Neural Network Design
	# Input nodes - a node for each ngram, rows: None means any number, columns: number of ngrams
	x = tf.placeholder(tf.float32,shape=[None,nodes_1st])

	# Variable to hold the actual output
	y_ = tf.placeholder(tf.float32,shape=[None,2])

	# Drop out probability variable
	keep_prob = tf.placeholder(tf.float32)

	# Weights and bias Variables for 1st layer
	W1 = tf.Variable(tf.truncated_normal(shape=[nodes_1st,nodes_2st],stddev=0.1))
	B1 = tf.Variable(tf.constant(0.1,shape=[nodes_2st]))

	# Output of first layer
	y1 = tf.nn.sigmoid(tf.matmul(x,W1)+B1) 

	# Weights and bias Variables for 2st layer
	W2 = tf.Variable(tf.truncated_normal(shape=[nodes_2st,nodes_3rd],stddev=0.1))
	B2 = tf.Variable(tf.constant(0.1,shape=[nodes_3rd]))

	# Output of first layer
	y2 = tf.nn.sigmoid(tf.matmul(y1,W2)+B2) 

	# Weights and bias Variables for 3rd layer
	W3 = tf.Variable(tf.truncated_normal(shape=[nodes_3rd,nodes_output],stddev=0.1))
	B3 = tf.Variable(tf.constant(0.1,shape=[nodes_output]))

	# Dropout 
	dropout = tf.nn.dropout(y2, keep_prob)

	# Final output
	y = tf.nn.softmax(tf.matmul(dropout,W3)+B3)

	# Cross entropy function 
	cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_,logits=y))
	
	# Using Grdient Descent
	train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

	# comparison of y and y_
	correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
	
	# Accuracy
	accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

	# Use session to initialize all variables
	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())	
		# Run the algorithm - On each iteration, batch of 25 articles goes in network 
		# Feed forward and back	propagaion happens 	
		for i in range(200):
			# Using training data
			x_input,y_output = batch(train_df,1)
			print('W1',W1.eval())
			print('W2',W2.eval())
			train_accuracy = accuracy.eval(feed_dict={x:x_input,y_:y_output,keep_prob:1.0})
			print('Step %d Training accuracy %g' %(i,train_accuracy))
			# Backpropagation
			train_step.run(feed_dict={x:x_input,y_:y_output,keep_prob:0.5})

		# Using test data
		x_input,y_output = batch(test_df,0)
		print('W1',W1.eval())
		print('W2',W2.eval())
		test_accuracy = accuracy.eval(feed_dict={x:x_input,y_:y_output,keep_prob:1.0})
		print('Test Accuracy ', test_accuracy)


"""			
			print('x shape',(x.eval(feed_dict={x:x_input})).shape)
			print('y_',y_.eval(feed_dict={y_:y_output}))
			print('W1',W1.eval())
			print('B1',B1.eval())
			print('y1',y1.eval(feed_dict={x:x_input}))
			print('W2',W2.eval())
			print('B2',B2.eval())
			print('correct_prediction',correct_prediction.eval(feed_dict={x:x_input,y_:y_output,keep_prob:1.0}))

"""	

