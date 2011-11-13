import os
import config.siteconfig
import stringutils

class cnh_reader:
    def __init__(self, location):
        self.datalocation   = location

    def connect(self):
        self.dataP  = open(os.path.join(config.siteconfig.PROJECT_PATH, config.siteconfig.DATA_DIR, self.datalocation), 'r')

    def get_next_instance(self):
        cnh_date    = self.dataP.readline().strip()
        if len(cnh_date) is 0:
            return None
        cnh_trans   = self.dataP.readline().strip()
        cnh_url     = self.dataP.readline().strip()

        return (cnh_date, cnh_url, stringutils.stringutils.cleanstr(cnh_trans))

    def disconnect(self):
        if self.dataP is not None:
            self.dataP.close()


    
