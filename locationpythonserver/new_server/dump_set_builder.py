#!/usr/bin/env python
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
import datamanager
import jsonparser
import locationresolver
import httplib
import json
import random

def main():
    f = open("dump.txt", "r")
    dump = []
    for json_packet in f.readlines():
        #print json_packet
        try:
            json_obj = json.loads(json_packet)
            if not json_obj.has_key('location'):
                continue
            dump.append(json_obj)
        except Exception as e:
            print e

    print len(dump), "objects"
    return
    test_f = open("dump_test.txt", "w")
    training_f = open("dump_training.txt", "w")
    for json_obj in dump:
        if random.random() > 0.8:
            test_f.write(json.dumps(json_obj))
            test_f.write("\n")
        else:
            training_f.write(json.dumps(json_obj))
            training_f.write("\n")
    test_f.close()
    training_f.close()
        
        
        
if __name__ == "__main__":
    main()
