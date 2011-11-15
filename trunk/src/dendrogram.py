#! /usr/bin/python

from matplotlib.pyplot import show
from scipy.spatial.distance import pdist
from scipy.cluster import hierarchy
from numpy.random import rand
import math
import copy
from config.siteconfig import *
import pickle

class dendrogram:
    def __init__(self, ft_vector, inst_vectors):
        self.ft_vector  = ft_vector
        self.inst_vectors   = inst_vectors

    def maketree(self):
        Y   = None
        dist_vc_path    = os.path.join(PROJECT_PATH, SRC_DIR, DIST_VECTORS)
        if os.path.exists(dist_vc_path) is False:
            Y   = []
            inst_keys   = self.inst_vectors.keys()
            len_keys    = len(inst_keys)
            for inst in inst_keys[:len_keys-1]:
                for ainst in inst_keys[inst_keys.index(inst)+1:len_keys]:
                    inst_v  = copy.deepcopy(self.inst_vectors[inst][0])
                    ainst_v = copy.deepcopy(self.inst_vectors[ainst][0])
                    Y.append(math.sqrt(sum((inst_v[x]-ainst_v[x])*(inst_v[x]-ainst_v[x]) for x in set(inst_v.keys()+ainst_v.keys()))))
            fp  = open(dist_vc_path, 'w')
            pickle.dump(Y, fp)
            fp.close()
        else:
            print 'Loading: ' + dist_vc_path 
            fp  = open(dist_vc_path, 'r')
            Y   = pickle.load(fp)
            fp.close()
            print 'Loaded: ' + dist_vc_path 

        self.plot(Y)
  
    def plot(self, Y):
        Z   = hierarchy.linkage( Y )
        hierarchy.dendrogram(Z,truncate_mode='level', p=10, show_contracted=True)
        show()

if __name__ == '__main__':
    X = [[1.0],[1.0],[2.0],[4.0],[9.0]]
    print 'Vectors'
    print X
    Y = pdist( X )
    print 'Distance'
    print Y
    Z = hierarchy.linkage( Y )
    hierarchy.dendrogram(Z)
    show()
