#! /usr/bin/python

import os, sys
from comicreader import *
from config.siteconfig import *
from collections import defaultdict
import PorterStemmer
import stopwords

ft_vector_dist  = defaultdict(int)
ps  = PorterStemmer.PorterStemmer()
st  = stopwords.stopwords()

def add_to_vector(text):
    for part in text.split():
        if st.isstopword(part.strip()) is False:
            word    = ps.stem(part, 0, len(part)-1)
            if st.isstopword(word) is False:
                if len(word)>2:
                    ft_vector_dist[word]    = ft_vector_dist[word]+1

def launch_readers():
    '''
        Reads various comics.
    '''
    print 'Launching Readers.'
    for key in COMIC_READERS.keys():
        object  = globals()[key]
        reader_start(getattr(object,key)(COMIC_READERS[key]))

def reader_start(reader_obj):
    '''
        Launch readers to read comic files.
    '''
    reader_obj.connect()
    inst    = reader_obj.get_next_instance()
    while inst != None:
        add_to_vector(inst[2])
        inst    = reader_obj.get_next_instance()
    reader_obj.disconnect()

if __name__ == '__main__':
    if os.path.join(PROJECT_PATH, SRC_DIR) != os.getcwd():
        print 'Run from ' + PROJECT_PATH + SRC_DIR
    else:
        launch_readers()
        fp  = open(os.path.join(PROJECT_PATH, SRC_DIR, FT_VECTOR), 'w')
        for key in ft_vector_dist.keys():
            fp.write(key + ' ' + str(ft_vector_dist[key]) + '\n')

        fp.close()
