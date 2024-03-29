#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright (c) 2013 Maxim Kovalev, Carnegie Mellon University
#    This file is part of Locationing Server.
#
#    Locationing Server is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Locationing Server is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Locationing Server.  If not, see <http://www.gnu.org/licenses/>.
import MySQLdb
import time
import bg_updater

class LocationResolver(object):
    
    def __init__(self, db_host = "localhost", db_user = "root", db_password = "",
                 db_name = "wifi_location_training_2", background_updates_delay = 10, debug = False):
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
        print self.id_to_name
        raise Exception("No entry with the id {} found".format(locid))
    
    def start_background_updates(self):
        self.bg_upd_thread = bg_updater.BackgroundUpdater(reference_class = self, delay = 10,
                                                          msg = "Location list was updated",
                                                          debug = self.debug)
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
        
        
    
