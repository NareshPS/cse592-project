#! /usr/bin/python
import os,pickle

class save_object:
  def save_it(self, obj, store_name):
    '''
      Saves the object in a file. It uses python
      pickle module to dump to disk.
      obj         : Object to dump on disk.
      store_name  : File to store the object.
    '''
    if obj is not None and store_name is not None:
      fp  = open(store_name, 'w')
      pickle.dump(obj, fp)
      fp.close()
    else:
      raise Exception('Null object or store name')

  def load_it(self, store_name):
    '''
      Loads the object from file. Returns the read object.
      Uses pyhton pickle module to read from disk.
      store_name    : File to read the object from.
    '''
    if os.path.exists(store_name) is False:
      return None
    else:
      fp  = open(store_name, 'r')
      obj = pickle.load(fp)
      fp.close()
      return obj

if __name__ == '__main__':
  c=save_object()
  a=c.load_it('temp')
  if a is None:
    print 'Not Loaded'
    a        = {}
    a['abc']  = 123
    a['123']  = 'abc'
    c.save_it(a, 'temp')
