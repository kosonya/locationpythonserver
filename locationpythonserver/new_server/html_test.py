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