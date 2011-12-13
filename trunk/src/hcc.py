from math import log
from copy import copy

class hcc:
  '''
    This class clusters the input features using
    hierarchial co-clustering. It uses the algorithm
    described by Jingxuan Li and Tao Li in their paper
    'HCC: A Hierarchical Co-Clustering Algorithm'.
    The paper is available at:
    http://users.cs.fiu.edu/~taoli/pub/sigir10-p861-li.pdf

    It takes as input, the corpus-wide feature vector 
    consisting of words and their frequency count. It also
    takes as input document feature vectors. Document feature
    vectors are sparse.
    It starts with computing TF-IDF on the input vectors to create
    a relationship matrix describing the relation between 
    words and documents.
      The matrix X[i,j] = (x[i,j]) for each i in corpus-wide feature vector
      and each j in input documents. Each element of the matrix is 
      tf-idf value for the word and that document. It doesn't compute the 
      matrix at once, but does it when the value requires computation.
  '''
  def __init__(self, v_ft, v_in):
    '''
      init function for the class.
      v_ft    : corpus-wide feature vector.
      v_in    : instance-wide feature vector.
    '''
    self.v_ft   = v_ft
    self.v_in   = v_in

  def tfidf(self, w, d):
    '''
      Computes tf-idf value for a cell given by X[w,d].
      w   : word
      d   : document
    '''
    tf  = float(self.v_ft [0][w][1])
    idf = log(float(self.v_ft [1])/tf)
    return tf*idf

  def compute_ch(self, m):
    '''
      In this function we compute cluster homogeniety.
        CH(C) = (1/mn)*sum(square(x[i,j] - mu))
        mu    = Avg(x[i,j])
    '''
    print m
    xs  = None
    [self.tfidf(x,y) for x in m[0] for y in m[1]]
    mu  = sum(xs)/float(len(xs))
    print xs, mu
    return 1.0
    #return ((1.0/float(len(m[0])*len(m[1])))*float(sum(pow((),2.0))))


  def pickup_two_nodes(self, m):
    '''
      Pickup two nodes with minimum value of CH.
    '''
     
  def merge(self, p, q):
    '''
      This function returns the merged cluster
      of p and q.
      For merging, it merges the two components separately
      The two components being, document part of cluster and
      term part of cluster.
    '''
    return (p[0]+q[0], p[1]+q[1])

  def hcc_cluster(self):
    '''
      This function runs the clustering algorithm. The algorithm
      is described below:
      Algorithm 1 HCC Algorithm Description
      -------------------------------------
      Create an empty hierarchy H
      List <- Objects in A + Objects in B
      N <- size[A] + size[B]
      Add List to H as the bottom layer
      for i = 0 to N - 1 do
        p, q = PickUpTwoNodes(List)
        o = Merge(p, q)
        Remove p, q from List
        Add o to List
        Add List to H at a higher layer
      end for
      -------------------------------------
    '''
    v_ft  = self.v_ft
    v_in  = self.v_in
    #Create bottom layer of the cluster.
    #Bottom layer contains all the words and documents.
    l       = [([x],[]) for x in v_ft [0]]
    l.append('')
    l[-1:]  = [([],[x]) for x in v_in]
    N       = len(l)
    cluster = [l]
    for i in range(0,N):
      m     = copy(l)
      l     = m
      p, q  = self.pickup_two_nodes(m)
      o     = self.merge(p, q)
      del m[p]
      del m[q]
      cluster.append(m)
    print cluster
