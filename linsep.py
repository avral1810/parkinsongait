#Team Members:
# Vandit Maheshwari
# Aviral Upadhyay

import numpy as np
from cvxopt import matrix, solvers
import matplotlib.pyplot as plt

def getData():
    fil = open('linsep.txt')
    aa = fil.readlines()
    aa = [line[:-1] for line in aa ]
    data = np.array([[ float(ele) for ele in line.split(',')] for line in aa])
    Y = data[:,-1]
    Y = Y.reshape(len(data),-1)
    X = data[:,:-1]
    return X,Y

def getQMatrix(X,Y):
    ymul = np.dot(Y,Y.T)
    xmul = np.dot(X,X.T)
    return np.multiply(xmul,ymul)

def solver(X,Y):
    QMat = getQMatrix(X,Y)
    P = matrix(QMat.tolist())
    q = matrix([-1.0 for i in range(0,len(X))])
    ide  = -1 * np.identity(len(X))
    G = matrix(ide.tolist())
    h = matrix([0.0 for i in range(0,len(X))])
    A = Y.T
    A = A.astype(np.double)
    A = A.tolist()[0]
    A = matrix(A,(1,len(X)))
    b = matrix(0.0)
    sol = solvers.qp(P,q,G,h,A,b)
    return sol['x']

X,Y = getData() #Read the data from the file
alpha = solver(X,Y) #Solve for alpha using the quadratic solver
alpha = np.array(alpha)
alpha = np.around(alpha,5)
indices = np.flatnonzero(alpha)
W = np.dot(np.multiply(alpha,Y).T,X) # Calculating the Weights value
b = Y.T - np.dot(W,X.T) # Calculating the bias values
bvals = b[0][indices]
print("Weight Values : {}".format(W))
print("Intercept Value: ",bvals[0])
print("The equation of the line is :")
print("[{}] x + [{}] y + {}".format(W[0][0],W[0][1],bvals[0]))
x = np.linspace(0,1,100)
for iterator in x:
    y = ((-(W[0][0]/W[0][1]) * x) - (bvals[0]/W[0][1]))
    plt.plot(x,y,'g-')
plt.scatter(X[:,0],X[:,1],c=Y,cmap='bwr',alpha=1,s=50,edgecolors='k')
plt.show()