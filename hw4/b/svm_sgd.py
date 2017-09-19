#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import sys
from sklearn import svm
import numpy as np
import scipy as sp
import scipy.sparse
from pandas import *
from sklearn.linear_model import SGDClassifier
from scipy.sparse import csr_matrix

#input trian data
content=[]
f=open('train','r')
index=0
for line in f:
    label=line.split(' ',1)[0]
    feature=line.split(' ',1)[1].split(' ')
    content.append([label,feature[0:-1]])
    index+=1

featuredic={}
test_featuredic={}
labellist=[]
test_labellist=[]
for i in xrange(len(content)):   
    feature={}
    for j in content[i][1]:
        feature[int(j.split(':')[0])]=1
    labellist.append(int(content[i][0]))
    featuredic[i]=feature

df = DataFrame(featuredic).T.fillna(0)
m=csr_matrix(df)
print m.shape
y=np.array(labellist)
print y
x = m
#SGD
clf = SGDClassifier(loss="hinge", penalty="l2")
clf.fit(x, y)
pre_f=open('test','r')
pre_feature={}
index=0
for line in pre_f:
    itemlist=line.split('\t')
    feature={}
    for i in itemlist:
        feature[int(i.split(':')[0])]=1
    feature[123]=0
    pre_feature[index]=feature
    index+=1
pre_df = DataFrame(pre_feature).T.fillna(0)

fout = open('svm_sgd_result.txt','w')
pre_m=csr_matrix(pre_df)
print pre_m.shape
pre=clf.predict(pre_m)
#output
for i in pre:
    fout.write(str(i)+'\n')
    print i
