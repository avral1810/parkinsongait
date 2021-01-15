import pandas
import numpy as np
from pandas.plotting import scatter_matrix #.tools.plotting is depricated


def shuffler(dataset):
  return dataset.reindex(np.random.permutation(dataset.index))


def __acquire__():
	url = "dataFiles/fortrain/all.csv"
	names = ['gct', 'fl', 'tl', 'hal', 'll', 'kal', 'katl', 'height' ,'class']
	dataset = pandas.read_csv(url,names = names)
	dataset = shuffler(dataset)
	array = dataset.values
	print("File Read")
	Z = []
	X = array[:,0:-1]
	for i in range(0,len(array)):
		if array[i][-1] == np.float64(1.0):
			Z.append([1,0,0])
		elif array[i][-1] == np.float64(2.0):
			Z.append([0,1,0])
		elif array[i][-1] == np.float64(3.0):
			Z.append([0,0,1])
	print("Data set complete")
	return X,np.array(Z)

def batch(geneXall, geneYall, batch_size, last_batch):
	geneX = geneXall[last_batch:last_batch+batch_size]
	geneY = geneYall[last_batch:last_batch+batch_size]
	return geneX,geneY
