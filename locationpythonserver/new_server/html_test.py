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

import lxml.html
import os


filespath = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(filespath, "static", "dashboard.html")
            
#f = open(filename, "r")
#content = "".join(f.readlines())
#f.close()
#page = lxml.etree.ElementTree(lxml.etree.XML(content))

page = lxml.html.parse(filename)

el = page.findall(".//div[@id=\"aaa\"]")[0]
print el.text
el.text = "trololo"


res = lxml.html.tostring(page, encoding = "utf-8", pretty_print = True)

print res