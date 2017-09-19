import numpy as np
import scipy as sp
import scipy.sparse

def pmf(R, U, V, K, iterations , alpha , lamdaU , lamdaV ):
    V = V.T
    n,m=R.shape
    user=R.nonzero()[0]
    movie=R.nonzero()[1]
    score=R.data

    mse=0
    minE=10000000
    minU=U
    minV=V
    for iteration in range(iterations):
        e=0
        for x in range(len(score)):
            #score value:score[x]
            i=user[x]     # row
            j=movie[x]    #colum
            Rij=(score[x]-1)/4
            eij=Rij-1/(1+np.exp(-np.dot(U[i,:],V[:,j])))    #error in [Rij]
            mse=mse+eij**2

            for k in range(K):
                e = e + lamdaU / 2 * (U[i][k] ** 2) + lamdaV / 2 * (V[k][j] ** 2)
            e = e + eij ** 2      #PMF objective function
            for k in range(K):   #find optimal U,V by natral gradient descent
                U[i][k] = U[i][k] + alpha * (2 * eij * V[k][j] - lamdaU * U[i][k])
                V[k][j] = V[k][j] + alpha * (2 * eij * U[i][k] - lamdaV * V[k][j])

            #print "e:",e
        if minE>e:
            minE=e
            minU=U
            minV=V
        if e < 0.01:
            print "reach the minimun e",e
            break

        print "interation:",iteration,"minE:",minE
    return minU, minV.T

def rmse(test_data, U,V):
    '''Calculate root mean squared error.
        Ignoring missing values in the test data.
        '''

    mse=0
    #f=open('test_rating.txt','w')
    for i in range(len(test_data.data)):
        row=test_data.nonzero()[0][i]
        col=test_data.nonzero()[1][i]

        score=np.dot(U[row],V[:,col])
        score = 1/(1+np.exp(-score))
        score=score*6+1                                           
        #print test_data.data[i],score   
        #f.write(str(score)+'\n')
        #f.flush()

        sqerror=test_data.data[i]-score
        mse = mse+sqerror**2

    n=len(data.data)
    return np.sqrt(mse/n)
    

def rmse_test(real,predict):
    Rmse=0
    mse = 0
    for i in range(len(real)):
        #print real[i],predict[i]
        mse=mse+(real[i]-predict[i])**2
    Rmse=np.sqrt(mse/len(real))
    print Rmse

def read_train_data():
    '''considering time-consuming problem,just only read q train data ,which q%5==1 '''
    f=open('train.dat','r')
    count=0
    content=list()
    for line in f.readlines():
        count+=1
	if count % 5==1 :continue
	content.append(line)
     #   if count>=10000:break
    print "content reading end"
    data1={}
    movies={}
    users={}
    user_list=list()

    movies_list=list()
    score_list=list()
    for item in content:


        user=item.split('\t')[0]
        movie=item.split('\t')[1]
        score=item.split('\t')[2].strip()


        if movies.get(movie) is None:
            movies[movie]=len(movies)

        movies_list.append(movies[movie])

        if users.get(user) is None:
            users[user]=len(users)

        user_list.append(users[user])
        score_list.append(float(item.split('\t')[2].strip()))
        #print (users[user],movies[movie])
    data=sp.sparse.coo_matrix((score_list,(user_list,movies_list)))
    return data,users,movies

def read_test_data(users,movies,U,V):
    '''because we donot know the exact real test data, so we use train data to do RMSE to evaluate the quality of this method
              considering time-consuming problem,just only read q train data ,which q%5==1 '''#have delete later for predicting
    f=open('test.dat','r')
    f1=open('test_rating.txt','w')
    count=0
    content=list()
    for line in f.readlines():
        count+=1
	#if count % 5 !=1: continue
        content.append(line)
      #  if count>=10000:break
    print "content reading end"
    #score=np.mean(np.dot(U,V))+0.25

    score=np.dot(np.mean(U,axis=0),np.mean(V,axis=1))
    score = 1/(1+np.exp(score))
    score=score*6+1                                                  ######!!!!4-8
    #print score
    real=list()
    predict=list()
    row=0
    col=0
    maximum=0
    minimun=5

    for item in content:
        user=item.split('\t')[0]
        movie=item.split('\t')[1].strip()
        #score=float( item.split('\t')[2].strip())
        real.append(score)

        if movies.get(movie) is None:
            movie_col=np.mean(V,axis=1)

        else:
            col=movies[movie]
            movie_col=V[:,col]


        if users.get(user) is None:

            user_row=np.mean(U,axis=0)

        else:
            row=users[user]
            user_row=U[row]

        #if col==0 and row==0:continue
        score=np.dot(user_row,movie_col)
        score = 1/(1+np.exp(score))
        score=score*6+1                                 #####!
        predict.append(score)

        f1.write(str(score)+'\n')
        f1.flush()
        #print "position:",(row,col),len(U[row]),len(V[:,col]),score
        if score < minimun: minimun=score
        if score > maximum: maximum=score
    f1.close()
    #print minimun, maximum
    #print 'train data predition results:'
    rmse_test(real,predict)


#set dimension
K =10

#get N,M to calculate U, V
data,users,movies=read_train_data()
N, M = data.shape
print N, M

#initialize U ,V
sigma_R =0.01
sigma_P =1
sigma_Q =1
P =np.random.randn(N, K)*sigma_P
Q =np.random.randn(M, K)*sigma_Q
lambda_P =sigma_R**2 / sigma_P**2
lambda_Q =sigma_R**2 / sigma_Q**2
print lambda_P,lambda_Q



R=data
U, V = pmf(R, P, Q, K,30,0.005,lambda_P,lambda_Q)
'''use train data to test RMSE'''
print rmse(R,U,V.T)

read_test_data(users,movies,U,V.T)

