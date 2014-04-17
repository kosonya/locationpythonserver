#!/usr/bin/env python

import datamanager
import jsonparser
import locationresolver
import httplib
import json
import MySQLdb
import time

def write_data(filename):
    f = open(filename, "r")
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
    rights = 0
    conn = httplib.HTTPConnection(host = "localhost", port = 8080)
    for i, json_obj in enumerate(dump):
        trueloc = json_obj['location']
        json_str = json.dumps(json_obj)
        print "Object", i+1, "out of", len(dump)
        print json_str
        conn.request("POST", "/api/v1/process_wifi_gps_reading/list/", json_str, {"Content-type": "application/json"})
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        print data
        try:
            loc = json.loads(response.reason)[0]['location_name']
            print "Sent location:", trueloc, "; received location:", loc
            if loc == trueloc:
                print "That's correct!"
                rights += 1
                print "Success rate so far:", float(rights)/(i+1)
        except Exception as e:
           pass
    print "Success rate:", float(rights)/len(dump)


def purge_database():
        db = MySQLdb.connect(host = 'localhost', user = 'root',
                             passwd = '', db = 'wifi_location_training')
        db.set_character_set('utf8')
        c = db.cursor()
        c.execute('SET NAMES utf8')
        c.execute('SET CHARACTER SET utf8')
        c.execute('SET character_set_connection=utf8')
        c.execute('delete from gps_and_signal_readings')
        c.execute('delete from locations')
        c.execute('delete from wifi_readings')
        c.close()
        db.close()

def read_data(filename, by_location_arrs, by_device_arrs):
    f = open(filename, "r")
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
    dump_len = len(dump)
    rights = 0
    conn = httplib.HTTPConnection(host = "localhost", port = 8080)
    by_location = {}
    by_device = {}
    for i, json_obj in enumerate(dump):
        trueloc = json_obj['location']
        dev = json_obj['device_model']
        del json_obj['location']
	should_continue = True
	no_gps = False
	no_wifi = False
	if no_wifi:
		for key in json_obj.keys():
			if "wifi" in key:
				del json_obj[key]
			elif "GPS" in key:
				should_continue = False
		if should_continue:
			dump_len -= 1
			continue
	elif no_gps:
		for key in json_obj.keys():
			if "GPS" in key:
				del json_obj[key]
			elif "wifi" in key:
				should_continue = False
		if should_continue:
			dump_len -= 1
			continue
        json_str = json.dumps(json_obj)
        print "Object", i+1, "out of", len(dump)
        print json_str
        conn.request("POST", "/api/v1/process_wifi_gps_reading/list/", json_str, {"Content-type": "application/json"})
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        if by_location.has_key(trueloc):
            by_location[trueloc][0] += 1
        else:
            by_location[trueloc] = [1, 0]
        if by_device.has_key(dev):
            by_device[dev][0] += 1
        else:
            by_device[dev] = [1, 0]
        print data
        try:
            loc = json.loads(response.reason)[0]['location_name']
            print "Sent location:", trueloc, "; received location:", loc
            if loc == trueloc:
                print "That's correct!"
                rights += 1
                by_location[trueloc][1] += 1
                by_device[dev][1] += 1
                print "Success rate so far:", float(rights)/(i+1)
        except Exception as e:
           pass
    print "Success rate:", float(rights)/dump_len

    print by_location
    print by_device

    if by_location_arrs.has_key('Total'):
        by_location_arrs['Total'].append( (dump_len, rights) )
    else:
        by_location_arrs['Total'] = [(dump_len, rights)]

    if by_device_arrs.has_key('Total'):
        by_device_arrs['Total'].append( (dump_len, rights) )
    else:
        by_device_arrs['Total'] = [(dump_len, rights)]

    for location in by_location.keys():
        if by_location_arrs.has_key(location):
            by_location_arrs[location].append( (by_location[location][0], by_location[location][1]) ) 
        else:
            by_location_arrs[location] = [(by_location[location][0], by_location[location][1])]

    for device in by_device.keys():
        if by_device_arrs.has_key(device):
            by_device_arrs[device].append( (by_device[device][0], by_device[device][1])) 
        else:
            by_device_arrs[device] = [(by_device[device][0], by_device[device][1])]


    return by_location_arrs, by_device_arrs


def build_report(arrs):
	res = """\hline"""
	res += "\n"
	for key in arrs.keys():
		line = key
		total = 0
		total_rights = 0
		for pair in arrs[key]:
			line += " & " + str(pair[0])
			line += " & " + ("%3.1f\%%" % (100*float(pair[1])/pair[0]))
			total += pair[0]
			total_rights += pair[1]
		line += " & " + str(total)
		line += " & " + ("%3.1f\%%" % (100*float(total_rights)/total))
		line += """\\\\""" + '\n'
		line += """\hline""" + '\n'
		res += line
	return res

def main():
	by_location_arrs = {}
	by_device_arrs = {}
	for i in xrange(3):
		filename = "dump_training_by_location_%d.txt" % i
		print filename
		print "Purging database, stop the server"
		raw_input()
		purge_database()
		print "Database purged, start the server"
		raw_input()
		write_data(filename)
		print "Server stuffed, waiting for reloading"
		time.sleep(10)
		filename = "dump_test_by_location_%d.txt" % i
		by_location_arrs, by_device_arrs = read_data(filename, by_location_arrs, by_device_arrs)
		print by_location_arrs, by_device_arrs

	print by_location_arrs
	print by_device_arrs

	print build_report(by_location_arrs)
	print "\n\n\n\n"
	print build_report(by_device_arrs)

if __name__ == "__main__":
	main()
