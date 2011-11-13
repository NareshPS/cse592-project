#! /usr/bin/python

import os, sys
from comicreader import *
from config.siteconfig import *
from collections import defaultdict
import PorterStemmer
import stopwords

class main:
    def __init__(self):
        self.ps = PorterStemmer.PorterStemmer()
        self.st = stopwords.stopwords()

    def add_to_vector(self, text, ft_vector=None, vt=None):
        for part in text.split():
            strip_part  = part.strip()
            st_word     = self.ps.stem(strip_part, 0, len(strip_part)-1)
            if self.st.isstopword(strip_part) is False and self.st.isstopword(st_word) is False and (len(st_word)>2) is True:
                if ft_vector is not None:
                   ft_vector[st_word]   = ft_vector[st_word]+1
                if vt is not None:
                    try:
                        idx     = vt[st_word].index(strip_part)
                    except ValueError:
                        vt[st_word].append(strip_part)

    def launch_readers(self, callback, ft_vector=None, vt=None):
        '''
            Reads various comics.
        '''
        print 'Launching Readers.'
        for tup in COMIC_READERS:
            object  = globals()[tup[0]]
            print 'Processing: ' + tup[0] + " Value: " + tup[1]
            callback(getattr(object,tup[0])(tup[1]), ft_vector, vt)

    def init_ft_vector(self, reader_obj, ft_vector=None, vt=None):
        '''
            Launch readers to read comic files.
        '''
        reader_obj.connect()
        inst    = reader_obj.get_next_instance()
        while inst != None:
            self.add_to_vector(inst[2], ft_vector, vt)
            inst    = reader_obj.get_next_instance()
        reader_obj.disconnect()

    def run_cluster(self):
        ft_vector_dict  = defaultdict(int)
        stem_words      = defaultdict(list)
        self.launch_readers(self.init_ft_vector, ft_vector_dict, stem_words)
        fp  = open(os.path.join(PROJECT_PATH, SRC_DIR, FT_VECTOR), 'w')
        for key in ft_vector_dict.keys():
            fp.write(key + ' ' + str(ft_vector_dict[key]) + '\n')
        fp.close()

        fp  = open(os.path.join(PROJECT_PATH, SRC_DIR, STEM_LIST), 'w')
        for key in stem_words.keys():
            fp.write(key + ' ' + str(stem_words[key]) + '\n')
        fp.close()
        
if __name__ == '__main__':
    if os.path.join(PROJECT_PATH, SRC_DIR) != os.getcwd():
        print 'Run from ' + PROJECT_PATH + SRC_DIR
    else:
        m   = main()
        m.run_cluster()
