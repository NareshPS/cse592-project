import os
from comicreader import xkcd_reader
from comicreader import cnh_reader

PROJECT_PATH    = '/home/naresh/cse592/cse592-project/trunk/'
DATA_DIR        = 'comics'
SRC_DIR         = 'src'
FT_VECTOR       = 'ft_vector.txt'
STOP_WORDS      = "stop.txt"
STEM_LIST       = "stem.txt"
FT_FIN_VECTOR   = 'ft_final_vector.txt'

COMIC_READERS   = [
    ('xkcd_reader', os.path.join(PROJECT_PATH, DATA_DIR, 'xkcd_comic_list.txt')),
    ('cnh_reader', os.path.join(PROJECT_PATH, DATA_DIR, 'cnh.txt')),
    ('cnh_reader', os.path.join(PROJECT_PATH, DATA_DIR, 'collegeroomiesfromhell.txt')),
    ('cnh_reader', os.path.join(PROJECT_PATH, DATA_DIR, 'dieselsweeties.txt')),
    ('cnh_reader', os.path.join(PROJECT_PATH, DATA_DIR, 'goats.txt')),
    ('cnh_reader', os.path.join(PROJECT_PATH, DATA_DIR, 'gpf.txt')),
    ('cnh_reader', os.path.join(PROJECT_PATH, DATA_DIR, 'nukees.txt')),
    ('cnh_reader', os.path.join(PROJECT_PATH, DATA_DIR, 'questionablecontent.txt')),
    ('cnh_reader', os.path.join(PROJECT_PATH, DATA_DIR, 'sheldon.txt'))
    ]
