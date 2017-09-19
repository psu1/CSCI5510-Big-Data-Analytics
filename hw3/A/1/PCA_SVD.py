import os.path
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import linalg


def display(Xrow,fig_name):
    ''' Display a digit by first reshaping it from the row-vector into the image.  '''
    plt.imshow(np.reshape(Xrow,(28,28)))
    plt.gray()
    plt.savefig(fig_name)
    plt.show()

def load_data(digit, num):
    ''' 
    Loads all of the images into a data-array (for digits 0 through 5). 
pyplot
    The training data has 5000 images per digit and the testing data has 200, 
    but loading that many images from the disk may take a while.  So, you can 
    just use a subset of them, say 200 for training (otherwise it will take a 
    long time to complete.

    Note that each image as a 28x28 grayscale image, loaded as an array and 
    then reshaped into a single row-vector.

    Use the function display(row-vector) to visualize an image.
    
    '''
    X = np.zeros((num,784),dtype=np.uint8)   #784=28*28
    print '\nReading digit %d' % digit,
    for i in xrange(num):
        if not i%100: print '.',
        pth = os.path.join('train%d' % digit,'%05d.pgm' % i)
        with open(pth, 'rb') as infile:
            header = infile.readline()
            header2 = infile.readline()
            header3 = infile.readline()
            image = np.fromfile(infile, dtype=np.uint8).reshape(1,784)
        X[i,:] = image
    print '\n'
    return X

'''initalize '''
def zeroMean(X):
    X_mean=np.mean(X,axis=0)
    X_std=X-X_mean
    return X_std,X_mean

'''initial_data'''
digit=0
num=5000

X = load_data(digit, num)
X_std,X_mean=zeroMean(X)

'''plot mean picture'''
fig_name='0_mean'
display(X_mean,fig_name)

'''SVD decompositon'''
U,S,V=linalg.svd(X_std)   
#eigvals=np.diag(S)
print(S.shape )

'''plot eigvals-dimensions'''
x=np.arange(100)
y=S[x]
plt.figure(figsize=(8,5))
plt.plot(x,y,'or')
plt.xlabel('dimension')
plt.ylabel('egivalues')
plt.savefig('eigenvalues_dimensions.png')
plt.show()

'''plot the first 20 eigenvectors'''
for i in xrange(20):

   fig_name = 'eigenvector_'+str(i+1)+'.png'
   display(V[i,:],fig_name)




