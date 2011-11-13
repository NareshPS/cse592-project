import config.siteconfig
import os, sys, datetime, json, string, re
import stringutils

class xkcd_reader:
    def __init__(self, location):
        self.datalocation   = location

    def connect(self):
        self.dataP          = open(os.path.join(config.siteconfig.PROJECT_PATH, config.siteconfig.DATA_DIR, self.datalocation), 'r')

    def get_next_instance(self):
        xkcd_json           = self.dataP.readline()
        if xkcd_json != None and len(xkcd_json) is not 0:
            trans_struct    = json.loads(xkcd_json)
            trans_date      = datetime.date(int(trans_struct['year']), int(trans_struct['month']), int(trans_struct['day']))
            return (trans_date.strftime('%d %b %Y').upper(), str(trans_struct['img']), stringutils.stringutils.cleanstr(trans_struct['transcript']))
        else:
            return None

    def disconnect(self):
        if self.dataP != None:
            self.dataP.close()
