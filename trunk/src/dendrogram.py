#! /usr/bin/python

from matplotlib.pyplot import show
from scipy.spatial.distance import pdist
from scipy.cluster import hierarchy
from numpy.random import rand

import matrixops

class dendrogram:
    def __init__(self, ft_vector, inst_vectors):
        self.ft_vector  = ft_vector
        self.inst_vectors   = inst_vectors

    def maketree(self):
        Y   = []
        inst_keys   = self.inst_vectors.keys()
        len_keys    = len(inst_keys)
        for inst in inst_keys[:len_keys-1]:
            for ainst in inst_keys[inst_keys.index(inst)+1:len_keys]:
                Y.append(matrixops.matrixops.euclideandistance(self.inst_vectors[inst][0], self.inst_vectors[ainst][0]))

        self.plot(Y)
  
    def plot(self, Y):
        Z   = hierarchy.linkage( Y )
        hierarchy.dendrogram(Z)
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
