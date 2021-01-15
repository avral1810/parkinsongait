#Team Members:
# Vandit Maheshwari
# Aviral Upadhyay

import numpy as np
from cvxopt import matrix, solvers

def getData():
    fil = open('nonlinsep.txt')
    aa = fil.readlines()
    aa = [line[:-1] for line in aa ]
    data = np.array([[ float(ele) for ele in line.split(',')] for line in aa])
    Y = data[:,-1]
    Y = Y.reshape(len(data),-1)
    X = data[:,:-1]
    return X,Y

X,Y = getData()

def kernelFunc(mat):
    return np.square(1 + mat)

def getQMatrix(X,Y):
    ymul = np.dot(Y,Y.T)
    xmul = np.dot(X,X.T)
    zmul = kernelFunc(xmul)
    return np.multiply(zmul,ymul)

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

alpha = solver(X,Y)
alpha = np.array(alpha)
alpha[alpha<1e-5]=0
indices = np.flatnonzero(alpha)
newalpha = alpha.T[0][indices]

newalpha=newalpha.reshape(6,-1)
print(newalpha)
newY = Y.T[0][indices]
newY = newY.reshape(6,-1)
supportVectors = X[:][indices]
supportVectors_y = Y[:][indices]


m =2
kMat = kernelFunc(np.dot(supportVectors,supportVectors.T))
ym = Y.T[0][m]
alphaY = np.multiply(newalpha,newY)
kernelXnXm = kMat[:][m]
kernelXnXm = kernelXnXm.reshape(len(kernelXnXm),-1)
b = ym - np.dot(alphaY.T,kernelXnXm)
print ("The Suppport Vectors are: ")
print (supportVectors)