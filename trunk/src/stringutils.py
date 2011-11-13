import re, string

class stringutils:
    trans   = string.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ[]{}\n\t.":\'?!,$@', 'abcdefghijklmnopqrstuvwxyz               ')
    @staticmethod
    def cleanstr(dirtystr):
        return re.sub(r'\s+', ' ', str(dirtystr).translate(stringutils.trans).strip())
        
