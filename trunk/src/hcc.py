from copy import copy

class hcc:
  '''
    This class clusters the input features using
    hierarchial co-clustering. It uses the algorithm
    described by Jingxuan Li and Tao Li in their paper
    'HCC: A Hierarchical Co-Clustering Algorithm'. They
    improve the algorithm described in 
    'An error variance approach to two-mode hierarchical clustering'
    The papers is available at:
    http://users.cs.fiu.edu/~taoli/pub/sigir10-p861-li.pdf
    http://www.springerlink.com/content/v3q6u7820u35x327/

    It takes as input, the corpus-wide feature vector 
    consisting of words and their frequency count. It also
    takes as input document feature vectors. Document feature
    vectors are sparse.
    It starts with computing TF-IDF on the input vectors to create
    a relationship matrix describing the relation between 
    words and documents.
      The matrix X[i,j] = (x[i,j]). The values for each cell are 
      acquired using self.call callback. It doesn't compute the 
      matrix at once, but does it when the value requires computation.
  '''
  def __init__(self, callback, v_ft, v_in):
    '''
      init function for the class.
      v_ft    : corpus-wide feature vector.
      v_in    : instance-wide feature vector.
    '''
    self.v_ft   = v_ft
    self.v_in   = v_in
    self.call   = callback
    self.center = None

  def compute_centroid(self):
    if self.center is None:
      self.center = max([self.call(self.v_ft, self.v_in, x,y) for x in self.v_ft [0] for y in self.v_in])
    return self.center

  def compute_ch(self, p, q):
    '''
      In this function we compute cluster heterogeneity.
        CH(C) = (1/mn)*sum(square(x[i,j] - mu))
        mu    = Max value in the termXdocument matrix
    '''
    xs  = [self.call(self.v_ft, self.v_in, x,y) for x in p[0]+q[0] for y in p[1]+q[1]]
    return (1.0/float((len(p[0])+len(q[0]))*(len(p[1])+len(q[1]))))*sum([pow(x-self.compute_centroid(),2) for x in xs])

  def pickup_two_nodes(self, m):
    '''
      Pickup two nodes with minimum value of CH.
      Call compute_ch to get CH values.
    '''
    ch_vals = [(self.compute_ch(p,q),p,q) for p in m if len(p [0])!=0 for q in m if len(q [1])!=0 and p!=q]
    ch_sort = sorted(ch_vals, key=lambda ch: ch[0])
    return (ch_sort[0][1], ch_sort[0][2])
     
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
    for i in range(0,N-1):
      m     = copy(l)
      l     = m
      p, q  = self.pickup_two_nodes(m)
      o     = self.merge(p, q)
      m.remove(p)
      m.remove(q)
      m.append(o)
      cluster.append(m)
    return cluster
