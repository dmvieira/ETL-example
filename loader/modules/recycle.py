# -*- coding: utf-8 -*-
import json, shutil, os
from datetime import datetime

class Feeder(object):
    '''
    receive filename of json file from bridge and db to store values
    '''
    def __init__(self,db):
        self.db = db
        self.now = datetime.now()

    def get_kind(self,code):
        print code
        kind = self.db(self.db.kind.code == code).select(self.db.kind.id).first()
        return kind.id

    def set_filename(self,filename):
        self.links = json.load(open(filename))
    
    def insert(self):
        try:
            for link in self.links:
                link['dt_arrive'] = self.now
                link['kind'] = self.get_kind(link['kind'])
                self.db.grantx.update_or_insert(self.db.grantx.link == link['link'],
                **link)
            self.db.commit()
        except:
            self.db.rollback()  
            raise #RuntimeError("Error storing new grants")
    
    def store(self):
        old = self.db(self.db.grantx.dt_arrive < self.now).select()
        try:
            for grant in old:
                grant_dict = grant.as_dict()
                grant_dict['dt_storage'] = self.now
                self.db.grantx_archive.insert(**grant_dict)
            self.db.commit()
        except:
            self.db.rollback()
            raise RuntimeError("Error storing old grants")
    
    def delete(self):
        try:
            self.db(self.db.grantx.dt_arrive < self.now).delete()
            self.db.commit()
        except:
            self.db.rollback()
            raise RuntimeError("Error removing old grants")        

class Dustman(object):
    '''
    receive path of bridge dump json files, crawler base path to get
    subdirectories and trash directory to move files
    '''
    def __init__(self,crawler,bridge,trash,accepted):
        self.crawler = os.path.abspath(crawler)
        self.bridge = os.path.abspath(bridge)
        self.trash = os.path.abspath(trash)
        self.bridgelist = []
        self.crawlerlist = []
        self.accepted = accepted
    
    def get_crawler_files(self):
        for folder in os.listdir(self.crawler):
            if folder in self.accepted:
                try:
                    for item in os.listdir(os.path.join(self.crawler,folder)):
                        if item.endswith(".json"):
                            self.crawlerlist.append(os.path.join(self.crawler,folder,item))
                except: pass
        return self.crawlerlist

    def get_bridge_files(self):
        for item in os.listdir(self.bridge):
            if item.endswith(".json"):
                self.bridgelist.append(os.path.join(self.bridge,item))
        return self.bridgelist

    def crawler_to_trash(self):
        folders = os.listdir(self.crawler)
        self.to_trash(self.crawler)
        for f in folders:
            os.mkdir(os.path.join(self.crawler,f))

    def bridge_to_trash(self):
        self.to_trash(self.bridge)
        
    def to_trash(self,origin):
        for item in os.listdir(origin):
            shutil.copy(os.path.join(origin,item),self.trash)
            os.remove(os.path.join(origin,item))

