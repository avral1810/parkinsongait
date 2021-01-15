import tensorflow as tf
import pickle
import numpy as np
import shuffler 
import sys
import random
import statistics
import pandas


tor = ""
try:
	tor = sys.argv[1]
	tor = tor.lower()
except:
	print("Provide type [train] or [run VALUE]")




if tor == "train":
	geneXall, geneYall = shuffler.__acquire__()
	total_data = len(geneYall)


n_nodes_hl1 = 500
n_nodes_hl2 = 500

last_batch = 0
n_classes = 3

batch_size = 4000
number_of_inputs = 8
hm_epochs = 150

x = tf.placeholder('float')
y = tf.placeholder('float')

hidden_1_layer = {'f_fum': n_nodes_hl1, 'weight' : tf.Variable(tf.random_normal([number_of_inputs,n_nodes_hl1])),
				'bias' : tf.Variable(tf.random_normal([n_nodes_hl1]))}
hidden_2_layer = {'f_fum': n_nodes_hl2, 'weight' : tf.Variable(tf.random_normal([n_nodes_hl1,n_nodes_hl2])),
				'bias' : tf.Variable(tf.random_normal([n_nodes_hl2]))}
output_layer = {'f_fum': None, 'weight' : tf.Variable(tf.random_normal([n_nodes_hl2,n_classes])),
				'bias' : tf.Variable(tf.random_normal([n_classes]))}



def nn_model(data):
	l1 = tf.add(tf.matmul(data,hidden_1_layer['weight']), hidden_1_layer['bias'])
	l1 = tf.nn.relu(l1)

	l2 = tf.add(tf.matmul(l1,hidden_2_layer['weight']), hidden_2_layer['bias'])
	l2 = tf.nn.relu(l2)

	output = tf.matmul(l2,output_layer['weight']) + output_layer['bias'] 

	return output

saver =  tf.train.Saver()
tf_log = 'models/tf.log'
el_log = 'models/el.log'


def train_nn(x):
	global last_batch
	prediction = nn_model(x)
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits = prediction, labels = y))
	optimizer = tf.train.AdamOptimizer(learning_rate = 0.01).minimize(cost)
	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())
		try:
			epoch = int(open(tf_log,'r').read().split('\n')[-2]) + 1
		except:
			epoch = 1
		while epoch <= hm_epochs:
			if epoch != 1:
				saver.restore(sess,"./models/model-1.ckpt")
			epoch_loss = 1
			last_batch = 0
			once_done = [0,0,0]
			while last_batch < total_data:
				geneX,geneY = shuffler.batch(geneXall,geneYall,batch_size,last_batch)
				last_batch = last_batch + batch_size
				_, c = sess.run([optimizer, cost], feed_dict = {x: (geneX), y:(geneY)})
				epoch_loss += c
			saver.save(sess,"./models/model-1.ckpt")
			print('Epoch', epoch, 'completed out of',hm_epochs,'loss',epoch_loss)
			with open(tf_log,'a') as f:
				f.write(str(epoch) + '\n')
			with open(el_log,'a') as f:
				f.write("loss " + str(epoch_loss) +" "+str(epoch) + '\n')
			epoch += 1

def use_nn(input_data):
	prediction = nn_model(x)
	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())
		saver.restore(sess,"./models/model-1.ckpt")
		feature = np.array(input_data)
		result = sess.run(tf.argmax(prediction.eval(feed_dict = {x:[feature]}),1))
		return int(result[0])


if tor == "run":
	try:
		epoch = int(open(tf_log,'r').read().split('\n')[-2]) + 1
	except:
		print("Model not trained")
		exit()	
	useFile = "dataFiles/test/someone.csv"
	ll = []
	names = ['gct', 'fl', 'tl', 'hal', 'll', 'kal', 'katl', 'height' ,'class']
	dataset2 = pandas.read_csv(useFile,names = names)
	size = int(dataset2.shape[0])
	low = random.randint(0,size - 50)
	dataset2 = dataset2[low : low + 50]
	dataset2 = np.array(dataset2)
	dataset2 = dataset2[:,0:8]
	for e in dataset2:
		ll.append(use_nn(np.array(e)))
	subject = ""
	if int(statistics.mode(ll)) == 0:
		subject = "Zaid"
	elif int(statistics.mode(ll)) == 1:
		subject = "Aru"
	elif int(statistics.mode(ll)) == 2:
		subject = "Aditya"
	print("class is ", subject)
	exit(subject)
elif tor == "train":
	train_nn(x)	