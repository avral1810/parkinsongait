import pylab,numpy

def smoothList(list,strippedXs=False,degree=10):
    if strippedXs==True: return Xs[0:-(len(list)-(len(list)-degree+1))]
    smoothed=[0]*(len(list)-degree+1)
    for i in range(len(smoothed)):
        smoothed[i]=sum(list[i:i+degree])/float(degree)
    return smoothed

   
def smoothListTriangle(list,strippedXs=False,degree=5):  
    weight=[]
    window=degree*2-1
    smoothed=[0.0]*(len(list)-window)
    for x in range(1,2*degree):weight.append(degree-abs(degree-x))
    w=numpy.array(weight)
    for i in range(len(smoothed)):
        smoothed[i]=sum(numpy.array(list[i:i+window])*w)/float(sum(w))
    return smoothed

   

def smoothListGaussian(list,strippedXs=False,degree=5):  
    window=degree*2-1  
    weight=numpy.array([1.0]*window)  
    weightGauss=[]  
    for i in range(window):
        i=i-degree+1
        frac=i/float(window)
        gauss=1/(numpy.exp((4*(frac))**2))
        weightGauss.append(gauss)
        weight=numpy.array(weightGauss)*weight
        smoothed=[0.0]*(len(list)-window)
        for i in range(len(smoothed)):
            smoothed[i]=sum(numpy.array(list[i:i+window])*weight)/sum(weight)
        return smoothed