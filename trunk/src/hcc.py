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
  def __init__(self, callback, v_series, v_docs):
    '''
      init function for the class.
      v_ft    : corpus-wide feature vector.
      v_in    : instance-wide feature vector.
    '''
    self.v_series = v_series
    self.v_docs   = v_docs
    self.call     = callback

  def compute_centroid(self, cluster):
    '''
      Compute centroid.
      Centroid is the center of the cluster. Mathematically,
      it is the average of distances between the cluster nodes.
      It would have lesser value for tight clusters.
    '''
    mu  = 0.0
    for n in cluster:
      mu  += self.call(n[0], n[1])
    return mu/len(cluster) 

  def compute_ch(self, p, q):
    '''
      In this function we compute cluster heterogeneity.
        CH(C) = (1/mn)*sum(square(x[i,j] - mu))
        mu    = Max value in the termXdocument matrix
    '''
    xs  = 0.0
    mu  = self.compute_centroid(p+q)
    for n in p+q:
      xs  += pow(self.call(n[0], n[1])-mu, 2)
    return (1.0/float(2*(len(p)+len(q))))*xs

  def pickup_two_nodes(self, m):
    '''
      Pickup two nodes with minimum value of CH.
      Call compute_ch to get CH values.
    '''
    len_m   = len(m)
    nodes   = None
    m_val   = None
    for p_in in range(0, len_m):
      for q_in in range(p_in+1, len_m):
        c_val     = self.compute_ch(m [p_in], m[q_in])
        if m_val is None or c_val < m_val:
          m_val   = c_val
          nodes   = (m [p_in],m [q_in])
    return nodes
     
  def merge(self, p, q):
    '''
      This function returns the merged cluster
      of p and q.
      For merging, it merges the two components separately
      The two components being, document part of cluster and
      term part of cluster.
    '''
    return p+q

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
      We also populate another matrix which is used
      as relationship matrix for document-series clustering.
      The value is computed based on the clusters
      obtained from word-document clustering.
      First, we initializes the matrix to 0.0 values.
      Then, we add up the level at which cluster has has been
      merged. We add up the level value to each document series
      pair in the corss-product of documentXseries for the new cluster.
    '''
    v_series  = self.v_series
    v_docs    = self.v_docs
      
    #Create bottom layer of the cluster.
    #Bottom layer contains all the words and documents.
    m       = [[(x,y)] for x in v_series for y in v_docs]
    N       = len(m)
    cluster = [m]
    for i in range(0,N-1):
      print i, ' of ', N
      m     = copy(m)
      p, q  = self.pickup_two_nodes(m)
      o     = self.merge(p, q)
      m.remove(p)
      m.remove(q)
      m.append(o)
      cluster.append(m)
    return cluster
