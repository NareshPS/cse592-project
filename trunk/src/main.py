#! /usr/bin/python

import os, sys
from collections import defaultdict
import pickle

from comicreader import *
from config.siteconfig import *
import PorterStemmer
import stopwords
import matrixops
import dendrogram

class main:
    def __init__(self):
        self.ft_vector_dict = defaultdict(int)
        self.stem_words     = defaultdict(list)
        self.ps = PorterStemmer.PorterStemmer()
        self.st = stopwords.stopwords()
        self.inst_vectors   = {}

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

    def doc_ft_vector(self, reader_obj, ft_vector=None, vt=None):
        '''
            Launch readers to get each document's
            feature vector.
        '''
        reader_obj.connect()
        inst    = reader_obj.get_next_instance()
        while inst != None:
            inst_vector = defaultdict(int)
            self.add_to_vector(inst[2], inst_vector, None)
            self.inst_vectors[inst[1]]  = (inst_vector, len(inst[2].split())) 
            inst    = reader_obj.get_next_instance()
        reader_obj.disconnect()

    def run_cluster(self):
        '''
            Compute the main Feature Vector.
        '''
        ft_path     = os.path.join(PROJECT_PATH, SRC_DIR, FT_VECTOR)
        st_path     = os.path.join(PROJECT_PATH, SRC_DIR, STEM_LIST)
        if os.path.exists(ft_path) is False:
            self.launch_readers(self.init_ft_vector, self.ft_vector_dict, self.stem_words)
            fp  = open(ft_path, 'w')
            for key in self.ft_vector_dict.keys():
                if self.ft_vector_dict[key]<=1:
                    del(self.ft_vector_dict[key])
            pickle.dump(self.ft_vector_dict, fp)
            fp.close()

            fp  = open(st_path, 'w')
            for key in self.stem_words.keys():
                fp.write(key + ' ' + str(self.stem_words[key]) + '\n')
            fp.close()
        else:
            print 'Loading: ' + ft_path
            fp  = open(ft_path, 'r')
            self.ft_vector_dict = pickle.load(fp)
            fp.close()
            print 'Loaded: ' + ft_path

        '''
            Compute individual documents feature vector.
        '''
        inst_file   = os.path.join(PROJECT_PATH, SRC_DIR, INST_VECTORS)
        if os.path.exists(inst_file) is False:
            inst_fp = open(inst_file, 'w')
            self.launch_readers(self.doc_ft_vector)
            pickle.dump(self.inst_vectors, inst_fp)
            inst_fp.close()
        else:
            print 'Loading: ' + inst_file
            inst_fp = open(inst_file, 'r')
            self.inst_vectors   = pickle.load(inst_fp)
            inst_fp.close()
            print 'Loaded: ' + inst_file

        '''
            Make Dendrogram.
        '''
        d   = dendrogram.dendrogram(self.ft_vector_dict, self.inst_vectors)
        d.maketree()
        
if __name__ == '__main__':
    if os.path.join(PROJECT_PATH, SRC_DIR) != os.getcwd():
        print 'Run from ' + PROJECT_PATH + SRC_DIR
    else:
        m   = main()
        m.run_cluster()
