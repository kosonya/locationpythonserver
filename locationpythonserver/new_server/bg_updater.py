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
import time
import threading


class BackgroundUpdater(threading.Thread):
    def __init__(self, reference_class, delay = 10, msg = "Something was updated", debug = True):
        super(BackgroundUpdater, self).__init__()
        self.reference_class = reference_class
        self.delay = delay
        self.msg = msg
        self.debug = debug
        self.running = True
        
    def run(self):
        while self.running:
            self.reference_class.fetch_all_from_db()
            if self.debug:
                print "{}! Sleeping for {} seconds".format(self.msg, self.background_updates_delay)
                time.sleep(self.delay)