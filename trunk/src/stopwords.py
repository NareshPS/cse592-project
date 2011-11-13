#! /usr/bin/python

from config import siteconfig

class stopwords:
    stopFh         = None
    stopDict       = {}
    def __init__(self):
        self.stopFh = open(siteconfig.STOP_WORDS, 'r')

        for line in self.stopFh.readlines():
            if len(line.strip()) > 0 and line.strip()[0] != '|':
                key = line.split('|')[0].strip()
                self.stopDict[key]  = True

    def isstopword(self, word):
        try:
            if self.stopDict[word.strip()] is True:
                return True
        except KeyError:
            return False


if __name__ =='__main__':
    s   = stopwords()
    print s.isstopword('your')
    print s.isstopword('gotohell')





        
        
