#spectral_clustering:
#1)consruct a matrix representation of the graph;
#2)matrix decomposition:compute eigenvalue and eigenvectors of the matrix,map each point to a lower dimension
#3)clustering
import time,operator
import networkx as nx
import numpy as np
import scipy,time
from scipy.sparse.linalg import eigs
from sklearn.cluster import KMeans

#construct a grapgh of data
def parse(filename):
    G = nx.Graph()
    data = open(filename)
    n1 = []
    n2 = []
    edges=[]
    for i, rows in enumerate(data):
        if '#' in rows:
            continue
        rows = rows.strip().split('\t')
        node_a = int(rows[0])
        node_b = int(rows[1])
        G.add_edge(node_a, node_b)
    return G

#consruct a matrix representation of the graph
def getLaplacian(m):
    print time.ctime()
    d=[row.sum() for row in m]  
    print time.ctime()
    D=scipy.sparse.diags(d,0)
    print D
    print time.ctime()
    L=D-m
    print time.ctime()
    return L

#matrix decomposition 
def getLowerDimension(w,k):
    print w.shape
    eigValue,eigVec = eigs(w,k=100,which='LR')
    import cPickle
    print 'finished'
    print time.ctime()
    dim = len(eigValue)
    print dim
    print eigValue
    return eigVec

if __name__ == '__main__':
    print time.ctime()
    graph = parse('com-youtube.ungraph.txt')
    laplacianMat = nx.laplacian_matrix(graph)
    print time.ctime()
    print time.ctime()
    fout = open('spectral_clustering_result.txt','w')
    np_matrix = nx.to_scipy_sparse_matrix(graph,dtype=np.float32)
    print 'begin'
    lapW = getLaplacian(np_matrix)
    print 'end'
    reduced_matrix = getLowerDimension(lapW,100)
    print reduced_matrix.shape
    print time.ctime()
    #use Kmean to clustering
    kmeans_model = KMeans(n_clusters=100,init='k-means++',n_init=10).fit(reduced_matrix)
    print time.ctime()
    count=0
    for i in kmeans_model.labels_:
        count=count+1
        fout.write(str(count)+'	'+str(i)+'\n')
