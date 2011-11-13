import os
from comicreader import xkcd_reader
from comicreader import cnh_reader

PROJECT_PATH    = '/home/naresh/cse592/project/'
DATA_DIR        = 'comics'
SRC_DIR         = 'src'
FT_VECTOR       = 'ft_vector.txt'
STOP_WORDS      = "stop.txt"

COMIC_READERS   = {
    'xkcd_reader': os.path.join(PROJECT_PATH, DATA_DIR, 'xkcd_comic_list.txt'),
    'cnh_reader': os.path.join(PROJECT_PATH, DATA_DIR, 'cnh.txt')
    }
