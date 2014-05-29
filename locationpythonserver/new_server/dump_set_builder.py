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

def create_sets(dump_by_location):
	test_set = []
	training_set = []
	for location, dump in dump_by_location.items():
		if len(dump) < 3:
			continue
		random.shuffle(dump)
		pivot = int(len(dump)*0.8)
		training_set += dump[:pivot]
		test_set += dump[pivot:]
	return training_set, test_set

def main():
    f = open("dump.txt", "r")
    dump = []
    dump_by_location = {}
    dump_by_device = {}
    for json_packet in f.readlines():
        #print json_packet
        try:
            json_obj = json.loads(json_packet)
            if not json_obj.has_key('location'):
                continue
            dump.append(json_obj)
            if dump_by_location.has_key(json_obj['location']):
                dump_by_location[json_obj['location']].append(json_obj)
            else:
                dump_by_location[json_obj['location']] = [json_obj]
            if json_obj.has_key('device_model'):
                if dump_by_device.has_key(json_obj['device_model']):
                    dump_by_device[json_obj['device_model']].append(json_obj)
                else:
                    dump_by_device[json_obj['device_model']] = [json_obj]

        except Exception as e:
            print e

    f.close()
    print len(dump), "objects"

    print "locations:", dump_by_location.keys()
    for location in dump_by_location.keys():
       print location, ":", len(dump_by_location[location]), "objects"

    for i in xrange(3):
	training_set, test_set = create_sets(dump_by_location)
        test_f = open("dump_test_by_location_%d.txt" % i, "w")
        training_f = open("dump_training_by_location_%d.txt" % i, "w")
        for json_obj in training_set:
            training_f.write(json.dumps(json_obj))
            training_f.write("\n")
        for json_obj in test_set:
            test_f.write(json.dumps(json_obj))
            test_f.write("\n")
        test_f.close()
        training_f.close()


    return
   
    test_f = open("dump_test_2.txt", "w")
    training_f = open("dump_training_2.txt", "w")
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
