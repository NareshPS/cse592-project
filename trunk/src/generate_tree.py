from ete2a1 import Tree ,TextFace,NodeStyle

class generate_tree:
  def __init__(self):
    pass

  def mktreeNode(self, tuples):
    t       = Tree()
    nstyle  = NodeStyle()
    nstyle["shape"]   = "sphere"
    nstyle["size"]    = 10
    nstyle["fgcolor"] = "darkred"

    # Gray dashed branch lines
    nstyle["hz_line_type"]  = 1
    nstyle["hz_line_color"] = "#cccccc"
    t.set_style(nstyle)
    if len(tuples) == 1:
      t.name  = '(' + tuples[0][0]+ ',' + tuples[0][1] + ')'
    t.name    = ""
    return t

  def build_interm_nodes(self, cluster, l, l_nodes=None):
    print l
    mergedNode      = [x for x in cluster[l-1] if x not in cluster[l]]
    candidateNodes  = [x for x in cluster[l] if x not in cluster[l-1]]
    n_nodes         = []
    for x in cluster[l]:
      if x in cluster[l-1]:
        n_nodes.append(l_nodex [cluster[l-1].index(x))
      else:
        n_nodes.append(self.mktreeNode(x))
    for candidate in candidateNodes:
      l_nodes [cluster[l-1].index(mergedNode[0])].add_child(n_nodes[cluster[l].index(candidate)])

    if l==len(cluster)-1:
      return
    self.build_interm_nodes(cluster, l+1, n_nodes)

  def build_tree(self, cluster, l, node=None):
    l_nodes = [self.mktreeNode(x) for x in cluster[l]]
    self.build_interm_nodes(cluster, l+1, l_nodes)
    return l_nodes[0]
       
    '''
    N   = len(cluster)
    if l == N-2:
      return self.t 
    mergedNode      = [x for x in cluster[l] if x not in cluster[l+1]]
    candidateNodes  = [x for x in cluster[l+1] if x not in cluster[l]]
    candidate1      = [x for x in cluster[l+1] if x not in cluster[l+2]]
    if node is None:
      self.t  = self.mktreeNode(mergedNode[0])
      node    = self.t
    c1  = self.mktreeNode(candidateNodes[0])
    c2  = self.mktreeNode(candidateNodes[1])
    node.add_child(c1)
    node.add_child(c2)
    try:
      if candidateNodes.index(candidate1[0]) is 0:
        node  = c1
      else:
        node  = c2
    except ValueError:
      node  = self.mktreeNode(candidate1[0]) 
    self.build_tree(cluster, l+1, node)
    '''
