#!/usr/bin/env python

import MySQLdb

def _connect():
    db = MySQLdb.connect(host = 'localhost', user = 'root', db = 'wifilocation')
    db.set_character_set('utf8')
    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    return db, c

def get_all_locations():
    db, c = _connect()
    c.execute("SELECT location_id, location_name FROM locations")
    res = {}
    for (_id, name) in c.fetchall():
        res[int(_id)] = str(name)
    c.close()
    db.close()
    return res




def main():
    print get_all_locations()
    
if __name__ == "__main__":
    main()