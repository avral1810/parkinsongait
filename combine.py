import shuffler
import sys
from os import walk
import random
import os
import numpy as np
from pandas.plotting import scatter_matrix #.tools.plotting is depricated


f = []
for (dirpath, dirnames, filenames) in walk(sys.argv[1]):
	f.extend(filenames)
	break

for e in f:
	if e[-3:] == "csv":
		reader = open(str(sys.argv[1]) + str(e),'r')
		with open('dataFiles/all.csv','a') as temp:
			for each in reader:
				temp.write(each)
