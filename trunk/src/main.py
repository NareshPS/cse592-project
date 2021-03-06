#! /usr/bin/python

import os,sys

from comicreader import *
from config.siteconfig import *
from save_object import save_object
from PorterStemmer import PorterStemmer
from stopwords import stopwords
from hcc import hcc
from math import log
from lang_model import model
from generate_tree import generate_tree

class main:
  def __init__(self):
    '''
      self.saver    : Pickles the object on to the disk.
      self.ps       : Porter stemmer class object. It is required to get stem of a word.
      self.st       : Class object to check for stop words.
    '''
    self.saver  = save_object()
    self.ps     = PorterStemmer()
    self.st     = stopwords()
    self.m_ds   = {}
    self.models = {}
    self.m_mod  = model()

  def add_to_vector(self, text, v_ft, v_in, v_st):
    '''
      text    : Text to process. The function splits it into words
                and stores relevant information in v_ft and v_in vectors.
      v_ft    : The corpus-wide feature vector. It is a dictionary.
                Words form key of the dictionary. The value is a tuple.
                The tuple is of the form (total_count, document_count).
                First element contains total word count in all documents.
                Second element contains the number of document in which this
                word appears.
      v_in    : The instance-wide feature vector. Contains the frequency of each
                word in the instance.
      v_st    : step-word mappings. Useful later to understand the results.
    '''
    for part in text.split():
      #Remove leading or trailing spaces and new lines.
      strip_part  = part.strip()
      #Skip if the word is a stop word.
      #Skip if the word is not alpha.
      if self.st.isstopword(strip_part) is False and strip_part.isalpha() is True:
        #Stems the word.
        st_word   = self.ps.stem(strip_part, 0, len(strip_part)-1)
        #Ignore words with 2 characters or less.
        if len(st_word)<2:
          continue

        #Put stem and word in v_st vector.
        if v_st.has_key(st_word):
          v_st [st_word].add(strip_part)
        else:
          v_st [st_word]  = set()
          v_st [st_word].add(strip_part)

        #Update the word count in v_ft if it contains the word.
        #Else add that key to the v_ft vector.
        if v_ft.has_key(st_word):
          tup = v_ft [st_word]
          v_ft [st_word]  = (tup[0]+1, tup[1])
        else:
          v_ft [st_word]  = (1, 0)
      
        #Update the word count in v_in vector.
        #Increment the count if key exists. Create new key otherwise.
        if v_in.has_key(st_word):
          v_in [st_word]  += 1
        else:
          v_in [st_word]  = 1

    #Now, update the document count for each word appearing
    #in the current document.
    for key in v_in.keys():
      tup = v_ft [key]
      v_ft [key]  = (tup[0], tup[1]+1)

  def read_corpus(self, reader_obj, v_ft, v_in, v_st, v_doc, series):
    '''
      Launch readers to read comic files.
      reader_obj    : Object to read instances from a comic.
                      The objects supports get_next_instance()
                      routine which reads the next instance.
      v_ft,v_in,v_st: Output parameters for corpus-wide, instance-wide
                      feature vectors and stem-word mappings.
      docs          : Output parameter for list of documents.
    '''
    reader_obj.connect()
    inst  = reader_obj.get_next_instance()
    i = 0
    count = 1
    while inst != None:
      if count == 10:
        break
      v_ft [1]  += 1
      v_new     = {}
      self.add_to_vector(inst[2], v_ft [0], v_new, v_st)
      v_in [inst[1]]  = v_new
      v_doc [inst[1]] = series
      inst  = reader_obj.get_next_instance()
      count += 1
    reader_obj.disconnect()

  def launch_readers(self, callback, v_ft, v_in, v_st, v_doc):
    '''
      This function calls the callback
      for each Reader. Readers are defined for each
      comic types in the config file. The comic instances
      for each comic types are kept in a single file.
      These Readers configuration also defines common
      interface to read comic instances without knowing
      the details of the actual storage format.
    '''
    print 'Launching Readers.'
    for tup in COMIC_READERS:
      object  = globals()[tup[0]]
      print 'Processing: ' + tup[0] + " Value: " + tup[1]
      callback(getattr(object,tup[0])(tup[1]), v_ft, v_in, v_st, v_doc, tup [1])

  def init_vectors(self, v_ft, v_in, v_st, v_doc):
    '''
      This method computes the global feature vector
      as well as the feature vector for each instance.
      It passes a function pointer self.read_corpus
      which processes each document and stores relevant
      information in the two vectors passed as 
      additional arguments.
      Initializes v_ft. An empty dictionary for current
      state of feature vector and a 0 for document count.

      v_ft    : The global feature vector.
      v_in    : The feature vectors for all individual
                documents.
      v_st    : It contains mapping of stems and corresponding words.
      v_doc   : It contains document-comic mappings.
      These three vectors should be populated when the 
      function returns.
    '''
    if v_ft is None or v_in is None:
      raise Exception('v_ft is None or v_in is None')
    v_ft [0]  = {}
    v_ft [1]  = 0
    self.launch_readers(self.read_corpus, v_ft, v_in, v_st, v_doc)
    '''
      The feature vector would be huge as it contains
      almost all the differnt words in the corpus.
      However, we would like to reduce it to make
      computation simpler and faster.
      So, we remove the words having frequency less than
      or equal to 2. This reduces the Feature Vector 
      by almost a factor of 1/2. We remove these words
      from both the corpus-wide feature vector and
      the document specific feature vector.
    '''
    ft    = v_ft [0]
    for k,v in ft.items():
      if v[0] <= 2:
        del ft[k]

    for k,v in v_in.items():
      for k1,v1 in v.items():
        if ft.has_key(k1) is False:
          del v[k1]
    print 'Total Documents: ', v_ft [1], ' from: ', len(COMIC_READERS), ' different comics'
  
  def doc_len(self, v_in, d):
    c   = 0.0
    for v in v_in[d].values():
      c += v
    return c
  
  def tfidf(self, v_ft, v_in, w, d):
    '''
      Computes tf-idf value for a cell given by X[w,d].
      v_ft  : Tuple of Corpus-wide Feature Vector and corpus size.
      v_in  : Instance-wide feature Vector.
      w     : word
      d     : document
    '''
    tf  = 0.0
    if v_in[d].has_key(w):
      tf  = float(v_in[d][w])/self.doc_len(v_in, d)
    idf = log(float(v_ft [1])/(1.0+v_ft [0][w][1]))
    return tf*idf

  
  def run_cluster(self):
    '''
      Computes the main Feature Vector. Followinf variable are initialized.
      v_ft    : Global feature vector for all documents
                It is a tuple of two elements.
                First Element is a dictionary of words in
                corpus with their counts. Words are stemmed
                before storing in the vector. Stop words
                are removed.
                Second Element of the vector stores the total
                number of documents in the corpus.
      v_in    : Feature vector for each document.
                This is a dictionary object. They keys
                of the vectors are identifier of documents.
                The values are their corresponding feature vectors.
      v_st    : It stores the stems and their corresponding words.
                It is not required for the clustering. But, it would
                be useful for visualizing the results.
      v_doc   : It stores the mapping of document and comics. They key is comic.
                And the value is a list of document in that comic.
    '''
    v_ft  = self.saver.load_it(FT_VECTOR)
    v_in  = self.saver.load_it(INST_VECTORS)
    v_st  = self.saver.load_it(STEM_LIST)
    v_doc = self.saver.load_it(COMIC_VECTORS)
    if v_ft is None or v_in is None or v_st is None:
      v_ft  = {}
      v_in  = {}
      v_st  = {}
      v_doc = {}
      self.init_vectors(v_ft, v_in, v_st, v_doc)
      self.saver.save_it(v_ft, FT_VECTOR)
      self.saver.save_it(v_in, INST_VECTORS)
      self.saver.save_it(v_st, STEM_LIST)
      self.saver.save_it(v_doc, COMIC_VECTORS)
   
    self.m_ds   = self.saver.load_it(CLUSTER_WD)
    if self.m_ds is None:
      #Do word-document clustering. Use hcc class for that.
      c             = hcc(self.tfidf, v_ft, v_in, v_doc, False)
      self.m_ds     = c.hcc_cluster(True)
      self.saver.save_it(self.m_ds, CLUSTER_WD)

    c_ds    = self.saver.load_it(CLUSTER_DS)
    if c_ds is None:
      #Do document-series clustering. Use hcc class for that.
      d   = hcc(self.ds_cell, (v_in, None), set(v_doc.values()), v_doc, True)
      c_ds = d.hcc_cluster(False)
      self.saver.save_it(c_ds, CLUSTER_DS)

  def create_models(self, reader_obj, series, args):
    reader_obj.connect()
    inst  = reader_obj.get_next_instance()
    text  = ''
    while inst != None:
      text  += inst [2]
      inst  = reader_obj.get_next_instance()
    args [series] = self.m_mod.build_model(text)

  def create_rship_matrix(self, reader_obj, series, args):
    '''
      Initialize Relationship matrix.
      Read each document from the corpus and initialize
      the relationship matrix for each pair of
      docment and series.
      The values for matrix cells are returned by the models.
    '''
    reader_obj.connect()
    inst  = reader_obj.get_next_instance()
    text  = ''
    while inst != None:
      text  += inst [2]
      for s in self.models:
        args [s][inst[1]]  = self.m_mod.ppx(self.models[s], inst[2])
      inst  = reader_obj.get_next_instance()

  def launch_corpus_reader(self, callback, args):
    print 'Launching Readers.'
    for tup in COMIC_READERS:
      object  = globals()[tup[0]]
      print 'Processing: ' + tup[0] + " Value: " + tup[1]
      callback(getattr(object,tup[0])(tup[1]), tup[1], args)
  
  def ds_cell(self, series, doc):
    '''
      This function computes cell value for document
      series clusering. It fetches these values from
      self.ds matrix. The self.ds matrix is
      [Num Of Documents]X[Number Of Series] matrix.
      It is populated by init_ds_matrix() method.
    '''
    return self.m_rship[series][doc]

  def run_cluster1(self):
    '''
      This method uses language models to cluster web-comics.
      First, it creates the model for each comic series.
      The models are created using NLTK. Then, it gets the probability
      of each document in the series. This way we get the relationship
      matrix of document and series.
      ext, we run the HCC algorithm to cluster these comics.
    '''
    cluster   = self.saver.load_it(CLUSTER_DS)
    if cluster is None:
      self.m_rship    = self.saver.load_it(RSP_MATRIX)
      if self.m_rship is None:
        self.launch_corpus_reader(self.create_models, self.models)
        self.m_rship        = {}
        for s in self.models:
          self.m_rship [s]  = {}
        self.launch_corpus_reader(self.create_rship_matrix, self.m_rship)
        self.saver.save_it(self.m_rship, RSP_MATRIX)

      #Generate v_series and v_docs vectors.
      v_series  = self.m_rship.keys()
      v_docs    = self.m_rship[self.m_rship.keys()[0]].keys()
      
      #Do word-document clustering. Use hcc class for that.
      c       = hcc(self.ds_cell, v_series, v_docs)
      cluster = c.hcc_cluster()
      self.saver.save_it(cluster, CLUSTER_DS)
    #Create Hierarchial Tree using ETE
    cluster.reverse()
    t     = generate_tree()
    tree  = t.build_tree(cluster, 0)
    tree.show()
    
if __name__ == '__main__':
  #Check if the project is running from correct directory.
  if os.path.join(PROJECT_PATH, SRC_DIR) != os.getcwd():
    print 'Run from ' + PROJECT_PATH + SRC_DIR

  '''
    We store the computed vectors in files.
    And reload them instead of computing them again.
    If code is changed which might affect the vectors,
    please clean up the three vector files.
    Or run the following command.
    $ ./main.py clean
  '''
  cleanup = [FT_VECTOR, INST_VECTORS, STEM_LIST, CLUSTER_WD, CLUSTER_DS, COMIC_VECTORS, RSP_MATRIX, LANG_MODELS]
  if len(sys.argv) == 2 and sys.argv[1] == 'clean':
    for i in cleanup:
      if os.path.exists(i) is True:
        os.remove(i)
  else:
    m   = main()
    m.run_cluster1()
