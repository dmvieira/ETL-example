# -*- coding: utf-8 -*-
from modules import bridge, recycle, model
import json
import os
import hashlib

def main():

    CRAWLER = os.path.join('..', 'crawler')
    ACCEPTED = ['faperj', 'cnpq', 'dfg.de', 'nsf', 'grant.gov']
    BRIDGE = 'result'
    TRASH = 'trash'

    db = model.get_db()

    dustman = recycle.Dustman(CRAWLER,BRIDGE,TRASH,ACCEPTED)
    crawlerlist = dustman.get_crawler_files()
    # make bridge function for all crawler files
    for cfile in crawlerlist:
        cjson = json.load(open(cfile))
        print cfile
        for c in cjson:
            bridge.saveit(c['name'], c['uri'],
                          c['site'],
                          os.path.join(BRIDGE,
                                       hashlib.md5(
                                           c['uri']
                                       ).hexdigest())+'.json',
                          c['kind'], c.get('text', ''))
    bridgelist = dustman.get_bridge_files()
    # make recycle functions for inserting new grants into database

    f = recycle.Feeder(db)
    for bfile in bridgelist:
        f.set_filename(bfile)
        f.insert() # insert or update old files
    f.store() # store old files into backup table
    f.delete() # delete old files
    dustman.bridge_to_trash()

if __name__ == "__main__":
    main()
