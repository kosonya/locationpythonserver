#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time
import threading

class LocationResolver(object):
    
    def __init__(self, db_host = "localhost", db_user = "root", db_password = "",
                 db_name = "wifilocation", background_updates_delay = 10, debug = False):
        self.name_to_id = {}
        self.id_to_name = {}
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.background_updates_delay = background_updates_delay
        self.debug = debug
        self.fetch_all_from_db()
        
    def db_init(self):
        db = MySQLdb.connect(host = self.db_host, user = self.db_user,
                             passwd = self.db_password , db = self.db_name)
        db.set_character_set('utf8')
        c = db.cursor()
        c.execute('SET NAMES utf8')
        c.execute('SET CHARACTER SET utf8')
        c.execute('SET character_set_connection=utf8')
        return db, c 
        
    def fetch_all_from_db(self):
        db, c = self.db_init()
        query_template = "SELECT location_id, location_name FROM locations"
        c.execute(query_template)
        for locid, locname in c.fetchall():
            self.name_to_id[locname.decode("utf-8")] = int(locid)
            self.id_to_name[int(locid)] = locname.decode("utf-8")
        c.close()
        db.close()
        
    def add_location(self, locname):
        db, c = self.db_init()
        query_template = "INSERT INTO locations (location_name) VALUES (%s)"
        c.execute(query_template, unicode(locname))
        c.close()
        db.commit()
        db.close()
        
    def resolve_name(self, locname):
        ulocname = unicode(locname)
        
        if self.name_to_id.has_key(ulocname):
            return self.name_to_id[ulocname]
        
        self.fetch_all_from_db()
        if self.name_to_id.has_key(ulocname):
            return self.name_to_id[ulocname]
         
        self.add_location(ulocname)
        self.fetch_all_from_db()
        if self.name_to_id.has_key(ulocname):
            return self.name_to_id[ulocname]
        
        raise Exception("What was THAT?!")

    def resolve_id(self, locid):
        if self.id_to_name.has_key(locid):
            return self.id_to_name[locid]
        
        self.fetch_all_from_db()
        if self.id_to_name.has_key(locid):
            return self.id_to_name[locid]
        
        raise Exception("No entry with the id {} found".format(locid))
    
    def start_background_updates(self):
        def update(main_class):
            while True:
                main_class.fetch_all_from_db()
                if self.debug:
                    print "Location list updated! Sleeping for {} seconds".format(self.background_updates_delay)
                time.sleep(self.background_updates_delay)
            
        self.bg_upd_thread = threading.Thread(target = update, args = [self])
        self.bg_upd_thread.daemon = True
        self.bg_upd_thread.start()

def main():
    loc_res = LocationResolver(background_updates_delay = 1)
    #loc_res.add_location(u"Дом' 私の家")
    loc_res.fetch_all_from_db()
    for _id, name in  loc_res.id_to_name.items():
        print _id, name
    print loc_res.name_to_id
    
    print loc_res.resolve_name(u"Дом'\' 私の家")
    print loc_res.name_to_id  
    print loc_res.resolve_id(23)
    loc_res.start_background_updates()
    time.sleep(10)
    loc_res.background_updates_delay = 2
    time.sleep(10)
    
if __name__ == "__main__":
    main()
        
        
    