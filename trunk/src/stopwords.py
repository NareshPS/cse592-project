#! /usr/bin/python

from config import siteconfig

class stopwords:
  '''
    stopwords
    ---------
    This class reads stop words file from the disk and 
    creates a dictionary of the stop words. The choice of
    dictionary to store words is based on the requirement
    of efficiently query if a word is stop word.
    stopFh    : Handle to stop words file.
    stopDict  : Dictionary of stop words.
  '''
  stopFh     = None
  stopDict     = {}
  def __init__(self):
    '''
      Opens siteconfig.STOP_WORDS files.
      Each line of the file contains a stop word.
      Ignore the lines starting with '|'
    '''
    self.stopFh = open(siteconfig.STOP_WORDS, 'r')

    #Populate self.stopDict with stopwords.
    for line in self.stopFh.readlines():
      if len(line.strip()) > 0 and line.strip()[0] != '|':
        key = line.split('|')[0].strip()
        self.stopDict[key]  = True

  def isstopword(self, word):
    '''
      This function serves to check if a word is stopword or not.
      word    : word to be checked for stop word.
    '''
    try:
      if self.stopDict[word.strip()] is True:
        return True
    except KeyError:
      return False


if __name__ =='__main__':
  s   = stopwords()
  print s.isstopword('your')
  print s.isstopword('gotohell')





    
    
