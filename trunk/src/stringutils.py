import re, string

class stringutils:
  '''
    This is for cleaning up the string. It first replaces
    the unwanted characters with spaces. Next, it removes
    more than one space from the input string.
    It uses python's maketrans function to translate
    unwanted characters to spaces.
  '''
  trans   = string.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ[]{}\n\t":()/?!$@', 'abcdefghijklmnopqrstuvwxyz               ')
  @staticmethod
  def cleanstr(dirtystr):
    '''
      Cleans up the input string.
    '''
    return re.sub(r'\s+', ' ', str(dirtystr).translate(stringutils.trans).strip())
    
