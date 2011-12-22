#! /usr/bin/python
from nltk import wordpunct_tokenize
from nltk.model.ngram import NgramModel
from nltk.probability import WittenBellProbDist
from math import pow

class model:
  '''
    This class builds language model for the supplied corpus.
    It uses NLTK to build the model.
  '''
  def __init__(self):
    pass
  
  def build_model(self, text):
    c = wordpunct_tokenize(text)
    e = lambda fdist, bins: WittenBellProbDist(fdist, len(fdist)+1)
    m = NgramModel(1, c, e)
    return m

  def ppx(self, m, text):
    '''
      Returns the perplexity of text
      in the given model.
      
      m     : model
      text  : text
    '''
    print 1/pow(m.entropy(text), 2.0)

if __name__ == '__main__':
  m   = model()
  print m
