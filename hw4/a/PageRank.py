import numpy as np

#1)input:directed graph and parameter beta
beta = 0.9
dic = np.loadtxt("web-Google.txt",dtype='int')
dic_1 = dic[:,0]
dic_2 = dic[:,1]
from_nodes = np.sort(dic_1)
node_ind = np.argsort(dic_1)
to_nodes = dic_2[node_ind]
dic_sorted = np.transpose(np.vstack([from_nodes, to_nodes]))

all_nodes = np.sort(dic_sorted, axis=None)
fdn, f_counts = np.unique(from_nodes,return_counts=True)
aln = np.unique(all_nodes)
array_l=len(aln)
r_old = np.ones((array_l),dtype=float)/array_l
epson = 1

#2)output :pagerank 
while epson>0.0001:
	dic_count = 0
	for i in range(len(fdn)):
            print 'i =', i
	    r_new = (1-beta)*np.ones((array_l),dtype=float)/array_l
	    f_ind = np.argwhere(aln==fdn[i])
	    add = r_old[f_ind]/f_counts[i]
	    for j in range(f_counts[i]):
                print 'j = ', j
		to_ind = np.argwhere(aln==to_nodes[dic_count])
		r_new[to_ind]+=beta*add
		dic_count+=1
        diff_r = r_new - r_old
        epson = np.dot(np.transpose(diff_r),diff_r)/np.dot(np.transpose(r_old),r_old)
        r_old = r_new
        print 'epson=', epson

indice = np.argsort(r_new)

sorted_scores = np.sort(r_new)
sorted_nodes = aln[indice]
for i in range(array_l):
   index = -i-1
   print sorted_nodes[index], sorted_scores[index]

