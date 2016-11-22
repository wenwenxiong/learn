#!/usr/bin/env python

import urllib

params = urllib.urlencode({'id': 8, 'name': 'jack', 'age': 25})
print params
f = urllib.urlopen("http://localhost:18797/MailClient/test.aspx?%s" % params)
print f.read()
