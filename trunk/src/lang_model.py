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
  
  def discount(self, fdist, bins):
    return WittenBellProbDist(fdist, len(fdist)+1)

  def build_model(self, text):
    c = wordpunct_tokenize(text)
    m = NgramModel(1, c, self.discount)
    return m

  def ppx(self, m, text):
    '''
      Returns the perplexity of text
      in the given model.
      
      m     : model
      text  : text
    '''
    c = wordpunct_tokenize(text)
    if len(c) == 0:
      return 0.0
    return pow(2.0, m.entropy(c))

if __name__ == '__main__':
  m   = model()
  print m
