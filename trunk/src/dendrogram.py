#! /usr/bin/python

from matplotlib.pyplot import show
import hcluster
import numpy
from numpy.random import rand

class dendrogram:
    def __init__(self, ft_vector, inst_vectors):
        self.ft_vector  = ft_vector
        self.inst_vectors   = inst_vectors

    def maketree(self):
        X   = []
        for inst in self.inst_vectors:
            small_x = []
            for key in self.ft_vector:
                small_x.append(self.inst_vectors[inst][0][key])
            X.append(small_x)
        self.plot(X)
  
    def plot(self, X):
        Y   = hcluster.distance.pdist( X )
        Z   = hcluster.hierarchy.linkage( Y )
        hcluster.hierarchy.dendrogram(Z)
        show()


if __name__ == '__main__':
    '''
    X = rand( 5, 3 )
    X[0:5, :] *= 2
    Y = hcluster.distance.pdist( X )
    Z = hcluster.hierarchy.linkage( Y )
    hcluster.hierarchy.dendrogram(Z)
    show()
    '''
